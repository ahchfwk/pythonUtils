'''created by fwk
   2017/12/25
   To refine the tokenfile output by ccfinderx
'''

def refine(Tokenfilepath):
    '''
    refine the file string 
    '''
    f = open(Tokenfilepath, 'r')
    s = f.readlines()
    f.close()
    result = ''.join([x[12:].strip()+' ' for x in s])
    return result


if __name__ == "__main__":
    print refine(r'C:\Users\fwk\Desktop\BucketAssigner.java.java.2_0_0_0.default.ccfxprep')