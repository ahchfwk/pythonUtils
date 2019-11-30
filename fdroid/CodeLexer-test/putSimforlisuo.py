'''created by fwk
   2018/02/01
   computing simhash for lisuo's clone block and put to database
'''
import os, MySQLdb
import lexerparser, getHash


# tp has 4 value
# 20150101--20150131
# 20150201--20150228
# 20150301--20150331
# 1--20171130
def putSimhash(tp = '#1--20171130'):
    dbconn = MySQLdb.connect('10.141.221.73', 'root', 'root', 'fdroid')
    dbcursor = dbconn.cursor()
    sql = "select detection_tp,block_id,block_code from cc_block where \
    detection_id=2 and detection_tp='%s'" % tp
    dbcursor.execute(sql)
    tem = dbcursor.fetchall()[106666:]  # 18513
    updateSQL = "update fdroid.cc_block set simhash = '%s' \
    where block_id = %s and detection_tp = '%s'"
    for i in tem:
        code = i[2].replace(r"\n","").replace(r"\t","").replace(r"b'","").replace(r"',","")
        with open('lexer/tem.code', 'w') as f:
            f.write(code)
        os.popen('java -jar codeLexer.jar lexer/tem.code')
        token = lexerparser.parse()
        hash = getHash.get_nilsimsa(token)
        dbcursor.execute(updateSQL % (hash, i[1], i[0]))
        dbconn.commit()
        print i[1]


    dbcursor.close()
    dbconn.close()


def updateSim(detection_tp, block_id, simhash):
    pass

if __name__ == "__main__":
    putSimhash()