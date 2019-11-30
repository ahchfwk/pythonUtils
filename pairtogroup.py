# -*- coding: utf-8 -*-
"""created by fwk
   2018/06/20
   to transform clone pair to clone group 
"""

from collections import OrderedDict
data = [{1,2},{3,6},{4,7},{7,5},{3,1},{0,4}]
data2 = [{1},{3},{1,2},{3,4}]

def pairToGroupRecursive(grouplist, result):
    if len(grouplist) == 0:
        return result
    firstGroup = grouplist[0]
    flag = 0
    for i,v in enumerate(grouplist[1:]):
        # ru guo you jiaoji
        if firstGroup & v:
            flag = i+1
            break
    if flag:
        # qiu bing ji
        grouplist[0] = grouplist[0] | grouplist[flag]
        grouplist.pop(flag)
        # print grouplist
        pairToGroupRecursive(grouplist, result)
    else:
        result.append(grouplist[0])
        pairToGroupRecursive(grouplist[1:], result)
        

def pairToGroup(grouplist):
    keep = OrderedDict()
    result = [-1] * len(grouplist)
    for i in range(len(grouplist)):
        for j in grouplist[i]:
            if keep.has_key(j):
                keep[j].append(i)
            else:
                keep[j] = [i]
    print keep
    
    for i in range(len(grouplist)):
        # print grouplist[i]
        if result[i] == -1:
            tem = list(grouplist[i])
            print tem, '----'
            j = tem[0]
            # k = tem[1]
            result[i] = min(keep[j])
    print result

    
if __name__ == "__main__":
    pairToGroup(data)
