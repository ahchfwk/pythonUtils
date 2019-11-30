'''created by fwk
   2017/12/20
   get release from https://api.github.com/repos/
'''
import json
import requests
import MySQLdb


def check_tag(project_url):
    
    url_prefix = 'https://api.github.com/repos/'
    commit_url = url_prefix + project_url[19:] + '/releases'
    token = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
             'Authorization': 'token ' + 'e3572f2f2cf0e8075fd3dea841050257063809d5'}
    release_json = requests.get(commit_url, headers=token, timeout=30).json()
    print 'Project name: ' + project_url[19:]
    for item in release_json:
        if isinstance(item, dict):
            if item['tag_name']:
                # print item['tag_name']
                pass
            else:
                print '---------------------------', item['name']



if __name__ == '__main__':
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    sql = 'select git_address from fdroid.repository'
    dbcursor.execute(sql)
    repoadd = dbcursor.fetchall()
    repoadd = [x[0] for x in repoadd]
    dbcursor.close()
    dbconn.close()
    c = 1
    for i in repoadd:
        print c
        check_tag(i)
        c += 1
