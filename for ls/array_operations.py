# -*- coding:utf-8 -*-

from xml.dom.minidom import parse
from xml.dom import minidom
from xml.etree.ElementTree import ElementTree, Element
import getPath


# -------------------------------------------------------
def getJumpTypeAndButtonId(xmlPath):
    DOMTree = parse(xmlPath)
    tem = []
    result = []
    for ele in root.getElementsByTagName('Edge'):
        sourceDom = ele.getElementsByTagName('SourceWindow')[0]
        targetDom = ele.getElementsByTagName('TargetWindow')[0]
        if sourceDom.getAttribute('Type') == 'ACT' and targetDom.getAttribute(
                'Type') == 'ACT':
            tem.append(ele)

    for ele in tem:
        sname = ele.getElementsByTagName('SourceWindow')[0].getAttribute(
            'Name').encode('utf-8')
        tname = ele.getElementsByTagName('TargetWindow')[0].getAttribute(
            'Name').encode('utf-8')
        eventType = ele.getElementsByTagName('Event')[0].getAttribute(
            'Type').encode('utf-8')
        buttonId = 'cx.hell.android.pdfview:id/' + ele.getElementsByTagName(
            'Event')[0].getAttribute('idName').encode('utf-8')
        result.append([sname, tname, eventType, buttonId])

    return result


def getUniquePath(xmlPath):
    d = {}
    DOMTree = parse(xmlPath)
    root = DOMTree.documentElement
    for ele in root.getElementsByTagName('Edge'):
        sourceDom = ele.getElementsByTagName('SourceWindow')[0]
        targetDom = ele.getElementsByTagName('TargetWindow')[0]

        if sourceDom.getAttribute('Type') == 'ACT' and targetDom.getAttribute(
                'Type') == 'ACT':
            tem.append(ele)
    # 读取每一条边，创建只有sourcewindow的字典
    for ele in tem:
        sourceDom = ele.getElementsByTagName('SourceWindow')[0]
        d[sourceDom.getAttribute('Name').encode('utf-8')] = {}

    # 读取每一条边，创建有sourcewindow，targetwindow的字典
    for ele in tem:
        targetDom = ele.getElementsByTagName('TargetWindow')[0]
        for values in d.values():
            values[targetDom.getAttribute('Name').encode('utf-8')] = []

    #读取所有的跳转方式放进去
    for ele in tem:
        sourceDom = ele.getElementsByTagName('SourceWindow')[0]
        targetDom = ele.getElementsByTagName('TargetWindow')[0]
        event = ele.getElementsByTagName('Event')[0]
        eventType = event.getAttribute('Type')
        d[sourceDom.getAttribute('Name').encode('utf-8')][
            targetDom.getAttribute('Name').encode('utf-8')].append(
                eventType.encode('utf-8'))
    a,b,c = getPath.print_all_path_from_martix(d)
    return a,b,c


# -------------------------------------------------------
DOMTree = parse("apv.xml")
root = DOMTree.documentElement
#存放了只为ACT的边
tem = []
remain = []
#装所有的窗口只是ACT的name，包括重复的
oldact = []
#装删除重复后的name
act = []
#对每一条边
for ele in root.getElementsByTagName('Edge'):
    sourceDom = ele.getElementsByTagName('SourceWindow')[0]
    targetDom = ele.getElementsByTagName('TargetWindow')[0]

    if sourceDom.getAttribute('Type') == 'ACT' and targetDom.getAttribute(
            'Type') == 'ACT':
        tem.append(ele)

#对tem数组里的每一条边再做筛选
for ele in tem:
    sourceDom = ele.getElementsByTagName('SourceWindow')[0]
    targetDom = ele.getElementsByTagName('TargetWindow')[0]

    oldact.append(sourceDom.getAttribute('Name'))
    oldact.append(targetDom.getAttribute('Name'))

#删除冗余的activity
for x in oldact:
    if x not in act:
        act.append(x)

for ele in act:
    #输出所有的activity的name
    print(ele)

num = len(act)
#一共有num个ACT，也就是应该创建的list为num行num列的
print(num)

d = {}
#读取每一条边，创建只有sourcewindow的字典
for ele in tem:
    sourceDom = ele.getElementsByTagName('SourceWindow')[0]
    targetDom = ele.getElementsByTagName('TargetWindow')[0]
    # a=ele.getElementsByTagName('Event')[0].getAttribute('Type')
    d[sourceDom.getAttribute('Name').encode('utf-8')] = {}
    # print(a)

# 读取每一条边，创建有sourcewindow，targetwindow的字典
for ele in tem:
    sourceDom = ele.getElementsByTagName('SourceWindow')[0]
    targetDom = ele.getElementsByTagName('TargetWindow')[0]
    for values in d.values():
        values[targetDom.getAttribute('Name').encode('utf-8')] = []
    # for values in d.values():
    #     values[targetDom.getAttribute('Name').encode('utf-8')].append(a.encode('utf-8'))

    #读取所有的跳转方式放进去
for ele in tem:
    sourceDom = ele.getElementsByTagName('SourceWindow')[0]
    targetDom = ele.getElementsByTagName('TargetWindow')[0]
    event = ele.getElementsByTagName('Event')[0]
    type = event.getAttribute('Type')
    d[sourceDom.getAttribute('Name').encode('utf-8')][targetDom.getAttribute(
        'Name').encode('utf-8')].append(type.encode('utf-8'))
#输出用字典存储的各个activity之间的直接路径的跳转方式
print(d)

getPath.print_all_path_from_martix(d)
#先仅仅对click进行实现

print '-------------------------'
a,b,c = getUniquePath('apv.xml')
print a
print b
print c
for i in getJumpTypeAndButtonId('apv.xml'):
    print i