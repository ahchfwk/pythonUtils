import os


def parser(path):
    f = open(path, 'r')
    result = f.readlines()
    r = []
    for i in result:
        tem = i.split(':')
        filename = tem[0].replace('\\', '/')
        start = tem[1].split(',')[0]
        end = tem[1].split(',')[1]
        label = tem[2][:-1]
        r.append((filename, start, end, label))

    print r


def get_commit(repo_path):
    '''cc_intra_commit,还差repository_id没获取，去数据库搜根据repo_path'''
    os.chdir(repo_path)
    log = os.popen('git log')
    commit = ''
    commitDict = {}
    for line in log.readlines():
        if line.startswith('commit'):
            commit = line[7:-1]
        if line.startswith('Date:'):
            date = line[8:-1]
            commitDict[commit] = date
    os.chdir('../')
    return commitDict


def get_file(repo_path, commit_id):
    '''根据给定的repo_path和commit_id就能对应的java文件路径，文件名，以及token文件名'''
    os.chdir(repo_path)
    os.system('git checkout ' + commit_id)
    os.chdir('../')
    tem = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file[-4:] == 'java':
                file_addr = os.path.join(root, file).replace('\\', '/')
                file_name = file_addr.split('/')[-1]
                tokenfile_name = file_name+'.java.2_0_0_0.default.ccfxprep'
                tem.append((file_addr,file_name,tokenfile_name))

    os.system('git checkout master')
    os.chdir('../')
    return tem


if __name__ == '__main__':
    # parser(r'C:\Users\fwk\Desktop\hivedbClone\0a87cbc513d3b02270e2cc6eeed96d755634d7ce.txt')
    print get_file('hivedb', '09efeff')