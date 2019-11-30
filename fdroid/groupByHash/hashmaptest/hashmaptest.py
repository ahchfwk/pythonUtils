import sys, time
sys.path.append("C:\\Users\\fwk\\Desktop\\CodeLexer-test")
import getHash

hashlist = []
with open('hash.txt','r') as f:
    hashlist = f.readlines()[:900000]
    

hashDict = {}
def store(d, hs, h):
    if d.has_key(hs):
        d[hs].append(h)
    else:
        d[hs] = []
        d[hs].append(h)
    
for h in hashlist:
    store(hashDict, h[:16], h)
    store(hashDict, h[16:32], h)
    store(hashDict, h[32:48], h)
    store(hashDict, h[48:], h)


print sys.getsizeof(hashlist)/1024
print sys.getsizeof(hashDict)/1024


f = lambda x, y : x.append(y)
s = time.clock()
# for h in hashlist:
#     if hashDict.has_key(h[:16]):
#         for i in hashDict[h[:16]]:
#             x = getHash.compare_hash(i, h)
#             if x <= 3:
#                 f([], i)
#     if hashDict.has_key(h[16:32]):
#         for i in hashDict[h[16:32]]:
#             x = getHash.compare_hash(i, h)
#             if x <= 3:
#                 f([], i)
#     if hashDict.has_key(h[32:48]):
#         for i in hashDict[h[32:48]]:
#             x = getHash.compare_hash(i, h)
#             if x <= 3:
#                 f([], i)
#     if hashDict.has_key(h[48:]):
#         for i in hashDict[h[48:]]:
#             x = getHash.compare_hash(i, h)
#             if x <= 3:
#                 f([], i)

e = time.clock()
print e-s # 2092s

# 
zhe = []
with open('hash.txt','r') as f1:
    hashlist = f1.readlines()[900000:]
s = time.clock()
for h in hashlist:
    if hashDict.has_key(h[:16]):
        for i in hashDict[h[:16]]:
            x = getHash.compare_hash(i, h)
            if x <= 3:
                f(zhe, i)
    if hashDict.has_key(h[16:32]):
        for i in hashDict[h[16:32]]:
            x = getHash.compare_hash(i, h)
            if x <= 3:
                f(zhe, i)
    if hashDict.has_key(h[32:48]):
        for i in hashDict[h[32:48]]:
            x = getHash.compare_hash(i, h)
            if x <= 3:
                f(zhe, i)
    if hashDict.has_key(h[48:]):
        for i in hashDict[h[48:]]:
            x = getHash.compare_hash(i, h)
            if x <= 3:
                f(zhe, i)

e = time.clock()
print e-s # 733
print len(zhe)