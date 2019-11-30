#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import MySQLdb
from PairToClass import toDict
from PairToClass import pairToClass

DBconfig=('10.131.252.156','root','root','fdroid')
SourcererContext='/mnt/winE/SourcererCC/clone-detector/output8.0/tokensclones_index_WITH_FILTER.txt'

def PairInsert(arg1, arg2, arg3):
    Detection_Id = int(arg1)
    Repository_Id = int(arg2)
    Release_Id = int(arg3)
    Clonepair_Id = 0

    fhand = open(SourcererContext)
    dbconn = None
    con = None

    dbconn = MySQLdb.connect(*DBconfig)
    prilist = []

    for line in fhand:
        block = line.split(',')
        begin = int(block[0])
        end = int(block[1])
        #print 'Block: ' begin ,end
        prilist.append([begin,end])

    result = pairToClass(toDict(prilist))
    Group_id = 0
    for cloneList in result:
        Group_idlist = ','.join(str(x) for x in cloneList)
        Group_id += 1
        dbcursor = dbconn.cursor()
        sql1 = "INSERT INTO cc_group(detection_id,repository_id,release_id,group_id,group_idlist) VALUES (%s,%s,%s,%s,%s)"
        sql2 = "INSERT INTO cc_classinstance(detection_id,repository_id,release_id,group_id,block_id) VALUES (%s,%s,%s,%s,%s)"
        try:
            dbcursor.execute(sql1, (Detection_Id, Repository_Id, Release_Id, Group_id, Group_idlist))
            for x in cloneList:
                dbcursor.execute(sql2,(Detection_Id, Repository_Id, Release_Id, Group_id, x))
            dbconn.commit()
        except:
            dbconn.rollback()
            print 'db write defeat and roll back'

    if dbconn:
        dbconn.close()

	print 'pairToGroup start:'






	return;

if __name__ == '__main__':
        block = []
	count = 0
        #for i in range(1, len(sys.argv)):
        #       block[count] = sys.argv[i]
	#	count = count + 1

        PairInsert(sys.argv[1], sys.argv[2], sys.argv[3]);




