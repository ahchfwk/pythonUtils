#!/usr/bin/env python

import os
import commands
import MySQLdb
import getCodeFragment
import xmlParser


def getPathFromId(release_id):
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'codehub')
    dbcursor = dbconn.cursor()
    sql = "select local_addr from releases where id=%s" % release_id
    dbcursor.execute(sql)
    result = dbcursor.fetchone()
    path = "/home/fdse/data/releases"+str(release_id/10000+1)+"_unzip"+result[0][8:-4]
    dbcursor.close()
    dbconn.close()
    path = path if os.path.exists(path) else None
    return path


# def getSimHash(code):
#     with open("code.txt", "w") as f:
#         f.write(code)
#     os.popen("java -jar codeToHash.jar")
#     with open("simhash.txt", "r") as g:
#         return g.readline()


def detect(dirpath):
    print dirpath
    if not dirpath:
        return [],[]
    pj = dirpath.strip().split("/")[-1]
    directory = "/".join(dirpath.strip().split("/")[:-1])
    status, out = commands.getstatusoutput("./run.sh %s %s" % (dirpath,pj))
    pj = dirpath.strip().split("/")[-1]
    os.chdir("/home/fdse/fwk/nicad/NiCad-4.0")
    if not os.path.exists("detectResult/%s_functions-clones-0.30-classes.xml" % pj):
        return [],[]
    result = xmlParser.parseXml("detectResult/%s_functions-clones-0.30-classes.xml" % pj)
    if not result:
        return [],[]
    os.popen("rm detectResult/*")
    paths = []
    clones = []
    insid = 0
    for group in result.values():
        p = []
        g = []
        for i in group:
            g.append(insid)
            insid += 1
            paths.append(directory+"/"+i.path+","+i.start+","+i.end)
        clones.append(g[:])
    return paths, clones


def cloneGroup2DB(clones, release_id):
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'codehub')
    dbcursor = dbconn.cursor()
    sql = """INSERT INTO cc_cloneGroup (clone_id,release_id,block_id,group_id) VALUES (%s,%s,%s,%s)"""
    clone_id = 1
    if clones:
        for group_id,clone in enumerate(clones):
            for block_id in clone:
                try:
                    dbcursor.execute(sql, (clone_id, release_id, block_id, group_id))
                except:
                    dbconn.rollback()
                    print "cloneGroup2DB failed......"
            dbconn.commit()
    dbcursor.close()
    dbconn.close()


def block2DB(clones, paths, release_id):
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'codehub')
    dbcursor = dbconn.cursor()
    sql = """INSERT INTO cc_cloneBlock (clone_id,release_id,block_id,path,start,end) VALUES (%s,%s,%s,%s,%s,%s)"""
    clone_id = 1
    if clones:
        for clone in clones:
            for block_id in clone:
                tem = paths[int(block_id)].split(",")
                
                path = tem[0]
                start = int(tem[1])
                end = int(tem[2])
                # code = getCodeFragment.getCodeFrag(path, start, end).replace("'","''").replace('\\', '\\\\')
                # simhash = getSimHash(code)
                try:
                    # dbcursor.execute(sql, (clone_id, release_id, block_id, path, start, end, code, simhash))
                    dbcursor.execute(sql, (clone_id, release_id, block_id, path, start, end))
                except Exception as e:
                    dbconn.rollback()
                    print "cloneBlock2DB failed......"
                    print repr(e)
            dbconn.commit()
    dbcursor.close()
    dbconn.close()


if __name__ == '__main__':
    for i in range(270,20000):
        print i
        
        paths,clones = detect(getPathFromId(i))
        if not clones:
            print "+++++++++++++ No result ++++++++++++"
        cloneGroup2DB(clones, i)
        block2DB(clones, paths, i)
        

    
