####################################
# sql for use in anywhere
# author niko -*- date 07-26-2018
####################################

# -*- database codehub -*-
def getRepoIDbyName(name):
    return "SELECT repository_id FROM repository_java where local_addr='" + name + "'"

def getReleaseIDByRepoID(id):
    return "SELECT id from releases where repository_id=" + str(id)

#def getCloneGroupInfoByReleaseID(id):
#    return "SELECT distinct A.block_id, A.group_id, B.name, C.code, B.created_at FROM cc_cloneGroup as A, releases as B, cc_cloneBlock as C where A.release_id = B.id and A.release_id = C.release_id and A.block_id = C.block_id and B.id=" + str(id)

def getCloneGroupInfoByReleaseID(id):
    return "SELECT distinct A.block_id, A.group_id, B.name, C.path, B.created_at, C.code FROM cc_cloneGroup as A, releases as B, cc_cloneBlock as C where A.release_id = B.id and A.release_id = C.release_id and A.block_id = C.block_id and B.id=" + str(id)

def getCurProjectAddrInCCDB(id):
    ''' get the project which has already checked clone Info and put into DBtable'''
    return "SELECT DISTINCT C.local_addr FROM cc_cloneGroup as A, releases as B, repository_java as C where A.release_id=B.id and B.repository_id=C.repository_id and C.repository_id=" + str(id)

def getRepoIdBatch(start, batchCount):
    '''get repoId from repository_java by batch'''
    return "SELECT repository_id FROM repository_java where id>=" + str(start) + " limit " + str(batchCount)

def getProjectWebUrlByReleaseID(id):
    return "SELECT distinct p.git_addr from java_rl_class as c, java_rl_class_method as m, releases as r, repository_java as p where c.classid = m.classid and c.rlid=r.id and r.repository_id=p.repository_id and r.id =" + str(id)

