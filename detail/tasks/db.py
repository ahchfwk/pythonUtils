####################################
# DB connect for other module
# author niko -*- date 08-14-2018
####################################

import sys
sys.path.append(r"C:\Users\niko\Desktop\功能代码\读取codehub数据库python\detail")
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

    
    return results
