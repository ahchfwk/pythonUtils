#!/usr/bin/env python

import os
import commands
import MySQLdb
import PairToClass
import getCodeFragment


def getdirSize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    size = size/1000/1000
    return size


def copyJavaFile(dir, des):
    for root, dirs, files in os.walk(dir):
        for f in files:
            if f[-4:] == "java":
                os.popen("cp "+os.path.join(root, f)+" "+des)


def getPathFromId(release_id):
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'codehub')
    dbcursor = dbconn.cursor()
    sql = "select local_addr from releases where id=%s" % release_id
    dbcursor.execute(sql)
    result = dbcursor.fetchone()
    path = "/home/fdse/data/releases"+str(release_id/10000+1)+"_unzip"+result[0][8:-4]
    dbcursor.close()
    dbconn.close()
    return path


def detect(dirPath):
    print dirPath
    # os.popen("cp -r "+dirPath+" /home/fdse/fwk/SourcererCC/clone-detector/input/dataset/")
    copyJavaFile(dirPath, "/home/fdse/fwk/SourcererCC/clone-detector/input/dataset/")
    if getdirSize("/home/fdse/fwk/SourcererCC/clone-detector/input/dataset/")>8:
        print "---------------------------------too large"
        return [],[]
    commands.getstatusoutput("./SourCC.sh")
    # list of "path,start,end"
    paths = [] 
    with open("input/bookkeping/headers.file", "r") as f:
        for i in f.readlines():
            headers = i.strip().split(",")
            paths.append("/".join(dirPath.split("/")[:-1]) + headers[1][55:]+","+headers[2]+","+headers[3])
    # print paths

    # list of clone group
    result = []
    with open("output9.0/tokensclones_index_WITH_FILTER.txt", "r") as g:
        data = []
        for i in g.readlines():
            data.append(set(i.strip().split(",")))
        result = PairToClass.pairToGroup2(data)
    result = [list(x) for x in result]
    return paths, result


def getSimHash(code):
    with open("code.txt", "w") as f:
        f.write(code)
    os.popen("java -jar codeToHash.jar")
    with open("simhash.txt", "r") as g:
        return g.readline()


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
    sql = """INSERT INTO cc_cloneBlock (clone_id,release_id,block_id,path,start,end,code,simhash) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    clone_id = 1
    if clones:
        for clone in clones:
            for block_id in clone:
                tem = paths[int(block_id)].split(",")
                
                path = tem[0]
                start = int(tem[1])
                end = int(tem[2])
                code = getCodeFragment.getCodeFrag("/home/fdse/fwk/SourcererCC/clone-detector/input/dataset/"+path.split("/")[-1], start, end).replace("'","''").replace('\\', '\\\\')
                simhash = getSimHash(code)
                try:
                    dbcursor.execute(sql, (clone_id, release_id, block_id, path, start, end, code, simhash))
                except:
                    dbconn.rollback()
                    print "cloneBlock2DB failed......"
            dbconn.commit()
    dbcursor.close()
    dbconn.close()


def clear():
    os.popen("./clear.sh")


if __name__ == "__main__":
    for i in range(111,112):
        print i
        print "before clear"
        clear()
        try:
            paths,clones = detect(getPathFromId(i))
            print paths,"---------\n",clones
            if not clones:
                print "+++++++++++++No result"
            # cloneGroup2DB(clones, i)
            # block2DB(clones, paths, i)
        except Exception as e:
            print e.message
        clear()
        print "end clear"
