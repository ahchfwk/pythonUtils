#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import cProfile


def easyPairToClass(pairMap):
    result = []
    def recur(key):
        value = pairMap.get(key,-1)
        if value != -1 and not value[0]:
            for member in value[1]:
                s.add(member)
                recur(member)
            value[0] = True

    for k,v in pairMap.iteritems():
        if not v[0]:
            s = set([])
            s.add(k)
            recur(k)
            result.append(sorted(list(s)))

    return result


def toEasyDict(prilist):
    dict = collections.OrderedDict()
    for i in prilist:
        i.sort()
    for pair in prilist:
        dict[pair[0]] = dict.get(pair[0],[False,[]])
        dict[pair[0]][1].append(pair[1])
    for k,v in  dict.iteritems():
        v[1].sort()
    # print dict
    return dict


if __name__=='__main__':
    data = [[1,2],[3,6],[3,1]]
    prilist = (
    (11,12),
    (11,14),
    (11,13),
    (11,16),
    (11,15),
    (12,13),
    (12,14),
    (12,15),
    (13,15),
    (14,15),
    (14,17),
    (60,68),
    (77,99),
    (77,68)
    )

    # test = toEasyDict(prilist)
    # print easyPairToClass(test)

    test = toEasyDict(data)
    print easyPairToClass(test)


