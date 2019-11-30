# -*- coding:utf-8 -*-
'''created by fwk
   2018/4/8
   use hdfs to copy repository from server to local
'''

import os
import hdfs
import MySQLdb


path = os.path.join(os.path.basename(__file__), '../')
# os.path.split(os.path.realpath(__file__))[0]


def getRepoFromHdfs_batch(repoNumber=10):
    '''copy repo from server using hdfs'''
    client = hdfs.Client("http://10.141.221.82:50070", root='/home/fdse')
    repositories = client.list("/java/repositories")
    for r in repositories[:repoNumber]:
        client.download(u'/java/repositories/'+r, os.path.join(path, 'repositories'))
        print r, ' has download...'
        print os.path.join(path, 'repositories')

        
def getReleaseFromHdfs_batch(releaseNumber=10):
    '''copy releases form server using hdfs'''
    client = hdfs.Client("http://10.141.221.82:50070", root='/home/fdse')
    releases = client.list("/java/releases")
    for r in releases[:releaseNumber]:
        client.download(u'/java/releases/'+r, os.path.join(path, 'releases'))
        print r, ' has download...'


def gitclone(gitaddr, localpath):
    os.chdir(localpath)
    os.popen('git clone '+gitaddr)


if __name__ == "__main__":
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'codehub')
    dbcursor = dbconn.cursor()
    sql = """SELECT distinct repository_id, local_addr, git_addr FROM codehub.repository_java where repository_id in 
            (SELECT distinct repository_id FROM codehub.tmp_commit_tobe_clonedetect)"""
    dbcursor.execute(sql)
    result = dbcursor.fetchall()
    dbcursor.close()
    dbconn.close()
    # 速度慢，效果一般
    # client = hdfs.Client("http://10.141.221.82:50070", root='/home/fdse')
    # for i in result:
    #     try:
    #         client.download('/java/'+i[1], r"C:\Users\fwk\Desktop\py\codehub\repositories")
    #         print '/java/'+i[1], r"C:\Users\fwk\Desktop\py\codehub\repositories"
    #     except:
    #         print 'no '+'/java/'+i[1]

    # 采用git clone
    os.chdir(r'C:\Users\fwk\Desktop\py\codehub\repositories')
    for i in result[5:]:
        dir = i[1].split('/')
        if not os.path.exists(dir[-2]):
            os.mkdir(dir[-2])
        os.chdir(dir[-2])
        os.popen('git clone '+i[2])
        os.chdir(r'C:\Users\fwk\Desktop\py\codehub\repositories')
        print i