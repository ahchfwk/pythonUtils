####################################
# sql for use in anywhere
# author niko -*- date 07-26-2018
####################################

# -*- database codehub -*-
def getRepoIDbyName(name):
    return "SELECT repository_id FROM repository_java where local_addr like 'repositories/%/" + name + "'"

def getReleaseIDByRepoID(id):
    return "SELECT id from releases where repository_id=" + str(id)

def getCloneGroupInfoByReleaseID(id):
    return "SELECT A.block_id, A.group_id, B.name FROM cc_cloneGroup as A, releases as B where A.release_id = B.id and B.id=" + str(id)

def getCurProjectInCCDB():
    #return "SELECT DISTINCT C.local_addr FROM cc_cloneGroup as A, releases as B, repository_java as C where A.release_id=B.id and B.repository_id=C.repository_id and C.repository_id=" + str(1438007)
    return "SELECT DISTINCT C.local_addr FROM cc_cloneGroup as A, releases as B, repository_java as C where A.release_id=B.id and B.repository_id=C.repository_id and C.reporitory_id=1438007"

