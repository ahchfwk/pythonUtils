# -*- coding:utf-8 -*-
'''created by fwk
   2017/12/13
   to transform the tokenblock to clone fragment
'''
import sys


def getCodeFrag(sourceFilePath, start, end):
    f = open(sourceFilePath, 'r')
    sourceCode = f.readlines()
    f.close()
    tem = ''
    for i in sourceCode:
        tem = tem + i.replace('\n', '\r\n')
    sourceCode = tem
    return sourceCode[int(start):int(end) + 1]


def printCloneClass(resultFilePath, cid):
    f = open(resultFilePath, 'r')
    f.seek(-200, 2)
    lines = f.readlines()
    if len(lines) >= 2:
        if int(lines[-1].split(':')[-1]) > cid:
            f.seek(0)
            lines = f.readlines()
            print 'cloneClass %s:' % cid
            count = 0
            for i in lines:
                if int(i.split(':')[-1]) == cid:
                    count += 1
                    tem = i.split(':')
                    out1 = '----------clone instance '+str(count)+100*'-'
                    out2 = '----------from file: '+i.split(':')[0].split('\\')[-1]+100*'-'
                    print out1[:70]
                    print out2[:70]
                    print getCodeFrag(tem[0], tem[1].split(',')[0], tem[1].split(',')[1])
        else:
            print '克隆类id的范围在0到'+lines[-1].split(':')[-1]
    else:
        print 'zhe ......'


def getCloneClass(resultFilePath, cid):
    f = open(resultFilePath, 'r')
    f.seek(-200, 2)
    lines = f.readlines()
    cloneClass = []
    if len(lines) >= 2:
        if int(lines[-1].split(':')[-1]) > cid:
            f.seek(0)
            lines = f.readlines()
            count = 0
            for i in lines:
                if int(i.split(':')[-1]) == cid:
                    count += 1
                    tem = i.split(':')
                    cloneClass.append(getCodeFrag(tem[0], tem[1].split(',')[0], tem[1].split(',')[1]))
            return cloneClass
        else:
            print '克隆类id的范围在0到'+lines[-1].split(':')[-1]
    else:
        print 'zhe ......'

if __name__ == '__main__':
    # arg = sys.argv[1]
    # arg = arg.split(':')
    # path = arg[0]
    # starts = arg[1].split(',')[0]
    # ends = arg[1].split(',')[1]
    # print getCodeFrag(path, starts, ends)

    print getCloneClass('1.2.txt', 38)
