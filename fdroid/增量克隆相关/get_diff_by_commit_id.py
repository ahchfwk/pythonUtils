'''created by fwk
   2017/11/28
   get difffile.zip between commits
'''
# -*- coding:utf-8 -*-
import os
import sys
import zipfile  

def un_zip(file_name):  
    """unzip zip file"""  
    zfile = zipfile.ZipFile(file_name)
    zfile.extractall(file_name[:-4])
    # if os.path.isdir(file_name[:-4]):  
    #     pass  
    # else:  
    #     os.mkdir(file_name[:-4])  
    # for names in zip_file.namelist():  
    #     zip_file.extract(names, file_name[:-4])  
    # zip_file.close()  

    # zfile = zipfile.ZipFile('archive.zip','r')  


def get_diff_by_commit_id(id_1, id_2, path):
    '''id_1: old commit id
       id_2: new commit id
       path: the repository path'''
    os.chdir(path)
    updatedFiles = os.popen('git diff --name-status %s %s' % (id_1, id_2))
    updatedFiles = updatedFiles.readlines()
    with open('../diffFiles.txt', 'w') as f:
        f.writelines(updatedFiles)
    deletedFiles = []
    modifyAndAddFiles = []
    for file in updatedFiles:
        if file[0] == 'D':
            deletedFiles.append(file[2:].strip())
        else:
            modifyAndAddFiles.append(file[2:].strip())
    
    gitcmd = 'git archive -o ../latest.zip '+id_2
    for file in modifyAndAddFiles:
        gitcmd += ' '
        gitcmd += file
    
    print gitcmd
    x = os.popen(gitcmd).readlines()
    un_zip('../latest.zip')


if __name__ == "__main__":
    # give two commit_id and a path, get diffinfo writen into diffFiles.txt,
    # and pack the diff java files to latest dir
    try:
        commit_id_1 = sys.argv[1]
        commit_id_2 = sys.argv[2]
        path = sys.argv[3]
        get_diff_by_commit_id(commit_id_1, commit_id_2, path)
    except IndexError as IE:
        print IE.message
        print 'you must provide two commit id and a repository path'
    
    
