####################################
# clone group info To json
# author niko -*- date 07-26-2018
####################################

import sys
sys.path.append(r"C:\Users\niko\Desktop\功能代码\读取codehub数据库python\detail")
import sql.sqlBuilder as DB
import simplejson as json
import info.releaseInfo as INFO
import listProjectInCCDB as LP
import operateGenealogyII as OG
import pymysql
import config


def connectDatabase():
    conn = pymysql.connect(host = config.HOST, port = config.PORT, user = config.USER, passwd = config.PASSWORD, db = config.DATABASE)
    dbcursor = conn.cursor()
    if(dbcursor == None):
        raise("db connection failed!")
    return dbcursor
    
def getDataFromDB(dbcursor, sql):
    results = {}
    try:
        dbcursor.execute(sql)
        results = dbcursor.fetchall()
    except dbcursor.Error as e:
        print(e)
        conn.rollback()

    return results
                

if __name__ == '__main__':
    dbcursor = connectDatabase()
    f = open("startID.txt", "r")
    startID = f.read()
    f.close()
    while(True):
        print("======================================================")
        print("current data id:" + startID)
        projectAddrList, startID = LP.getProjectList(dbcursor, startID)
        print("current project list:\n", projectAddrList)
        for i in range(len(projectAddrList)):
            OG.genealogyWriteToFile(dbcursor, projectAddrList[i])
            f = open("startID.txt", "w")
            f.write(str(startID))
            f.close()
    
    
