# -*- coding:utf-8 -*-

from xml.dom.minidom import parse
from xml.dom import minidom
from xml.etree.ElementTree import ElementTree, Element
'''
DOMTree = parse("end.xml")
root = DOMTree.documentElement
tem = []
remain = []

for ele in root.getElementsByTagName('Edge'):
    sourceDom = ele.getElementsByTagName('SourceWindow')[0]
    targetDom = ele.getElementsByTagName('TargetWindow')[0]
    # print sourceDom.nodeName
    # print sourceDom.getAttribute('Name')
    if sourceDom.getAttribute('Name') != targetDom.getAttribute('Name'):
        tem.append(ele)

for ele in tem:
    sourceDom = ele.getElementsByTagName('SourceWindow')[0]
    targetDom = ele.getElementsByTagName('TargetWindow')[0]
    event = ele.getElementsByTagName('Event')[0]
    if sourceDom.getAttribute('Name') != "LAUNCHER_NODE[]1003" and targetDom.getAttribute('Name') != "LAUNCHER_NODE[]1003":
        if event.getAttribute('Type') == 'click':
            remain.append(ele)

for ele in remain:
    print ele.getAttribute("ID")

'''
tree = ElementTree()
tree.parse('morerout17-simple.xml')

id = 1
for edge in tree.findall('Edge'):
    edge.set('ID', str(id))
    id += 1
    for child in edge.getchildren():
        if child.tag == 'StackOperations':
            edge.remove(child)
            print 'stack'

for edge in tree.findall('Edge'):
    for child in edge.getchildren():
        if child.tag == 'LifecycleCallbacks':
            edge.remove(child)
            print 'life'

tree.write('./test.xml', encoding='utf-8', xml_declaration=False)
