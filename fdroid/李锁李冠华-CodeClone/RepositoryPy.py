#!/usr/bin/python
# -*- coding: UTF-8 -*-

#This is repository insert MySQL program
#Writen by LS in 2017_7_17

import MySQLdb
import sys
import os

#文件信息插入数据库，参数分别为Detection_Id,Repository_Id,Release_Id
def RepositoryInsert(arg1, arg2, arg3) :
        Detection_Id = int(arg1)
        Repository_Id = int(arg2)
        Repository = str(arg3)

        dbconn = None
        con = None

        dbconn = MySQLdb.connect('10.131.252.156','root','root','fdroid')



        #获得Repository路径
	repositorypath = os.path.dirname(Repository)
        #获得Repository名
        repositoryname = os.path.basename(Repository)

	dbcursor = dbconn.cursor()
	sql = "INSERT INTO cc_repository( detection_id,repository_id,repository_addr,repository_name) VALUES (%s,%s,%s,%s)"
        try:
		dbcursor.execute(sql, (Detection_Id,Repository_Id,repositorypath,repositoryname,))
       		dbconn.commit()
        except:
        	dbconn.rollback()

        if dbconn:
                dbconn.close()

        return;

if __name__ == '__main__':
	
	RepositoryInsert(sys.argv[1], sys.argv[2], sys.argv[3]);
