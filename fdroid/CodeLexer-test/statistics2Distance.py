# -*- coding:utf-8 -*-
'''created by fwk
   2018/02/25
   比较code2hash和token2hash的效果
'''
import MySQLdb, getHash, json, lexerparser
import os
from collections import OrderedDict


# 将unicode转化成string
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def code2hash():
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    # sql = 'select block_id,block_code from fdroid.cc_block where detection_id=1 and detection_tp = "20150101--20150131"'
    sql = 'SELECT cc_clonepair.clonepair_id, cc_clonepair.block1_id, \
    cc_clonepair.block2_id from fdroid.cc_clonepair where \
    clonepair_id<3000 and cc_clonepair.detection_tp="20150101--20150131"'

    blocksql = "SELECT block_id, block_code FROM fdroid.cc_block \
        where detection_id=1 and detection_tp = '20150101--20150131' \
        and block_id = %s"
    dbcursor.execute(sql)
    distanceDict = OrderedDict()
    for i in dbcursor.fetchall():
        blockid1 = i[1]
        blockid2 = i[2]
        sql1 = blocksql % blockid1
        sql2 = blocksql % blockid2
        dbcursor.execute(sql1)
        code1 = dbcursor.fetchone()[1].replace(r"\n","").replace(r"\t","").replace(r"b'","").replace(r"',","")
        hash1 = getHash.get_nilsimsa(code1)
        dbcursor.execute(sql2)
        code2 = dbcursor.fetchone()[1].replace(r"\n","").replace(r"\t","").replace(r"b'","").replace(r"',","")
        hash2 = getHash.get_nilsimsa(code2)
        dist = getHash.compare_hash(hash1,hash2)
        print i[0]
        if distanceDict.has_key(dist):
            distanceDict[dist] += 1
        else:
            distanceDict[dist] = 1
    dbcursor.close()
    dbconn.close()
    return distanceDict


def token2hash():
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    # sql = 'select block_id,block_code from fdroid.cc_block where detection_id=1 and detection_tp = "20150101--20150131"'
    sql = 'SELECT cc_clonepair.clonepair_id, cc_clonepair.block1_id, \
    cc_clonepair.block2_id from fdroid.cc_clonepair where \
    clonepair_id<3000 and cc_clonepair.detection_tp="20150101--20150131"'

    blocksql = "SELECT block_id, block_code FROM fdroid.cc_block \
        where detection_id=1 and detection_tp = '20150101--20150131' \
        and block_id = %s"
    dbcursor.execute(sql)
    distanceDict = OrderedDict()
    for i in dbcursor.fetchall():
        blockid1 = i[1]
        blockid2 = i[2]
        sql1 = blocksql % blockid1
        sql2 = blocksql % blockid2

        dbcursor.execute(sql1)
        code1 = dbcursor.fetchone()[1].replace(r"\n","").replace(r"\t","").replace(r"b'","").replace(r"',","")
        with open('lexer/tem.code', 'w') as f:
            f.write(code1)
        os.popen('java -jar codeLexer.jar lexer/tem.code')
        token1 = lexerparser.parse()
        hash1 = getHash.get_nilsimsa(token1)

        dbcursor.execute(sql2)
        code2 = dbcursor.fetchone()[1].replace(r"\n","").replace(r"\t","").replace(r"b'","").replace(r"',","")
        with open('lexer/tem.code', 'w') as f:
            f.write(code2)
        os.popen('java -jar codeLexer.jar lexer/tem.code')
        token2 = lexerparser.parse()
        hash2 = getHash.get_nilsimsa(token2)

        dist = getHash.compare_hash(hash1,hash2)

        print i[0]
        if distanceDict.has_key(dist):
            distanceDict[dist] += 1
        else:
            distanceDict[dist] = 1
    dbcursor.close()
    dbconn.close()
    return distanceDict


if __name__ == '__main__':
    f = open('lexer/CodeDistanceDict.pkl','w')
    json.dump(code2hash(), f)
    f.close()
    f = open('lexer/CodeDistanceDict.pkl','r')
    d = json.load(f)
    print byteify(d)

    f = open('lexer/tokenDistanceDict.pkl','w')
    json.dump(token2hash(), f)
    f.close()
    f = open('lexer/tokenDistanceDict.pkl','r')
    d = json.load(f)
    print byteify(d)




