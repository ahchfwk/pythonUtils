####################################
# get genealogy data from db and transform its format
# author niko -*- date 08-13-2018
####################################

import sys
sys.path.append(r"C:\Users\niko\Desktop\功能代码\读取codehub数据库python\detail")
import sql.sqlBuilder as SqlBui
import info.releaseInfo as INFO
import simplejson as json
import pymysql
import config
import re
import db
import os

def extractMethodName(file_string):
    item = re.findall(r"(.*)\(", file_string)
    targetStr = item[0]
    methodName = ''
    for i in range(len(targetStr) - 1, 0, -1):
        if(targetStr[i] == ' '):
          break
        methodName += targetStr[i]
    return methodName

def reverseStr(s):
    l=list(s)
    l.reverse()
    return "".join(l)

def sortedDictValues(adict): 
    keys = adict.keys()
    keys = list(keys)
    keys.sort()
    print(keys)
    return [adict[key] for key in keys] 

def getGenealogyDataByName(dbcursor, projectName):
    '''
       row[0] method id
       row[1] group id
       row[2] version name
       row[3] method codeblock
       row[4] created time
       the row above are row in the third for-loop
    '''
    print("getGenealogyData:\n", projectName)
    releaseID = None
    releaseDict = {}
    versionName = ""
    sql = SqlBui.getRepoIDbyName(projectName)
    results = db.getDataFromDB(dbcursor, sql)
    i = 0
    for row in results:
        print("current release id:", i)
        if(row[0] > 0):
            sql = SqlBui.getReleaseIDByRepoID(row[0])
            releaseID = db.getDataFromDB(dbcursor, sql)
            for row in releaseID:
                sql = SqlBui.getCloneGroupInfoByReleaseID(row[0])
                info = db.getDataFromDB(dbcursor, sql)
                for row in info:
                    versionName = row[4]
                    methodCode = row[5]
                    methodName = extractMethodName(methodCode)
                    methodName = reverseStr(methodName)
                    #print(methodName, methodCode)
                    if(versionName not in releaseDict):
                        releaseDict[versionName] = INFO.ReleaseInfo(versionName)
                        cloneInfo = INFO.CloneInfo(methodName, str(row[0]) + "-*-" + methodCode)
                        releaseDict[versionName].addInfo(cloneInfo)
                    else:
                        cloneInfo = INFO.CloneInfo(methodName, str(row[0]) + "-*-" + methodCode)
                        releaseDict[versionName].addInfo(cloneInfo)
        i += 1

    releaseList = sortedDictValues(releaseDict)
    return releaseList

def transformGenealogyData(data, dirName):
    print("transformGenealogyData")
    releaseList = data
    releaseNum = len(releaseList)
    num = 0
    for item in releaseList:
        #print(releaseDict[item].cloneGroupDict)
        curDict = item.cloneGroupDict
        release = {}
        release["name"] = "release-*-" + str(num)
        release["children"] = []
        for itemChild in curDict:
            group = {}
            curList = curDict[itemChild]
            group["name"] = "group-*-" + str(itemChild)
            group["children"] = []
            for element in curList:
                method = {}
                method["name"] = str(element)
                method["size"] = 200
                group["children"].append(method)
            release["children"].append(group)
        f = open(dirName + "/release" + str(num) + ".json", "w")
        f.write(json.dumps(release))
        f.close()

        num += 1
    return num

def genealogyWriteToFile(dbcursor, projectName):
    print("genealogyWriteToFile")
    nameArr = projectName.split("/")
    childDirName = nameArr[0] + "O" + nameArr[1] + "O" + nameArr[2]
    baseDirName = "res/genealogyData/"
    dirName =  baseDirName + childDirName
    if(os.path.exists(dirName) == False):
        os.mkdir(dirName)

        data = getGenealogyDataByName(dbcursor, projectName)
        num = transformGenealogyData(data, dirName)
        
        f = open(dirName + "/fileCount.txt", "w")
        f.write(str(num))
        f.close()
    else:
        print("dir already exitst")
    
if __name__=='__main__':
    dbcursor = db.connectDatabase()
    projectName = "repositories/bndtools/bndtools"
    #genealogyWriteToFile(dbcursor, projectName)
    cloneRelease = getGenealogyDataByName(dbcursor, projectName)
    print(cloneRelease)
