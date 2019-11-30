'''created by fwk
   2017/12/05
   mkdir
'''
import os
import sys

def make_pjdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == '__main__':
    make_pjdir(sys.argv[1])
