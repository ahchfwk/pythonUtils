####################################
# get project list which already into Code Clone DB
# author niko -*- date 08-13-2018
####################################

import sys
sys.path.append(r"C:\Users\niko\Desktop\功能代码\读取codehub数据库python\detail")
import pymysql
import config
import sql.sqlBuilder as SqlBui
import db


def getProjectList(dbcursor, startID):
    print("get repo id list")
    sqlForRepoID = SqlBui.getRepoIdBatch(startID, 5)
    repoID = db.getDataFromDB(dbcursor, sqlForRepoID)
    projectAddrList = []
    for id in repoID:
        if(id[0] > 0):
            sqlForProjectAddr = SqlBui.getCurProjectAddrInCCDB(id[0])
            addr = db.getDataFromDB(dbcursor, sqlForProjectAddr)
            if(len(addr) > 0):
                projectAddrList.append(addr[0][0])
            
    nextStartId = int(startID) + 5
    return projectAddrList, str(nextStartId)

if __name__=='__main__':
    dbcursor = db.connectDatabase()
    print(getProjectList(dbcursor, 10))
