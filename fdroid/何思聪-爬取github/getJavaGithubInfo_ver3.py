#coding:utf-8
from redis import Redis
import MySQLdb
import requests
from multiprocessing import Process
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import traceback
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def mail(sender, password, receiver, SMTP_server, content):
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = _format_addr('CrawlGithubInfo <%s>' % sender)
        msg['To'] = _format_addr('管理员 <%s>' % receiver)
        msg['Subject'] = Header('CrawlGithubInfo Message', 'utf-8').encode()
        server = smtplib.SMTP(SMTP_server, 25)
        server.set_debuglevel(1)
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())
        server.quit()
        traceback.print_exc()

def get_token():
    cursor.execute("select token from github_token")
    global tokens
    tokens = cursor.fetchall()

def get_data():
    get_token()
    while True:
        try:
            r = Redis(host = '10.131.252.156',db = 1, port = 6379)
            token = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
                     'Authorization': 'token ' + tokens[int(r['CurrentToken'])][0]}
        except Exception as e:
            print "1-----", time.ctime(time.time()), Exception, ':', e
            continue
        try:
            current_index = r.rpop('RepositoryIndex').decode()
            repository_API = "https://api.github.com/repositories?since=" + current_index
            #print current_index   #调试
            repository_json = requests.get(repository_API, headers = token, timeout = 30).json()
        except Exception as e:
            print "2-----", time.ctime(time.time()), Exception, ':', e
            time.sleep(5)
            r.rpush('RepositoryIndex',current_index)
            print current_index,"crawl again"
            continue
        finally:
            r['hit'] = str(int(r['hit']) + 1)
            if int(r['hit']) > 4500:
                if int(r['CurrentToken']) < 9:  # 遍历到n+1为止
                    r['CurrentToken'] = str(int(r['CurrentToken']) + 1)
                    r['hit'] = '0'
                else:
                    r['CurrentToken'] = '0'  # id重置为1
                    r['hit'] = '0'
        if len(repository_json) == 0:
            break
        elif len(repository_json) == 2:
            if 'message' in repository_json:
                if 'exceeded' in repository_json['message']:    #账号flagged out处理
                    try:
                        print 'Repository Failed'
                        print repository_json
                        time.sleep(5)
                        r.rpush('RepositoryIndex', current_index)
                        print current_index, "crawl again"
                        content = repository_json['message'] + '\n' + 'the current index is ' + current_index
                        mail(sender, password, receiver, SMTP_server, content)
                        if int(r['CurrentToken']) < 9:  # 遍历到n+1为止
                            r['CurrentToken'] = str(int(r['CurrentToken']) + 1)
                            r['hit'] = '0'
                        else:
                            r['CurrentToken'] = '0'  # id重置为1
                            r['hit'] = '0'
                        if repository_json['message'] not in ban_list:
                            ban_list.append(repository_json['message'])
                            if len(ban_list) == 10:                 #所有账号
                                content = 'All accounts have been flagged out.'
                                mail(sender, password, receiver, SMTP_server, content)
                                break
                    except:
                        traceback.print_exc()
                elif 'suspended' in repository_json['message']:     #账号suspended处理
                    try:
                        r.rpush('RepositoryIndex', current_index)
                        content = repository_json['message'] + '\n' + \
                                  'the current index is ' + current_index + '\n' + \
                                  'the current token is ' + str(r['CurrentToken'])
                        mail(sender, password, receiver, SMTP_server, content)
                        break
                    except:
                        traceback.print_exc()
            continue
        else:
            for i in range(len(repository_json)):
                language = ''
                try:
                    LanguageUrl = repository_json[i]['languages_url']
                    LanguageResponse = requests.get(LanguageUrl, headers = token, timeout = 30)
                    LanguageJson = LanguageResponse.json()
                    # print(LanguageJson)     # 调试
                    if len(LanguageJson) == 0:
                        continue
                    elif len(LanguageJson) == 2:
                        if 'message' in LanguageJson:
                            continue
                        else:
                            for LanguageItem in LanguageJson:
                                language += LanguageItem + ' '
                            language = language[:-1]
                    else:
                        for LanguageItem in LanguageJson:
                            language += LanguageItem + ' '
                        language = language[:-1]
                    #print i + 1,":",language  # 调试
                except Exception as e:
                    print "3-----", time.ctime(time.time()), '----' + current_index + '----' + str(i), Exception, ':', e
                    traceback.print_exc()
                    time.sleep(5)
                    continue
                finally:
                    r['hit'] = str(int(r['hit']) + 1)
                    if int(r['hit']) > 4500:
                        if int(r['CurrentToken']) < 9:  # 遍历到n+1为止
                            r['CurrentToken'] = str(int(r['CurrentToken']) + 1)
                            r['hit'] = '0'
                        else:
                            r['CurrentToken'] = '0'  # id重置为1
                            r['hit'] = '0'
                try:
                    github_id = repository_json[i]['id']
                    name = repository_json[i]['name']
                    if isinstance(repository_json[i]['owner'], dict):
                        user_id = repository_json[i]['owner']['id']
                        user_name = repository_json[i]['owner']['login']
                    else:
                        user_id = -1
                        user_name = 'Null'
                    website = repository_json[i]['html_url']
                    sql = "insert into github_repository_1(github_id, name, user_id, user_name, language, website) values(%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (github_id, name, user_id, user_name, language, website))
                    connect.commit()
                    r['TotalCount'] = str(int(r['TotalCount']) + 1)
                    if 'Java' in LanguageJson:
                        try:
                            repos_url = website.replace('https://github.com', 'https://api.github.com/repos')
                            repos_json = requests.get(repos_url, headers = token, timeout = 25).json()
                            stars = repos_json['stargazers_count']
                        except Exception as e:
                            print "4-----", time.ctime(time.time()), str(i) + '  ' + str(github_id), Exception, ':', e
                            stars = str(-1)
                            time.sleep(3)
                        finally:
                            sql = "insert into java_github_repository_1(github_id, name, user_id, user_name, website, stars) values(%s, %s, %s, %s, %s, %s)"
                            cursor.execute(sql, (github_id, name, user_id, user_name, website, stars))
                            connect.commit()
                            r['JavaCount'] = str(int(r['JavaCount']) + 1)
                            r['hit'] = str(int(r['hit']) + 1)
                            if int(r['hit']) > 4500:
                                if int(r['CurrentToken']) < 9:  # 遍历到n+1为止
                                    r['CurrentToken'] = str(int(r['CurrentToken']) + 1)
                                    r['hit'] = '0'
                                else:
                                    r['CurrentToken'] = '0'  # id重置为1
                                    r['hit'] = '0'
                except Exception as e:
                    print "5-----", time.ctime(time.time()), str(i) + '  ' + str(github_id), Exception, ':', e
                    print name, user_id, user_name, website
                    #traceback.print_exc()
                    time.sleep(10)
            try:
                if r['IsPaused'].decode() == 'yes':
                    print "The process has paused safely, you have 1 hour to kill it."
                    time.sleep(3600)
                    r['IsPaused'] = 'no'
            except:
                try:
                    content = 'Fatal error\n' + 'the current index is ' + current_index
                    mail(sender, password, receiver, SMTP_server, content)
                    traceback.print_exc()
                except:
                    break
                traceback.print_exc()
                break

class CrawlData(Process):
    def __init__(self):
        Process.__init__(self)
    def run(self):
        get_data()

tokens = []
connect = MySQLdb.connect(
        host = '10.131.252.156',
        port = 3306,
        user = 'root',
        passwd = 'root',
        db = 'github',
        charset = 'utf8'
        )
cursor = connect.cursor()
ban_list = []
f_handler = open('/home/fdse/Downloads/pythonFile/test.txt', 'r')
sender = f_handler.readline()[15:-1]
password = f_handler.readline()[15:-1]
receiver = f_handler.readline()[15:-1]
SMTP_server = f_handler.readline()[15:-1]
f_handler.close()

if __name__ == '__main__':
    get_data()
