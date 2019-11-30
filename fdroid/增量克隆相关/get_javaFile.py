'''created by fwk
   2018/01/23
   Traverse to find java file
'''
import os
import sys

if __name__ == '__main__':
    # get all .java files from a path,write it to javaFile.txt
    fileDir = sys.argv[1]
    tem = []
    f = file('javaFile.txt', 'w')
    for root, dirs, files in os.walk(fileDir):
        for file in files:
            if file[-4:] == 'java':
                tem.append(os.path.join(root, file)+'\n')
    f.writelines(tem)
    f.close()
