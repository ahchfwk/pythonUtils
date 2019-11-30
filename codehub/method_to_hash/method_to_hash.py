'''created by fwk
   2018/4/12
   extract method and generate hash,simhash for it and its token
'''

import os
import hashlib
import lexerparser
import getSimHash
import MySQLdb


def extract_method(parentPath, releasePath, resultPath):
    os.popen('java -jar method_analyze-0.0.1-SNAPSHOT.jar %s %s %s' % (parentPath, releasePath, resultPath))


def str2md5(codeBody):
    md5 = hashlib.md5()
    md5.update(codeBody)
    return md5.hexdigest()

def str2sha1(codeBody):
    sha1 = hashlib.sha1()
    sha1.update(codeBody)
    return sha1.hexdigest()


def str2simhash(codeBody):
    return getSimHash.get_nilsimsa(codeBody)


def token2md5(codeBody):
    with open('lexer/tem.code', 'w') as f:
        f.write(codeBody)
    os.popen('java -jar codeLexer.jar lexer/tem.code')
    token = lexerparser.parse()
    md5 = hashlib.md5()
    md5.update(token)
    return md5.hexdigest()


def token2sha1():
    os.popen('java -jar codeLexer.jar result/1.txt')
    token = lexerparser.parse()
    sha1 = hashlib.sha1()
    sha1.update(token)
    return sha1.hexdigest()


def token2simhash():
    token = lexerparser.parse()
    return getSimHash.get_nilsimsa(token)


def getmethod(startid, endid):
    sql = """SELECT m.methodid, c.path, c.classname, m.methodsignature from java_rl_class as c, 
    java_rl_class_method as m where c.classid = m.classid and m.methodid between %d and %d""" % (startid, endid)
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'codehub')
    dbcursor = dbconn.cursor()
    dbcursor.execute(sql)
    result = dbcursor.fetchall()
    dbcursor.close()
    dbconn.close()
    return result


def methodId2body(filepath, className, methodsignature):
    os.popen('java -jar method_analyze-0.0.2-SNAPSHOT.jar %s %s "%s"' % (filepath, className, methodsignature))
    with open('result/1.txt', 'r') as f:
        x = f.read()
    return x


if __name__ == "__main__":
    # parentPath = 'C:\\Users\\fwk\Desktop\\py\\codehub\\releases\\'
    # resultPath = 'C:\\Users\\fwk\Desktop\\py\\codehub\\method_to_hash\\methods\\'
    # releasePaths = os.listdir('../releases/')
    # for path in releasePaths:
    #     extract_method(parentPath, path, resultPath)
    # print str2md5('public static void main(){}')
    # print str2sha1('public static void main(){}')
    # print str2simhash('public static void main(){}')
    # print token2md5('public static void main(){}')
    # print token2sha1()
    # print token2simhash()

    # hashfilepath = './hash.txt'
    # projs = os.listdir('methods')
    # for pj in projs:
    #     print pj
    #     funcs = os.listdir('methods/'+pj)
    #     hashfile = open(hashfilepath, 'a')
    #     for f in funcs:
    #         fun = open('methods/'+pj+'/'+f, 'r')
    #         result = fun.readlines()
    #         fun.close()
    #         if len(result) > 2:
    #             funpath = result[0].strip()
    #             funsign = result[1].strip()
    #             funbody = ''.join(result[2:])
    #             hashfile.writelines(funpath+','+funsign+','+str2hash(funbody)+','+str2simhash(funbody)+','+token2hash(funbody)+','+token2simhash()+'\n')
    #     hashfile.close()
    
    for i in range(9):
        startid = i*1000000+1
        endid = (i+1)*1000000
        f = open('hash'+str(i)+'.txt', 'a')
        methods = getmethod(startid, endid)
        for m in methods[528533:600000]:
            code = methodId2body(m[1], m[2], m[3])
            sha1 = str2sha1(code)
            simhash = str2simhash(code)
            tokensha1 = token2sha1()
            tokenSimhash = token2simhash()
            print m[0], sha1, simhash, tokensha1, tokenSimhash
            line = "%s,%s,%s,%s,%s\n" % (m[0], sha1, simhash, tokensha1, tokenSimhash)
            f.writelines(line)
        f.close()
    