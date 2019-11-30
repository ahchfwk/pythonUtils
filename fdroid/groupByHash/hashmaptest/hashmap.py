'''created by fwk
   2018/4/18
   optimize simhash by using hashmap
'''


import sys
import time
sys.path.append("C:\\Users\\fwk\\Desktop\\CodeLexer-test")
import getHash


hashlist = []
codehashlist = []
tokenhashlist = []
codehashDict = {}
tokenhashDict = {}
hash2IDDict = {}


def store(d, hs, h):
    if d.has_key(hs):
        d[hs].append(h)
    else:
        d[hs] = []
        d[hs].append(h)


def pretreat(hashfile='codehubhash.txt'):
    print "loading data..."
    s = time.clock()
    with open(hashfile, 'r') as f:
        hashlist = f.readlines()
    codehashlist = [x.split(',')[2] for x in hashlist]
    tokenhashlist = [x.split(',')[4].strip() for x in hashlist]
    for h in codehashlist:
        store(codehashDict, h[:16], h)
        store(codehashDict, h[16:32], h)
        store(codehashDict, h[32:48], h)
        store(codehashDict, h[48:], h)
    for h in tokenhashlist:
        store(tokenhashDict, h[:16], h)
        store(tokenhashDict, h[16:32], h)
        store(tokenhashDict, h[32:48], h)
        store(tokenhashDict, h[48:], h)
    for h in hashlist:
        store(hash2IDDict, h.split(',')[2], h.split(',')[0])
    print time.clock() - s,'seconds'


def searchHash(hash, hashinput=None):
    S = set()
    if hashinput:
        while True:
            hash = raw_input('please put in a simhash:')
            s = time.clock()
            if codehashDict.has_key(hash[:16]):
                for i in codehashDict[hash[:16]]:
                    x = getHash.compare_hash(i, hash)
                    if x <= 3:
                        S.add(i)
            if codehashDict.has_key(hash[16:32]):
                for i in codehashDict[hash[16:32]]:
                    x = getHash.compare_hash(i, hash)
                    if x <= 3:
                        S.add(i)
            if codehashDict.has_key(hash[32:48]):
                for i in codehashDict[hash[32:48]]:
                    x = getHash.compare_hash(i, hash)
                    if x <= 3:
                        S.add(i)
            if codehashDict.has_key(hash[48:]):
                for i in codehashDict[hash[48:]]:
                    x = getHash.compare_hash(i, hash)
                    if x <= 3:
                        S.add(i)
            print S
            for r in S:
                print 'there are',len(hash2IDDict[r]),'simcodes'
            print time.clock() -s
            S = set()
    else:
        if codehashDict.has_key(hash[:16]):
            for i in codehashDict[hash[:16]]:
                x = getHash.compare_hash(i, hash)
                if x <= 3:
                    S.add(i)
        elif codehashDict.has_key(hash[16:32]):
            for i in codehashDict[hash[16:32]]:
                x = getHash.compare_hash(i, hash)
                if x <= 3:
                    S.add(i)
        elif codehashDict.has_key(hash[32:48]):
            for i in codehashDict[hash[32:48]]:
                x = getHash.compare_hash(i, hash)
                if x <= 3:
                    S.add(i)
        elif codehashDict.has_key(hash[48:]):
            for i in codehashDict[hash[48:]]:
                x = getHash.compare_hash(i, hash)
                if x <= 3:
                    S.add(i)
        return S


if __name__ == '__main__':
    pretreat()
    with open('codehubhash.txt', 'r') as f:
        hashlist = f.readlines()
    codehashlist = [x.split(',')[2] for x in hashlist]
    print sys.getsizeof(hashlist)
    print sys.getsizeof(codehashDict)
    s = time.clock()
    searchHash('c5d20d01dd8f995b73ab5ac05b11c8a9f2685a244ae2b8f7a8156c157fa62b0d',1)
    e = time.clock()
    print e - s  # 733s
    # t = 0
    # print len(codehashlist[::100])
    # for i in codehashlist[::100]:
    #     s = time.clock()
    #     searchHash(i)
    #     e = time.clock()
    #     t = t+s-e
    # print t

