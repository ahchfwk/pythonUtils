'''created by fwk
   2017/12/13
   To transform the tokenblock to clone fragment
'''

import os, MySQLdb, getHash
import lexerparser, getHash

def getCodeFrag(sourceFilePath, start, end):
    f = open(sourceFilePath, 'r')
    sourceCode = f.readlines()
    f.close()
    tem = ''
    for i in sourceCode:
        tem = tem + i.replace('\n', '\r\n')
    sourceCode = tem
    return sourceCode[int(start):int(end) + 1]


def changeTag(repo, tag):
    '''change tag by tag for each repo'''
    os.chdir('E:/codeclone/fdroid/'+repo)
    os.popen('git checkout '+tag)
    # e:/codeclone
    origindir = '/'.join(__file__.split('\\')[:-1])
    os.chdir(origindir)


def getFragFromTag(repo, tag, sourceFilePath, start, end):
    changeTag(repo, tag)
    code = getCodeFrag('E:/codeclone/'+sourceFilePath, start, end)
    # recover(repo)
    return code


def recover(repo):
    os.chdir('E:/codeclone/fdroid/'+repo)
    os.popen('git checkout master')
    origindir = '/'.join(__file__.split('\\')[:-1])
    os.chdir(origindir)


if __name__ == '__main__':
    # print getFragFromTag('geecko86-QuickLyric','2.0.8c','fdroid/geecko86-QuickLyric/QuickLyric/src/main/java/com/geecko/QuickLyric/lyrics/UrbanLyrics.java',1929,4605)
    querysql = """SELECT distinct Repository_Id, Release_Name FROM fdroid.cc_intra_cloneblock_release;"""

    sql = """SELECT 
    cc_intra_cloneblock_release.Repository_Id, 
    repository.local_address, 
    cc_intra_cloneblock_release.Release_Name, 
    cc_intra_cloneblock_release.Cloneblock_Id, 
    cc_intra_cloneblock_release.File_Addr, 
    cc_intra_cloneblock_release.Start_token, 
    cc_intra_cloneblock_release.End_token
    FROM fdroid.cc_intra_cloneblock_release, fdroid.repository where cc_intra_cloneblock_release.Repository_Id = repository.repository_id
    and repository.Repository_Id=%s and cc_intra_cloneblock_release.Release_Name='%s'"""

    updateSQL = """update fdroid.cc_intra_cloneblock_release set \
    Code_Fragment='%s', Simhash='%s' where Repository_Id=%s and \
    Cloneblock_Id=%s and Release_Name='%s' and Detection_Id=1"""

    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()

    dbcursor.execute(querysql)
    result = dbcursor.fetchall()

    for release in result[2500:]:
        dbcursor.execute(sql % (release[0], release[1]))
        tem = dbcursor.fetchall()
        havaToChangeTag = 1
        for i in tem:
            print i[0], i[2], i[3]
            if havaToChangeTag:
                changeTag(i[1].split('/')[-1], i[2])
                havaToChangeTag = 0
            code = getCodeFrag('E:/codeclone/'+i[4], i[5], i[6])
            
            with open('lexer/tem1.code', 'w') as f:
                f.write(code)
            os.popen('java -jar codeLexer.jar lexer/tem1.code')
            token = lexerparser.parse()
            hash = getHash.get_nilsimsa(token)
            # print code, hash, i[0], i[3], i[2]
            # '' in sql means '
            dbcursor.execute(updateSQL % (code.replace("'","''").replace('\\', '\\\\'), hash, i[0], i[3], i[2]))
        dbconn.commit()
        havaToChangeTag = 1
    dbcursor.close()
    dbconn.close()


