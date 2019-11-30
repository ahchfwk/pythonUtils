#coding:utf-8
import MySQLdb
from redis import Redis
import requests
import os
import urllib
import time
import traceback

def get_token():
    cursor.execute("select token from github_token")
    global tokens
    tokens = cursor.fetchall()

def download_tar(url):
    file_name = url.replace('https://api.github.com/repos/', '').replace('/', '-')
    dir_name = '/home/fdse/Downloads/GithubJavaReleases/' + file_name[:file_name.find('-tarball')]
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    path = dir_name + '/' + file_name.replace('-tarball', '') + '.tar.gz'
    urllib.socket.setdefaulttimeout(7200)
    urllib.urlretrieve(url, path)
    #print path



connect = MySQLdb.connect(
        host = '10.131.252.156',
        port = 3306,
        user = 'root',
        passwd = 'root',
        db = 'github',
        charset = 'utf8'
        )
tokens = []
cursor = connect.cursor()
get_token()
ban_list = []
connect.close()
while True:
    try:
        r = Redis(host ='10.131.252.156', port = 6379, db = 1)
        #index = r.rpop('id-160').decode()
        index = r['CurrentIndex'].decode()
        r['CurrentIndex'] = str(int(r['CurrentIndex']) + 1)
        connect_160 = MySQLdb.connect(
            host = '10.131.252.156',
            port = 3306,
            user ='root',
            passwd = 'root',
            db = 'github',
            charset = 'utf8'
        )
        cursor = connect_160.cursor()
        sql = "select website from java_github_repository_1 where id >=" + index +  " and id <" + str(int(index) + 1)
    except Exception as e:
        print Exception, ":", e
        print "the current time is:", time.ctime(time.time())
        print "the current index is:", index
        time.sleep(10)
        continue
    try:
        cursor.execute(sql)
        url_suffix = cursor.fetchone()[0].replace('https://github.com/', '') + '/releases'
        url_prefix = "https://api.github.com/repos/"
        url = url_prefix + url_suffix
        connect_160.close()
    except Exception as e:
        print "--------url's getting failed--------"
        #traceback.print_exc()
        print Exception, ':', e
        print "the current time is:", time.ctime(time.time())
        print "the current index is:",index
        print "------------------------------------"
        print "\n"
        time.sleep(2)
        continue
    try:
        token = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
                 'Authorization': 'token ' + tokens[int(r['CurrentToken-160'])][0]}
        releases_json = requests.get(url, headers = token).json()
    except Exception as e:
        print "--------release_json's getting failed--------"
        print url, ':', Exception, ':', e
        print "the current time is:", time.ctime(time.time())
        print "the current index is:", index
        print "---------------------------------------------"
        print "\n"
        time.sleep(2)
        continue
    finally:
        r['hit-160'] = str(int(r['hit-160']) + 1)
        if int(r['hit-160']) > 4500:
            if int(r['CurrentToken-160']) < 12:  # 遍历到n+1为止
                r['CurrentToken-160'] = str(int(r['CurrentToken-160']) + 1)
                r['hit-160'] = '0'
            else:
                r['CurrentToken-160'] = '11'  # id重置为12
                r['hit-160'] = '0'
    if len(releases_json) == 0:
        #print("the json of",url,"is none") # 调试
        continue
    elif len(releases_json) == 2:
        if 'message' in releases_json:
            if "API rate limit exceeded for" in releases_json['message']:
                print "----------------message----------------"
                print time.ctime(time.time()),'-----' + index
                print releases_json
                print "---------------------------------------\n"
                if releases_json['message'].decode() not in ban_list:
                    ban_list.append(releases_json['message'].decode())
                    if len(ban_list) == 2:
                        break
                if int(r['CurrentToken-160']) < 12:
                    r['CurrentToken-160'] = str(int(r['CurrentToken-160']) + 1)
                    r['hit-160'] = '0'
                else:
                    r['CurrentToken-160'] = '11'  # id重置为12
                    r['hit-160'] = '0'
                continue
            else:
                continue
        else:
            print "[-----------------------------------downloading start------------------------------------]"
            print "start at:", time.ctime(time.time())
            for i in range(len(releases_json)):
                try:
                    download_url = releases_json[i]['tarball_url']
                    print time.ctime(time.time()), index, ':from ' + download_url + ' downloading...'  # 调试
                    download_tar(download_url)
                    time.sleep(3)
                except Exception as e:
                    print "--------downloading failed--------"
                    print url, ':', Exception, ':', e
                    print "the current time is:", time.ctime(time.time())
                    print "the current index is:", index
                    print "----------------------------------"
                    print "\n"
                    time.sleep(3)
                finally:
                    r['hit-160'] = str(int(r['hit-160']) + 1)
                    if int(r['hit-160']) > 4500:
                        if int(r['CurrentToken-160']) < 12:  # 遍历到n+1为止
                            r['CurrentToken-160'] = str(int(r['CurrentToken-160']) + 1)
                            r['hit-160'] = '0'
                        else:
                            r['CurrentToken-160'] = '11'  # id重置为12
                            r['hit-160'] = '0'
                # for t in range(5, 0, -1):
                #     print("program can be terminated safely now, you have", t, "seconds to terminate it")
                #     time.sleep(1)
            r['DownloadCount-160'] = str(int(r['DownloadCount-160']) + 1)
            print "end at:", time.ctime(time.time())
            print "[----------------------------------------------------------------------------------------]"
            print "\n"
    else:
        print "[-----------------------------------downloading start------------------------------------]"
        print "start at:", time.ctime(time.time())
        for i in range(len(releases_json)):
            try:
                download_url = releases_json[i]['tarball_url']
                download_tar(download_url)
                time.sleep(3)
                print time.ctime(time.time()), index, ':from ' + download_url + ' downloading...'  # 调试
            except Exception as e:
                print "--------downloading failed--------"
                print url, ':', Exception, ':', e
                print "the current time is:", time.ctime(time.time())
                print "the current index is:", index
                print "----------------------------------"
                print "\n"
                time.sleep(3)
            finally:
                r['hit-160'] = str(int(r['hit-160']) + 1)
                if int(r['hit-160']) > 4500:
                    if int(r['CurrentToken-160']) < 12:  # 遍历到n+1为止
                        r['CurrentToken-160'] = str(int(r['CurrentToken-160']) + 1)
                        r['hit-160'] = '0'
                    else:
                        r['CurrentToken-160'] = '11'  # id重置为12
                        r['hit-160'] = '0'
            # for t in range(5, 0, -1):
            #     print("program can be terminated safely now, you have", t, "seconds to terminate it")
            #     time.sleep(1)
        r['DownloadCount-160'] = str(int(r['DownloadCount-160']) + 1)
        print "end at:", time.ctime(time.time())
        print "[----------------------------------------------------------------------------------------]"
        print "\n"
        try:
            if r['IsPaused-C'].decode() == 'yes':
                print "The process has paused safely, you have 30 minutes to kill it."
                time.sleep(1800)
                r['IsPaused-C'] = 'no'
        except:
            traceback.print_exc()
