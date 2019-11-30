# -*- coding: utf-8 -*-
'''created by fwk
   2018/02/26
   测试ccfx检测的克隆对转化为token的nilsimsa是否dist为0
'''
import getHash
import lexerparser
import os

def getCodeFrag(sourceFilePath, start, end):
    f = open(sourceFilePath, 'r')
    sourceCode = f.readlines()
    f.close()
    tem = ''
    for i in sourceCode:
        tem = tem + i.replace('\n', '\r\n')
    sourceCode = tem
    return sourceCode[int(start):int(end) + 1]


if __name__ == '__main__':
    f = open("../a.txt")
    lines = f.readlines()
    f.close()
    for i in range(len(lines) - 1):
        line1 = lines[i]
        line2 = lines[i + 1]
        class1 = line1.split(":")[-1]
        class2 = line2.split(":")[-1]
        if class1 == class2:
            code1 = getCodeFrag("." + line1.split(":")[0], line1.split(
                ":")[1].split(",")[0], line1.split(":")[1].split(",")[1])
            code2 = getCodeFrag("." + line2.split(":")[0], line2.split(
                ":")[1].split(",")[0], line2.split(":")[1].split(",")[1])
            
            with open('lexer/tem.code', 'w') as f:
                f.write(code1)
            os.popen('java -jar codeLexer.jar lexer/tem.code')
            token1 = lexerparser.parse()
            hash1 = getHash.get_nilsimsa(token1)
            
            with open('lexer/tem.code', 'w') as f:
                f.write(code2)
            os.popen('java -jar codeLexer.jar lexer/tem.code')
            token2 = lexerparser.parse()
            hash2 = getHash.get_nilsimsa(token2)
            print class1, class2, '-------------->', getHash.compare_hash(hash1, hash2)
            if getHash.compare_hash(hash1, hash2):
                print code1,'------------------------------------------------'
                print code2
