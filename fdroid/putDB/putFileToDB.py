'''created by fwk
   2017/12/29
   insert file info of clones into database
'''
import os
import MySQLdb


def get_repoid_depend_localAdd(localAdd):
    '''根据本地路径随机取一个clone结果文件名作为commit，查询其repoid并返回'''
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    commit = os.listdir(localAdd)[0][:-4]
    sql = 'select repository_id from fdroid.gitcommit where commit_id = "%s"' % (
        commit)
    dbcursor.execute(sql)
    repoid = dbcursor.fetchone()
    dbcursor.close()
    dbconn.close()
    if repoid:
        return repoid[0]
    else:
        return None


def get_dir(path):
    '''给一个根目录，返回所有repo在我的机器上的绝对路径的list'''
    # os.chdir(r'E:\fdroidResult')
    # print os.path.abspath(os.listdir(path)[0])
    # print os.getcwd().decode('cp936').encode('utf-8')
    roots = []
    for root, dirs, files in os.walk(path):
        if root:
            roots.append(root)
    return roots[1:]


def putFileToDB(path):
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    detection_id = 1  # detection_id
    for directory in get_dir(path):
        repository_id = get_repoid_depend_localAdd(directory)  # repository_id
        # if the repository_id can be found in DB
        if repository_id:
            filelist = os.listdir(directory)
            for f in filelist:
                print directory + '/' + f
                commit_id = f[:-4]  # commit_id
                clones = open(directory + '/' + f, 'r')
                tem = clones.readlines()
                clones.close()
                fileset = set([])
                # to filter the duplicated filename
                for i in tem:
                    file_addr = i.split(':')[0].replace('\\', '/')
                    fileset.add(file_addr)

                file_id = 0
                for i in fileset:
                    file_id += 1
                    file_addr = i
                    file_name = file_addr.split('/')[-1]
                    
                    sql = 'INSERT INTO cc_intra_file (Detection_Id,Repository_Id,Commit_Id,File_Id,File_Addr,File_Name)\
                     VALUES (%s,%s,%s,%s,%s,%s)'
                    try:
                        dbcursor.execute(
                            sql, (detection_id, repository_id, commit_id, file_id, file_addr, file_name))
                    except:
                        dbconn.rollback()
                        print '????'
                        print detection_id, repository_id, commit_id, file_id, file_addr, file_name
                    dbconn.commit()

    dbcursor.close()
    dbconn.close()


if __name__ == "__main__":
    putFileToDB(r'C:\Users\fwk\Desktop\py\putDB\fdroidResultTemp')
