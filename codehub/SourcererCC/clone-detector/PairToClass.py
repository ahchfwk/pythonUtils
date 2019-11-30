#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""created by fwk
   2018/06/20
   to transform clone pair to clone group 
"""

import sys
# set max recursion depth
sys.setrecursionlimit(10000)

data = [{1,2},{3,6},{4,7},{7,5},{3,1},{1,3},{0,4}]*200

def pairToGroup(grouplist, result, limit):
    # print grouplist
    # print result
    if len(grouplist) == 0:
        return grouplist
    if limit == 1000:
        return grouplist
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
        limit += 1
        return pairToGroup(grouplist, result, limit)
    else:
        result.append(grouplist[0])
        limit += 1
        return pairToGroup(grouplist[1:], result, limit)
        

def pairToGroup2(grouplist):
    limit = 0
    result = []
    tem = pairToGroup(grouplist, result, limit)
    while tem:
        tem = pairToGroup(tem, result, limit)
    return result


if __name__ == "__main__":
    result = pairToGroup2(data)
    print result

    
