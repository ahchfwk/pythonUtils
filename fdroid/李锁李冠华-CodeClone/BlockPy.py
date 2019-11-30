#!/usr/bin/python
# -*- coding: UTF-8 -*-

#This is clone block insert MySQL program
#Writen by LS in 2017_7_19

import MySQLdb
import sys
import os

def BlockInsert(arg1, arg2, arg3, arg4) :
        Detection_Id = int(arg1)
        Repository_Id = int(arg2)
        Release_Id = int(arg3)
	PreAddr = str(arg4)

        fhand = open ('/mnt/winE/SourcererCC/clone-detector/input/bookkeping/headers.file','r')
        fields = []
        dbconn = None
        con = None

        dbconn = MySQLdb.connect('10.131.252.156','root','root','fdroid')
        #print 'connect MySQL !'

        for line in fhand:
                block = line.split(',')
                length = int(block[3]) - int(block[2])
                ccaddr = str(block[1])
		addr = PreAddr + ccaddr[50:]
                begin = int(block[2])
                end = int(block[3])
                Block_Id = int(block[0])
                dbcursor = dbconn.cursor()
                sql = "INSERT INTO cc_block( detection_id,repository_id,release_id,block_id,block_addr,block_begin,block_end,block_length) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                try:
                        dbcursor.execute(sql, (Detection_Id,Repository_Id,Release_Id,Block_Id,addr,begin,end,length,))
                        dbconn.commit()
                except:
                        dbconn.rollback()

        if dbconn:
                dbconn.close()

        return;

if __name__ == '__main__':

        BlockInsert(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]);

