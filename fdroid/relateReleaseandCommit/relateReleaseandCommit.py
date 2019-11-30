#-*- coding:utf-8 -*-
'''created by fwk
   2018/3/16
   purpose ：将release和commit关联，通过时间
'''
import MySQLdb
import datetime


def redate(cdate, releasesDict):
    """根据commit日期找到最相近的且是commit日期前的release日期"""
    #先对releaseDict排序
    items = sorted(releasesDict.items())
    for i in range(len(items)-1):
        if items[i][0] <= cdate and items[i+1][0] > cdate:
            return releasesDict[items[i][0]]
    if items[-1][0] <= cdate:
        return releasesDict[items[-1][0]]
    return None


if __name__ == "__main__":

    updatesql = "update fdroid.cc_intra_commit set related_release ='%s' where Repository_Id=%s and Commit_SHA='%s'"
    querysql = """SELECT distinct Repository_Id FROM fdroid.cc_intra_release"""
    commitsql = "SELECT * FROM fdroid.cc_intra_commit where Repository_Id =%s"
    releasesql = """SELECT * FROM fdroid.cc_intra_release where Repository_Id =%s"""
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    dbcursor.execute(querysql)
    repoid = dbcursor.fetchall()

    # 对于每个Repository_id
    for i in repoid:
        # 查询给定id对应的commits
        dbcursor.execute(commitsql % i)
        commits = list(dbcursor.fetchall())
        commits.sort(key=lambda x:x[2])
        dbcursor.execute(releasesql % i)
        releases = list(dbcursor.fetchall())
        releases.sort(key=lambda x:x[1])
        releasesDict = {}
        # 构造{时间：releasename}的字典,releases时间格式是varchar，但commits是datetime。。。疏忽了
        for r in releases:
            releasesDict[r[2].replace(' ','').replace(':','')] = r[1]
        # 对于每个commit
        # print releases
        for c in commits:
            #  commitid，date
            print c[0], c[1], c[2].strftime('%Y%m%d%H%M%S'),
            relatdRelease = redate(c[2].strftime('%Y%m%d%H%M%S'),releasesDict)
            print relatdRelease  # 打印该commit对应的release
            # 如果不为none就入库
            if relatdRelease:
                dbcursor.execute(updatesql % (relatdRelease, c[0], c[1]))
        dbconn.commit()
    dbcursor.close()
    dbconn.close()
