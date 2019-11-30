'''created by fwk
   2018/01/23
   将fdroid上的项目从github上clone下来
'''


import os
import MySQLdb

def get_url_from_mysql():
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    sql = 'select repository_name,git_address from repository'
    dbcursor.execute(sql)
    result = dbcursor.fetchall()
    dbcursor.close()
    dbconn.close()
    return result


def get_url_from_txt():
    f = open('t.txt','r')
    r = f.readlines()
    s = []
    for i in r:
        s.append(i.strip().split())
    return s


def git_clone(repo_url):
    r = repo_url.split('/')
    os.system('git clone '+repo_url+' '+r[-2]+'-'+r[-1])
    print r[-2]+'-'+r[-1]


if __name__ == '__main__':
    result = get_url_from_txt()[84:]
    i = 85

    for r in result:
        print i,
        git_clone(r[1])
        i += 1
