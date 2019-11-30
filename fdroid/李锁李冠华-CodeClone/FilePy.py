#!/usr/bin/python
# -*- coding: UTF-8 -*-

#This is clone file insert MySQL program
#Writen by LS in 2017_7_3 And modify in 2017_7_19 

import MySQLdb
import sys
import os

#文件信息插入数据库，参数分别为Detection_Id,Repository_Id,Release_Id
def FileInsert(arg1, arg2, arg3, arg4) :
        Detection_Id = int(arg1)
        Repository_Id = int(arg2)
        Release_Id = int(arg3)
	PreAddr = str(arg4)

        fhand = open ('/mnt/winE/SourcererCC/clone-detector/input/bookkeping/headers.file','r')
        files = []
        dbconn = None
        con = None

        dbconn = MySQLdb.connect('10.131.252.156','root','root','fdroid')
        #print 'connect MySQL !'

        count = 0

        for line in fhand:
                block = line.split(',')

                #获得包含文件路径和文件名的字符串
                oldFileAddr = str(block[1])
		filefull = PreAddr + oldFileAddr[50:]
                #获得文件路径
                filepath = os.path.dirname(filefull)
                #获得文件名
                filename = os.path.basename(filefull)

                #判断文件是否已在列表中
                if filename not in files:
                        files.append(filepath)
                        files.append(filename)

                        Index = 2*count
                        File_Id = int(count)
                        File_Addr = files[Index]
                        File_Name = files[Index + 1]

                        count = count + 1

                        dbcursor = dbconn.cursor()
                        sql = "INSERT INTO cc_file( detection_id,repository_id,release_id,file_id,file_addr,file_name) VALUES (%s,%s,%s,%s,%s,%s)"
			try:
                                dbcursor.execute(sql, (Detection_Id,Repository_Id,Release_Id,File_Id,File_Addr,File_Name,))
                                dbconn.commit()
                        except:
                                dbconn.rollback()

        if dbconn:
                dbconn.close()

        return;

if __name__ == '__main__':

        FileInsert(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]);

