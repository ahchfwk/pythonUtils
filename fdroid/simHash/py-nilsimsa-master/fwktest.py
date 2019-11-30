"""
Purpose: Set of unit tests for nilsimsa package.

Test data consists of 20 randomly selected documents from a Diffeo corpus.

This software is released under an MIT/X11 open source license.

Copyright 2012-2015 Diffeo, Inc.
"""
import MySQLdb,time

from nilsimsa.deprecated._deprecated_nilsimsa import Nilsimsa as orig_Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints

import extractToken
import getCodeFragment
import os
try:
    import cPickle as pickle
except ImportError:
    import pickle

test_data_dir = os.path.join(os.path.dirname(__file__), "nilsimsa\\test_data\\")
test_data = "test_dict.p"
test_dict = os.path.join(test_data_dir, test_data)
sid_to_nil = pickle.load(open(test_dict, "rb"))
# print sid_to_nil

nil = Nilsimsa('0'*64)
s1 = nil.hexdigest()
nil = Nilsimsa('0'*63+'1')
s2 = nil.hexdigest()
print s1,s2
print compare_digests(s1,s2)

# for i in range(1,30):
#     cloneGroup = getCodeFragment.getCloneClass('1.2.txt', i)
#     s1 = Nilsimsa(cloneGroup[0]).hexdigest()
#     s2 = Nilsimsa(cloneGroup[1]).hexdigest()
#     #print s1,s2
#     print compare_digests(s1,s2)
#     if compare_digests(s1,s2) <0:
#         getCodeFragment.printCloneClass('1.2.txt', i)

# for i in range(1,50):
#     cloneGroup = getCodeFragment.getCloneClass('1.2.txt', i)
#     s1 = Nilsimsa(cloneGroup[0]).hexdigest()
#     cloneGroup = getCodeFragment.getCloneClass('1.2.txt', i+1)
#     s2 = Nilsimsa(cloneGroup[0]).hexdigest()
#     #print s1,s2
#     print compare_digests(s1,s2)
#     if compare_digests(s1,s2) >100:
#         getCodeFragment.printCloneClass('1.2.txt', i)
#         getCodeFragment.printCloneClass('1.2.txt', i+1)

def get_nilsimsa():
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    # sql = 'select block_id,block_code from fdroid.cc_block where detection_id=1 and detection_tp = "20150101--20150131"'
    sql = 'select detection_tp,block_id,block_code from fdroid.cc_block where detection_id=1'
    dbcursor.execute(sql)
    f = open('nilsimsa1.txt','w')
    start = time.clock()
    for i in dbcursor.fetchall():
        f.write(str(i[0])+ '   '+ str(i[1])+ '   ' + Nilsimsa(i[2]).hexdigest() + '\n')
        print i[1]
    
    end = time.clock()
    f.write(str(end-start))
    f.close()
    dbcursor.close()
    dbconn.close()

get_nilsimsa()