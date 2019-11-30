# -*- coding:utf-8 -*-
'''created by fwk
   2018/03/22
   deprive increment info of each clone of commits
'''
import sys

def parserInstance(filepath):
    '''返回克隆实例，以及groupid的序列'''
    f = open(filepath, 'r')
    r = f.readlines()
    insfrag = [x.split(':')[0]+':'+x.split(':')[1] for x in r]
    insnum = [x.split(':')[-1] for x in r]
    return insfrag, insnum


def parserGroup(filepath):
    '''返回以groupid为key，克隆实例为value的字典'''
    f = open(filepath, 'r')
    r = f.readlines()
    groupdict = {}
    for i in r:
        groupdict[i.split(':')[-1].strip()] = []
    for i in r:
        groupdict[i.split(':')[-1].strip()].append(i.split(':')[0]+':'+i.split(':')[1])
    return groupdict


def compareInst(oldfilepath='1.txt', newfilepath='2.txt'):
    old = parserInstance(oldfilepath)
    if not old[0]:
        return None
    new = parserInstance(newfilepath)
    tem = 0
    increment_Instance = [[],[],[]]
    for i in range(len(old[0])):
        if old[0][i] not in new[0]:
            # print old[0][i],old[1][i].strip(),
            # print 'Removed'
            # record(newfilepath, old[0][i]+' '+old[1][i].strip()+' -Removed\n')
            increment_Instance[0].append(old[1][i].strip())
            increment_Instance[1].append(old[0][i])
            increment_Instance[2].append('-')
            
    for i in range(len(new[0])):
        if new[0][i] not in old[0]:
            # print new[0][i],new[1][i]
            # print new[0][i],
            # print 'Added'
            # record(newfilepath, new[0][i]+' '+new[1][i].strip()+' -Added\n')
            # record(newfilepath, new[0][i]+' -Added\n')
            increment_Instance[0].append(new[1][i].strip())
            increment_Instance[1].append(new[0][i])
            increment_Instance[2].append('+')
    return increment_Instance


def compareGroup(oldfilepath='1.txt', newfilepath='2.txt'):
    maxclass = 0
    with open(newfilepath, 'r') as f:
        lines = f.readlines()
        if lines:
            maxclass = lines[-1].strip().split(':')[-1]
        else:
            maxclass = 0
    oldc = parserGroup(oldfilepath)
    oldi = parserInstance(oldfilepath)
    newc = parserGroup(newfilepath)
    newi = parserInstance(newfilepath)
    increment_Group = [[],[],[]]

    newclassCount = 1
    for k,v in newc.items():
        tem = 0  # 记录有多少个克隆实是上个版本没有的
        for i in v:
            if i not in oldi[0]:
                tem += 1
        if tem == len(v):
            # print k,v
            # print 'New group'
            # record(newfilepath, k+' '+' -Group +dded\n')
            increment_Group[0].append(str(int(maxclass)+newclassCount))
            increment_Group[1].append(v)
            increment_Group[2].append("+")
            newclassCount += 1
        elif tem > 0:
            # print k,v
            # print 'Group updated'
            # record(newfilepath, k+' '+' -Group updated\n')
            increment_Group[0].append(k)
            increment_Group[1].append(v)
            increment_Group[2].append("U")
        else:
            oldg = getGbyI(v[0],oldc)
            if oldg and len(oldg) != len(v):
                # print k,v
                # print 'Group updated'
                # record(newfilepath, k+' '+' -Group updated\n')
                increment_Group[0].append(k)
                increment_Group[1].append(v)
                increment_Group[2].append("U")

    for k,v in oldc.items():
        tem = 0
        for i in v:
            if i not in newi[0]:
                tem += 1
        if tem == len(v):
            # print k,v
            # print 'Group deleted'
            # record(newfilepath, k+' '+' -Group deleted\n')
            increment_Group[0].append(k)
            increment_Group[1].append(v)
            increment_Group[2].append("-")
    return increment_Group


def getGbyI(inst, groupdict):
    for k,v in groupdict.items():
        if inst in v:
            return v
    return None


def record(recordfile, infofrag):
    # 记录更新情况的文件
    f = open('info'+recordfile, 'a')
    f.writelines(infofrag)
    f.close()


def increment_Info(oldfilepath='1.txt', newfilepath='2.txt', filepath='record.txt'):

    increment_Group = compareGroup(oldfilepath, newfilepath)
    increment_Instance = compareInst(oldfilepath, newfilepath)
    if not increment_Instance:
        # indicates there's no inst in old version...abs
        with open(filepath, 'w') as f:
            with open(newfilepath, 'r') as f1:
                for i in f1.readlines():
                    tem = i.split(":")
                    classid = tem[-1].strip()
                    instpath = tem[0]+' '+tem[1] 
                    f.write(classid+' '+instpath+' + +\n')
        return

    # print increment_Group
    # print increment_Instance
    f = open(filepath, 'w')
    for i in range(len(increment_Instance[0])):
        for j in range(len(increment_Group[0])):
            if increment_Instance[1][i] in increment_Group[1][j]:
                if increment_Group[2][j] == 'U':
                    print increment_Group[0][j],increment_Instance[1][i],'U',increment_Instance[2][i]
                    f.write(increment_Group[0][j]+' '+increment_Instance[1][i]+' U '+increment_Instance[2][i])
                    f.write('\n')
                    break
                if increment_Group[2][j] == '+':
                    print increment_Group[0][j],increment_Instance[1][i],'+','+'
                    f.write(increment_Group[0][j]+' '+increment_Instance[1][i]+' +'+' +')
                    f.write('\n')
                    break
                if increment_Group[2][j] == '-':
                    print increment_Group[0][j],increment_Instance[1][i],'-','-'
                    f.write(increment_Group[0][j]+' '+increment_Instance[1][i]+' -'+' -')
                    f.write('\n')
                    break
        # when break,else will not executed
        else:
            print increment_Instance[0][i],increment_Instance[1][i],'U',increment_Instance[2][i]
            f.write(increment_Instance[0][i]+' '+increment_Instance[1][i]+' U '+increment_Instance[2][i])
            f.write('\n')
    f.close()


if __name__ == '__main__':
    argv = sys.argv
    # compareInst(argv[1],argv[2])
    # compareGroup(argv[1],argv[2])
    increment_Info('1.txt','2.txt','record.txt')
    