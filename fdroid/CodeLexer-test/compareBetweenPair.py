# -*- coding:utf-8 -*-
'''created by fwk
   2018/01/30
   比较token2hash和code2hash的跨度是否均匀
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


def compare_betweenPair(num):
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    # sql = 'select block_id,block_code from fdroid.cc_block where detection_id=1 and detection_tp = "20150101--20150131"'
    sql = 'SELECT distinct cc_clonepair.block1_id \
    from fdroid.cc_clonepair where \
    clonepair_id<%s and cc_clonepair.detection_tp="20150101--20150131"' % num

    blocksql = "SELECT block_id, block_code FROM fdroid.cc_block \
        where detection_id=1 and detection_tp = '20150101--20150131' \
        and block_id = %s"
    dbcursor.execute(sql)
    SourceCodedistanceDict = OrderedDict()
    CodeTokendistanceDict = OrderedDict()
    tem = dbcursor.fetchall()
    
    for i in range(len(tem)-1):
        print i
        blockid1 = tem[i][0]
        blockid2 = tem[i+1][0]
        sql1 = blocksql % blockid1
        sql2 = blocksql % blockid2

        dbcursor.execute(sql1)
        code1 = dbcursor.fetchone()[1].replace(r"\n","").replace(r"\t","").replace(r"b'","").replace(r"',","")
        hash1 = getHash.get_nilsimsa(code1)
        with open('lexer/tem.code', 'w') as f:
            f.write(code1)
        os.popen('java -jar codeLexer.jar lexer/tem.code')
        token1 = lexerparser.parse()

        dbcursor.execute(sql2)
        code2 = dbcursor.fetchone()[1].replace(r"\n","").replace(r"\t","").replace(r"b'","").replace(r"',","")
        hash2 = getHash.get_nilsimsa(code2)
        with open('lexer/tem.code', 'w') as f:
            f.write(code2)
        os.popen('java -jar codeLexer.jar lexer/tem.code')
        token2 = lexerparser.parse()

        dist = getHash.compare_hash(hash1,hash2)
        if SourceCodedistanceDict.has_key(dist):
            SourceCodedistanceDict[dist] += 1
        else:
            SourceCodedistanceDict[dist] = 1
        
        dist = getHash.compare_hash(getHash.get_nilsimsa(token1),getHash.get_nilsimsa(token2))
        
        # print code1
        # print code2
        # print token1,token2
        
        if CodeTokendistanceDict.has_key(dist):
            CodeTokendistanceDict[dist] += 1
        else:
            CodeTokendistanceDict[dist] = 1

    dbcursor.close()
    dbconn.close()
    return SourceCodedistanceDict, CodeTokendistanceDict


if __name__ == '__main__':
    
    a,b = compare_betweenPair(1000)
    f = open('lexer/betweenCodeDistanceDict.pkl','w')
    json.dump(a, f)
    f.close()
    f = open('lexer/betweenCodeDistanceDict.pkl','r')
    d = json.load(f)
    print byteify(d)

    f = open('lexer/betweenTokenDistanceDict.pkl','w')
    json.dump(b, f)
    f.close()
    f = open('lexer/betweenTokenDistanceDict.pkl','r')
    d = json.load(f)
    print byteify(d)





