# -*- coding:utf-8 -*-
'''created by fwk
   2018/01/26
   Insert commit and date into datebase
   but there's something wrong,please refer to new
'''
import os
import MySQLdb


def get_repoid_from_mysql():
    '''返回repository_id 和 项目相对路径 的 list'''
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    sql = 'select repository_id,local_address from repository'
    dbcursor.execute(sql)
    result = dbcursor.fetchall()
    dbcursor.close()
    dbconn.close()
    result = [(x[0], x[1].split('/')[-1]) for x in result]
    return result


def get_commitid():
    '''遍历fdroid本地文件夹，获取commitid和commitdate，并入库'''
    month = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
             'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    result = get_repoid_from_mysql()
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    dbcursor.execute('select distinct repository_id from cc_intra_commit')
    tem = dbcursor.fetchall()
    tem = [x[0] for x in tem]
    print len(tem)
    print len(result)
    os.chdir('E:/fdroid')
    rere = result[:]

    for i in rere:
        if i[0] not in tem:
            if os.path.exists(i[1]):
                os.chdir(i[1])
            else:
                continue
            print (i)
            log = os.popen('git log')
            commit = ''
            for line in log.readlines():
                if line.startswith('commit'):
                    commit = line[7:-1]
                if line.startswith('Date:'):
                    date = line[8:-1]
                    tem = date.split()
                    date = tem[-2]+'-'+month[tem[1]]+'-'+tem[2]+' '+tem[3]
                    sql = 'INSERT INTO cc_intra_commit (Repository_Id,Commit_Id,Commit_Date) VALUES (%s,%s,%s)'
                    try:
                        dbcursor.execute(sql, (i[0], commit, date))
                    except:
                        dbconn.rollback()
                        print '????'
                    dbconn.commit()
            os.chdir('E:/fdroid')
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
        dbcursor.execute('select repository_id from repository where local_address = "%s"' % ('/root/BigCode/FdroidRepo/'+f))
        tem = dbcursor.fetchall()
        
        if len(tem) > 1:
            print tem
            x += 1
    print x   

if __name__ == '__main__':
    # print get_commitid()
    # '2014-11-03 03:16:25'  'Tue Sep 17 02:27:17 2013 +0800'
    find_same_localaddress()