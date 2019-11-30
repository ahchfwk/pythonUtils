'''created by fwk
   2018/03/11
   encapsulation the nilsimsa
'''
# from nilsimsa.deprecated._deprecated_nilsimsa import Nilsimsa as orig_Nilsimsa
from nilsimsa import Nilsimsa, compare_digests, convert_hex_to_ints
import time

# nil = Nilsimsa('0'*64)
# s1 = nil.hexdigest()
# nil = Nilsimsa('0'*64+'11111234234223423423424')
# s2 = nil.hexdigest()
# print s1,s2
# print compare_digests(s1,s2)

def get_nilsimsa(string):
    return Nilsimsa(string).hexdigest()


def compare_hash(hash1, hash2):
    return 128 - compare_digests(hash1, hash2)

def hash_test():
    # it takes about 6ms each 100 char 
    start = time.clock()
    # for i in range(100):
    #     get_nilsimsa('1~qwerhjklkjhgyulkjhnbvmnbghupolredwsaqzxcvbnm,./;lkjhgfdsaqwertyuiop[]|?><!@#$%^&*()ASDFGHJKLP'\
    #     '1~qwerhjklkjhgyulkjhnbvmnbghupolredwsaqzxcvbnm,./;lkjhgfdsaqwertyuiop[]|?><!@#$%^&*()ASDFGHJKLP'\
    #     'QMWNERTYHGFDCXS:;"*{}ABChQMWNERTYHGFDCXS:;"*{}ABChQMWNERTYHGFDCXS:;"*{}ABChQMWNERTYHGFDCXS:;"*{}ABCh'\
    #     'QMWNERTYHGFDCXS:;"*{}ABChQMWNERTYHGFDCXS:;"*{}ABChQMWNERTYHGFDCXS:;"*{}ABChQMWNERTYHGFDCXS:;"*{}ABCh')
    # end = time.clock()
    # print end-start

    # start = time.clock()
    # for i in range(100):
    #     get_nilsimsa('1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890')
    # end = time.clock()
    # print end-start

    # start = time.clock()
    # for i in range(100):
    #     get_nilsimsa('1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'\
    #     '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
    # end = time.clock()
    # print end-start

    # start = time.clock()
    # for i in range(100):
    #     get_nilsimsa('1111111111111                                                111111111111111111111111111111111111111'\
    #     '0000000    000000000   00000             00             0000         00 0 0 0 0 0 0 0 0 0 0        0')
    # end = time.clock()
    # print end-start

if __name__ == '__main__':
    l = get_nilsimsa('123456789')
    n = get_nilsimsa('234567890')
    print l
    print n
    print compare_hash(l, n)
    hash_test()
    
