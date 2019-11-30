'''created by fwk
   2018/3/15
   To trans the code in DB to hash
'''

import os, MySQLdb, getHash
import lexerparser, getHash

if __name__ == '__main__':
    querysql = """SELECT distinct Repository_Id, Release_Name FROM cc_intra_cloneblock_release;"""

    sql = """SELECT 
    cc_intra_cloneblock_release.Repository_Id, 
    cc_intra_cloneblock_release.Release_Name, 
    cc_intra_cloneblock_release.Cloneblock_Id,
    cc_intra_cloneblock_release.Code_fragment
    FROM cc_intra_cloneblock_release where Repository_Id=%s 
    and Release_Name='%s'"""

    updateSQL = """update cc_intra_cloneblock_release set \
    Simhash='%s' where Repository_Id=%s and \
    Release_Name='%s' and Cloneblock_Id=%s and Detection_Id=1"""

    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()

    dbcursor.execute(querysql)
    result = dbcursor.fetchall()

    for release in result:
        dbcursor.execute(sql % (release[0], release[1]))
        tem = dbcursor.fetchall()
        for i in tem:
            print i[0], i[1], i[2],
            code = i[3]
            with open('lexer/tem1.code', 'w') as f:
                f.write(code)
            os.popen('java -jar codeLexer.jar lexer/tem1.code')
            token = lexerparser.parse()
            hash = getHash.get_nilsimsa(token)
            print hash
            #dbcursor.execute(updateSQL % (hash, i[0], i[1], i[2]))
        dbconn.commit()
    dbcursor.close()
    dbconn.close()


