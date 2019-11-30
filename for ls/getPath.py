# -*- coding:utf-8 -*-

def print_all_path_from_martix(activityMatrix): 
    mat = activityMatrix  # activityMatrix就是存储activity的二维字典
    pathList = []  # 存储已有路径
    for key in mat.keys():
        mat[key][key] = []  # 这里将每个activity跳向自己的路径置为空list
        pathList.append([key])  # pathList存储已有路径，已有的每条路径都用list表示，这里将pathList初始值设为各个activity表示出发点

    getAllPath(pathList, mat, 1)  # 调用该该函数，该函数递归的查找mat中所有activity路径，并将结果存到pathList中

    switch = []
    path = []
    event = []
    for key, value in mat.items():
        for key2 in value.keys():
            result = getShortestPath(key, key2, pathList, len(mat))  # 该函数从存储所有路径的pathList中找activity间的最短路径
            
            # print key + '->' + key2 + ':',  # 以下几行以某种格式将结果打印出来，这不重要
            if not result:
                pass
                # print 'no path'
            else:
                switch.append([key, key2])
                path.append(result)
                # print result, ',', 'eventType:',
                tem = []
                for i in range(len(result) - 1):
                    # print mat[result[i]][result[i + 1]][0],
                    tem.append(mat[result[i]][result[i + 1]][0])
                # print ''
                event.append(tem)
    return switch, path, event

def getAllPath(pathList, mat, pathLength):
    '''该函数找出所有的不循环的路径'''
    updateList = []  # 存储每次迭代要更新的路径，比如第一次存储的时找到的所有长度为2的路径，第二次存储的时找到的所有长度为3的路径...

    for key in mat.keys():
        for path in pathList:
            if len(path) == pathLength and key not in path and mat[path[-1]][key]:  # 每次只找长度等于pathLength的path的后续路径
                add = path[:]
                add.append(key)
                
                updateList.append(add)

    pathList += updateList

    pathLength += 1  # 初始pathLength是1，以后每次迭代加一，到其大于mat长度(即activity个数)时，停止迭代
    if pathLength <= len(mat):
        getAllPath(pathList, mat, pathLength)


def getShortestPath(act1, act2, pathList, MaxPathlength):
    '''该函数从已有的所有路径里，查找最短路径'''
    for i in range(2, MaxPathlength + 1):  # 每次找长度等于i的路径，从2开始，直到最大path长度(即MaxPathlength)为止
        for path in pathList:
            if len(path) == i and path[0] == act1 and path[-1] == act2:  # 对于pathList里的每条路径，如果path的起点和重点至我们需要的，就返回这个结果
                return path
    return None  # 如果循环结束也没返回，说明没有满足要求的path，那就返回None


if __name__ == '__main__':
    testMatrix = {
        'A': {
            'A': ['aa'],
            'B': ['ab'],
            'C': [],
            'D': ['ad', 'ad2']
        },
        'B': {
            'A': ['ba'],
            'B': ['bb'],
            'C': ['bc', 'bc2'],
            'D': []
        },
        'C': {
            'A': [],
            'B': [],
            'C': ['cc'],
            'D': ['cd', 'cd2', 'cd3']
        },
        'D': {
            'A': ['da', 'da2'],
            'B': [],
            'C': ['dc'],
            'D': ['dd']
        }
    }

    a,b,c = print_all_path_from_martix(testMatrix)
    print a, b, c
