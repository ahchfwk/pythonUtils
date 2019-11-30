import json

l = {'1':['false','top'],
    '2':[[1],[2]]}
x = [1,2,3]

f = open('te.json','w')
tem = {1:l,2:x}

print json.dump(tem,f)
f.close()
s = open('te.json','r')
x = json.load(s)
print x