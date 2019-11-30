# -*- coding:utf-8 -*-
'''created by fwk
   2018/02/28
   group clones by simhash
'''
def groupAll(data, threshold, result, distfun):
    subResult = []
    
    if not data:
        pass
    else:
        head = data[0]
        for i in data:
            tag = 1
            if distfun(i,head) <= threshold:
                # 判断与已存在的结果是否距离都小于阈值
                for j in subResult:
                    if distfun(i,j) > threshold:
                        tag = 0
                        break
                if tag:
                    subResult.append(i)
        data = [i for i in data if i not in subResult]
        result.append(subResult)
        groupAll(data, threshold, result, distfun)


def groupAllnoRecursive(data, threshold, distfun):
    result = []
    while len(data)>0:
        tem = data[0]
        subResult = []
        for i in data:
            tag = 1
            if distfun(i, tem) <= threshold:
                for j in subResult:
                    if distfun(i,j) > threshold:
                        tag = 0
                        break
                if tag:
                    subResult.append(i)
        result.append(subResult)
        data = [i for i in data if i not in subResult]
    return result


def searchGroup(data, threshold, singledata, distfun):
    result = []
    for i in data:
        if distfun(i,singledata) <= threshold:
            result.append(i)
    return result

def distance(a,b):
    return ((a-b) if a>b else (b-a))


if __name__ == '__main__':
    data1 = [1,2,5,4,5,5,6,7,1,2,0,8,5,9]
    data2 = [1,2,1,2,5,]
    result = []
    groupAll(data1, 2, result, distance)
    print result
    
    result = []
    groupAll(data2, 2, result, distance)
    print result

    result = groupAllnoRecursive(data1, 2, distance)
    print result

    result = groupAllnoRecursive(data2, 2, distance)
    print result