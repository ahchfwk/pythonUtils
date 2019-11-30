# -*- coding: utf-8 -*-
'''created by fwk
   2018/03/15
   test for groupByHash
'''
import MySQLdb
import getHash
import groupByHash
import time


if __name__ == '__main__':
    # dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    # dbcursor = dbconn.cursor()
    # sql = "SELECT block_id, simhash FROM fdroid.cc_block where detection_tp = '20150101--20150131' and block_id;"
    # dbcursor.execute(sql)
    # re = dbcursor.fetchall()
    # dbcursor.close()
    # dbconn.close()
    # re = [str(x[0])+' '+x[1]+'\n' for x in re]
    # with open('hash.txt','w') as f:
    #     f.writelines(re)

    # 准备数据
    data = []
    with open('hash.txt','r') as f:
        data = f.readlines()
        data = [x.split()[1] for x in data]
    result = []
    # groupByHash.groupAllnoRecursive(data, 1, result, getHash.compare_hash); print result
    # print groupByHash.searchGroup(data, 1, data[1], getHash.compare_hash)

    # 测试
    data1 = data[:10000]
    data2 = data[:20000]
    data5 = data[:5000]

    """----------- 在10000条数据中找出相似数据，需要1.6s，数据量和时间成正比，阈值无关 ------------"""
    # s = time.clock()
    # for i in data[:10]:
    #     groupByHash.searchGroup(data1, 1, i, getHash.compare_hash)
    # e = time.clock()
    # print '阈值为1，共10000条数据，寻找10条hash需要:',e-s,'s'    #16s

    # s = time.clock()
    # for i in data[:10]:
    #     groupByHash.searchGroup(data1, 100, i, getHash.compare_hash)
    # e = time.clock()
    # print '阈值为100，共10000条数据，寻找10条hash需要:',e-s,'s'    #16s，证明时间与阈值无关

    # s = time.clock()
    # for i in data[:10]:
    #     groupByHash.searchGroup(data5, 1, i, getHash.compare_hash)
    # e = time.clock()
    # print '阈值为1，共5000条数据，寻找10条hash需要:',e-s,'s'    #8s, 证明时间与总数据量呈线性关系


    """----------- 将100条数据完全分组，需要0.7s，数据量的平方和时间成正比，阈值无关 ------------"""
    # s = time.clock()
    # for i in range(10):
    #     groupByHash.groupAllnoRecursive(data[100*i:100*i+100], 5, getHash.compare_hash)
    # e = time.clock()
    # print '完全分组总量为100的data 10次，需要:',e-s,'s'    #7s
    
    # s = time.clock()
    # for i in range(10):
    #     groupByHash.groupAllnoRecursive(data[200*i:200*i+200], 5, getHash.compare_hash)
    # e = time.clock()
    # print '完全分组总量为200的data 10次，需要:',e-s,'s'    #28s,证明完全分组与数据量的平方成线性关系

    # s = time.clock()
    # for i in range(20):
    #     print i
    #     groupByHash.groupAllnoRecursive(data[1000*i:1000*i+1000], 5, getHash.compare_hash)
    # e = time.clock()
    # print '完全分组总量为1000的data 20次，需要:',e-s,'s'    #1199s,证明完全分组与数据量的平方成线性关系

    # s = time.clock()
    # result = []
    # groupByHash.groupAllnoRecursive(data[:10000], 5, getHash.compare_hash)
    # e = time.clock()
    # print '完全分组总量为10000的data 1次，需要:',e-s,'s'    #预计7000s，实际4762s,证明完全分组与数据量的平方成线性关系