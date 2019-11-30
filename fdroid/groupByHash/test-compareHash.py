import getHash
import time


hashlist = []
with open('hash.txt', 'r') as f:
    hashlist = f.readlines()[:100000]

test = hashlist[:10]

start = time.clock()
for i in test:
    for j in hashlist:
        getHash.compare_hash(i, j)

end = time.clock()
print end - start  # 61s
