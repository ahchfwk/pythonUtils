#!/usr/bin/python
# -*- coding: UTF-8 -*-

#This is clone pairs insert
#Writen by LS in 2017_6_28

import MySQLdb
import sys
import os

Detection_Id = int(1)
Release_Id = int(1)
Clonepair_Id = 0


fhand = open ('/mnt/winE/SourcererCC/clone-detector/output8.0/tokensclones_index_WITH_FILTER.txt','r')
dbconn = None
con = None

dbconn = MySQLdb.connect('10.131.252.156','root','root','fdroid')
print 'connect MySQL !'

for line in fhand:
        block = line.split(',')
        begin = int(block[0])
        end = int(block[1])
	Clonepair_Id = Clonepair_Id + 1
	#print 'Block: ' begin ,end
       
        dbcursor = dbconn.cursor()
        sql = "INSERT INTO cc_clonepairs( detection_id,clonepair_id,release_id,block_id1,block_id2) VALUES (%s,%s,%s,%s,%s)"
        try:
                dbcursor.execute(sql, (Detection_Id,Clonepair_Id,Release_Id,begin,end,))
                dbconn.commit()
        except:
                dbconn.rollback()


with dbconn:
        cur = dbconn.cursor()
        aa = cur.execute("SELECT * FROM cc_clonepairs")
        print aa

        info = cur.fetchmany(aa)
        for i in info:
                print i
        cur.close()
        dbconn.commit()

if dbconn:
        dbconn.close()

