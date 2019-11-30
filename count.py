# -*- coding:utf-8 -*-
'''created by fwk
   2019/01/04
   To count the code quantoty of codehub.java_rl_class_method_new
'''

import MySQLdb
from collections import Counter
import json

class Stat(object):
    def __init__(self):
        self.lineNum = 0
        self.interfaceNum = 0
        self.funcNum = 0
        self.classSet = set()
        self.releaseSet = set()
        self.repoSet = set()
        self.returnTypeMap = Counter()
        self.dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'codehub')
        self.dbcursor = self.dbconn.cursor()

    def addClass(self, classId):
        self.classSet.add(classId)

    def addRelease(self, releaseName):
        self.releaseSet.add(releaseName)

    def addRepo(self, repoName):
        self.repoSet.add(repoName)

    def closeConn(self):
        self.dbcursor.close()
        self.dbconn.close()


    def countCodeLine(self, start, end):
        
        sql = """SELECT methodid,m.classid,returntype,begin,end,path,isInterface 
        FROM codehub.java_rl_class_method_new as m, codehub.java_rl_class as c 
        where m.classid=c.classid and methodid between {} and {}""".format(start, end)
        print 'exe sql'
        self.dbcursor.execute(sql)
        print 'completed'
        # (0,        1,       2,          3,     4,   5,    6)
        # (methodid, classid, returntype, begin, end, path, ininterface)
        while True:
            r = self.dbcursor.fetchone()
            if not r:
                break
            
            if r[0] % 10000 == 0:
                print "methodid = "+str(r[0]) 
            self.lineNum = self.lineNum + r[4] - r[3]
            self.interfaceNum += r[6]
            if r[4] - r[3]:
                self.funcNum += 1
            self.addClass(r[1])
            self.returnTypeMap[r[2]] += 1
            path = r[5].split('/',3)
            self.addRepo(path[0]+'/'+path[1])
            self.addRelease(path[0]+'/'+path[1]+'/'+path[2])
        
    
if __name__ == "__main__":
    s = Stat()
    for i in range(950):
        s.countCodeLine(i*100000+1,(i+1)*100000)
    s.closeConn()
    print "lineNum=", s.lineNum
    print "interfaceNum", s.interfaceNum
    print "funcNum", s.funcNum
    print "classNum", len(s.classSet)
    print "releaseNum", len(s.releaseSet)
    print "repoNum", len(s.repoSet)
    print "returnTypeNum", len(s.returnTypeMap)
    with open('stat.txt','w') as f:
        json.dump(sorted(s.returnTypeMap.items(), key=lambda x:x[1], reverse=True), f)



