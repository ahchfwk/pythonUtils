#!/usr/bin/python
# -*- coding: UTF-8 -*-

#This is clone all information insert MySQL program
#Writen by LS in 2017_7_3

import MySQLdb
import sys
import os

"""
#文件信息插入数据库，参数分别为Detection_Id,Repository_Id,Release_Id
def FileInsert(arg1, arg2, arg3) :
	Detection_Id = int(arg1)
	Repository_Id = int(arg2)
	Release_Id = int(arg3)

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
		filefull = str(block[1])
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


def BlockInsert(arg1, arg2, arg3) :
	Detection_Id = int(arg1)
	Repository_Id = int(arg2)
	Release_Id = int(arg3)

	fhand = open ('/mnt/winE/SourcererCC/clone-detector/input/bookkeping/headers.file','r')
	fields = []
	dbconn = None
	con = None

	dbconn = MySQLdb.connect('10.131.252.156','root','root','fdroid')
	#print 'connect MySQL !'

	for line in fhand:
		block = line.split(',')
		length = int(block[3]) - int(block[2])
		addr = str(block[1])
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
"""
def PairInsert(arg1, arg2, arg3) :
	Detection_Id = int(arg1)
	Repository_Id = int(arg2)
	Release_Id = int(arg3)
	Clonepair_Id = 0

	fhand = open ('/mnt/winE/SourcererCC/clone-detector/output8.0/tokensclones_index_WITH_FILTER.txt','r')
	dbconn = None
	con = None

	dbconn = MySQLdb.connect('10.131.252.156','root','root','fdroid')
	#print 'connect MySQL !'

	for line in fhand:
		block = line.split(',')
		begin = int(block[0])
		end = int(block[1])
		Clonepair_Id = Clonepair_Id + 1
		#print 'Block: ' begin ,end

		dbcursor = dbconn.cursor()
		sql = "INSERT INTO cc_clonepair( detection_id,repository_id,release_id,clonepair_id,block_id1,block_id2) VALUES (%s,%s,%s,%s,%s,%s)"
		try:
			dbcursor.execute(sql, (Detection_Id,Repository_Id,Release_Id,Clonepair_Id,begin,end,))
			dbconn.commit()
		except:
			dbconn.rollback()

	if dbconn:
		dbconn.close()

	return;

def DetectionInsert(arg0,arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9) :
	#转换数据类型
	Detection_Id = int(arg0)
	Repository_Id = int(arg1)
	Release_Id = int(arg2)
	Detection_Granularity =str(arg3)
	Detection_Percent = float(arg4)
	Detection_date = str(arg5)
	Detection_Time = int(arg6)
	Detection_TimeOfToken = int(arg7)
	Detection_TimeOfIndexing = int(arg8)
	Detection_TimeOfClone = int(arg9)

	print 'Clone Time Get:',Detection_Time

	dbconn = MySQLdb.connect('10.131.252.156','root','root','fdroid')
	dbcursor = dbconn.cursor()
	sql = "INSERT INTO cc_detection( detection_id,repository_id,release_id,detection_granularity,detection_percent,detection_date,detection_time,detection_timeoftoken,detection_timeofindexing,detection_timeofclone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

	#print 'sql get!'
	try:
		dbcursor.execute(sql, (Detection_Id,Repository_Id,Release_Id,Detection_Granularity,Detection_Percent,Detection_date,Detection_Time,Detection_TimeOfToken,Detection_TimeOfIndexing,Detection_TimeOfClone,))
		dbconn.commit()
	except:
		dbconn.rollback()

	if dbconn:
		dbconn.close()

	return;


fhand = open ('/mnt/winE/SourcererCC/clone-detector/Detection.txt','r')
#dbconn = None
#con = None

#dbconn = MySQLdb.connect('10.131.252.156','root','root','fdroid')
#print 'connect MySQL !'

block = []
count = 0
for line in fhand.readlines():
	line = line.strip()
	block.append(line)
	count = count + 1
'''
print block[5]
print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
print len(block)
print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
'''
DetectionInsert(block[0],block[1],block[2],block[3],block[4],block[5],block[6],block[7],block[8],block[9]);

#FileInsert(block[0], block[1], block[2]);

#BlockInsert(block[0], block[1], block[2]);

PairInsert(block[0], block[1], block[2]);
'''
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
print "The release insert MySQL !"
print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
#if dbconn:
#	dbconn.close()




#if __name__ == "__main__":
#	sys.exit(main())
'''
