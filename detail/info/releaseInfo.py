####################################
# infomation about each release
# author niko -*- date 07-26-2018
####################################

class CloneInfo:
    def __init__(self, groupID, methodID):
        self.groupID = groupID
        self.methodID = methodID

class ReleaseInfo:
    def __init__(self, name):
        self.versionName = name
        self.cloneGroupDict = {}

    def addInfo(self, info):
        if(info.groupID in self.cloneGroupDict):
            self.cloneGroupDict[info.groupID].append(info.methodID)
        else:
            self.cloneGroupDict[info.groupID] = self.getInfoList()
            self.cloneGroupDict[info.groupID].append(info.methodID)

    def getInfoList(self):
        infoList = []
        return infoList

  
