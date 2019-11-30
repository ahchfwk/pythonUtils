# -*- coding:utf-8 -*-
'''created by fwk
   2018/03/20
   Insert commit and date into datebase
'''
import os
import MySQLdb


def get_repoid_from_mysql():
    '''返回repository_id 和 项目相对路径 的 list'''
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    sql = """select distinct cc_intra_release.Repository_Id,repository.local_address from fdroid.cc_intra_release, 
    fdroid.repository where repository.repository_id = cc_intra_release.Repository_Id"""
    dbcursor.execute(sql)
    result = dbcursor.fetchall()
    dbcursor.close()
    dbconn.close()
    resultDict = {}
    for i in result:
        resultDict[i[1].split('/')[-1]] = i[0]
    return resultDict


def get_commitid():
    '''遍历fdroid本地文件夹，获取commitid和commitdate，并入库'''
    month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
             'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

    os.chdir('E:/codeclone/fdroid')
    repolist = os.listdir('E:/codeclone/fdroid')
    repoDict = get_repoid_from_mysql()
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    for i in repolist:
        repository_id = repoDict[i]
        os.chdir(i)
        log = os.popen('git log --pretty=format:"%H*%cd"')
        for line in log.readlines():
            commit = line.split('*')[0]
            tem = line.split('*')[1].split()
            date = tem[-2] + '-' + month[tem[1]] + '-' + tem[2] + ' ' + tem[3]
            sql = 'INSERT INTO cc_intra_commit (Repository_Id,Commit_SHA,Commit_Date,related_release) VALUES (%s,%s,%s,%s)'
            
            dbcursor.execute(sql, (repository_id, commit, date, 'null'))
            print repository_id, commit, date
            
        dbconn.commit()
        os.chdir('E:/codeclone/fdroid')
    dbcursor.close()
    dbconn.close()


def find_same_localaddress():
    '''找出不合理的数据，返回对应同一个local_address的repository的repository_id'''
    os.chdir('E:/fdroid')
    filelist = os.listdir('.')
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    x = 0
    for f in filelist:
        dbcursor.execute('select repository_id from repository where local_address = "%s"' % (
            '/root/BigCode/FdroidRepo/' + f))
        tem = dbcursor.fetchall()

        if len(tem) > 1:
            print tem
            x += 1
    print x


if __name__ == '__main__':
    # print get_commitid()
    # '2014-11-03 03:16:25'  'Tue Sep 17 02:27:17 2013 +0800'
    get_commitid()
