# -*- coding:utf-8 -*-
'''created by fwk
   2018/4/10
   relate release and commit by time
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


def relate():
    repoIdSql = """SELECT distinct repository_id FROM codehub.releases where is_artificial=0 and 
    repository_id in (select distinct repository_id from codehub.commits )"""
    commitsSql = """SELECT id, commit_date, sha FROM codehub.commits where repository_id = %s"""
    releaseSQL = """SELECT id, created_at FROM codehub.releases where repository_id = %s"""
    insertSQL = """insert into tmp_commit_tobe_clonedetect values (%s,%s,"%s",%s);"""
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'codehub')
    dbcursor = dbconn.cursor()
    dbcursor.execute(repoIdSql)
    repoIds = [x[0] for x in dbcursor.fetchall()]
    count = 1
    for repoid in repoIds:
        dbcursor.execute(commitsSql % repoid)
        commits = dbcursor.fetchall()
        dbcursor.execute(releaseSQL % repoid)
        releases = dbcursor.fetchall()
        releaseDict = {}
        for r in releases:
            releaseDict[r[1].strftime('%Y%m%d%H%M%S')] = r[0]
        print "-----------------%s------------------" % count
        count += 1
        # print releaseDict
        for c in commits:
            # id from commit, repository_id, commit_sha, releated release
            related_release = redate(c[1].strftime('%Y%m%d%H%M%S'), releaseDict)
            print repoid, c[0], c[2], related_release
            if related_release:
                dbcursor.execute(insertSQL % (repoid, c[0], c[2], related_release))
        dbconn.commit()
    dbcursor.close()
    dbconn.close()


if __name__ == "__main__":
    relate()
