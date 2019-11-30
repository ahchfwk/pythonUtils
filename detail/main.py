####################################
# clone group info To json
# author niko -*- date 07-26-2018
####################################

import sys
sys.path.append(r"C:\Users\niko\Desktop\功能代码\读取codehub数据库python\detail")
import sql.sqlBuilder as DB
import simplejson as json
import info.releaseInfo as INFO
import tasks.listProjectInCCDB as LP
import tasks.operateGenealogy as OG
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
    projectAddrList = LP.getProjectList(dbcursor, 1)
