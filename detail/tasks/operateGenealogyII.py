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
       row[3] filePath
       row[4] created time
       row[5] method codeblock
       the row above are row in the third for-loop
    '''
    print("getGenealogyData:\n", projectName)
    releaseID = None
    releaseDict = {}
    versionName = ""
    projectUrl = ""
    sql = SqlBui.getRepoIDbyName(projectName)
    results = db.getDataFromDB(dbcursor, sql)
    i = 0
    for row in results:
        print("current release id:", i)
        if(row[0] > 0):
            sql = SqlBui.getReleaseIDByRepoID(row[0])
            releaseID = db.getDataFromDB(dbcursor, sql)
            for row in releaseID:
                curReleaseID = row[0]
                sql = SqlBui.getCloneGroupInfoByReleaseID(curReleaseID)
                info = db.getDataFromDB(dbcursor, sql)
                for row in info:
                    versionName = row[4]
                    path = row[3]
                    methodCode = row[5]
                    methodName = extractMethodName(methodCode)
                    methodName = reverseStr(methodName)
                    path = path.split("/")
                    fileName = path[len(path) - 1]
                    #print(methodName, methodCode)
                    if(versionName not in releaseDict):
                        releaseDict[versionName] = INFO.ReleaseInfo(versionName)
                        cloneInfo = INFO.CloneInfo(methodName, str(row[0]) + "-*-" + str(row[1]) + "-*-" + str(curReleaseID) + "-*-" + methodName + "-*-" + fileName)
                        releaseDict[versionName].addInfo(cloneInfo)
                    else:
                        cloneInfo = INFO.CloneInfo(methodName, str(row[0]) + "-*-" + str(row[1]) + "-*-" + str(curReleaseID) + "-*-" + methodName + "-*-" + fileName)
                        releaseDict[versionName].addInfo(cloneInfo)
        i += 1

    releaseList = sortedDictValues(releaseDict)

    if(projectUrl == ""):
        sqlForUrl = SqlBui.getProjectWebUrlByReleaseID(releaseID[0][0])
        projectUrl = db.getDataFromDB(dbcursor, sqlForUrl)
        projectUrl = projectUrl[0][0]
    return releaseList, projectUrl

def transformGenealogyDataDetail(data, dirName):
    print("transformGenealogyDataDetail")
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
        f = open(dirName + "/releaseDetail" + str(num) + ".json", "w")
        f.write(json.dumps(release))
        f.close()

        num += 1
    return num

def transformGenealogyData(data, projectUrl, dirName):
    print("transformGenealogyData")
    releaseList = data
    releaseNum = len(releaseList)
    num = 0
    for item in releaseList:
        #print(releaseDict[item].cloneGroupDict)
        curDict = item.cloneGroupDict
        release = {}
        release["name"] = "release##" + str(num)
        release["children"] = []
        for itemChild in curDict:
            group = {}
            curList = curDict[itemChild]
            methodCount = 0
            methodInfo = ""
            for element in curList:
                curInfo = "##" + str(element)
                methodInfo += curInfo
                methodCount += 1
            group["name"] = "group##" + projectUrl + methodInfo
            group["size"] = 200 + methodCount * 10
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

        data, projectUrl = getGenealogyDataByName(dbcursor, projectName)
        num = transformGenealogyData(data, projectUrl, dirName)
        
        f = open(dirName + "/fileCount.txt", "w")
        f.write(str(num))
        f.close()
    else:
        print("dir already exitst")
    
if __name__=='__main__':
    dbcursor = db.connectDatabase()
    projectName = "repositories/bndtools/bndtools"
    genealogyWriteToFile(dbcursor, projectName)
    #cloneRelease = getGenealogyDataByName(dbcursor, projectName)
    #print(cloneRelease)
