# -*- coding:utf-8 -*-
'''created by fwk
   2018/01/23
   get commit log
'''
import os
import sys

# get all commit info for a giving repo path
path = sys.argv[1]
os.chdir(path)
x = os.popen('git log').readlines()
print x

with open('../log.txt', 'w') as f:
    f.writelines(x)

