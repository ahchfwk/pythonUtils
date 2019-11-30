# -*- coding:utf-8 -*-

from xml.etree.ElementTree import ElementTree, Element

tree = ElementTree()
tree.parse('morerout17-simple.xml')

id = 1
for edge in tree.findall('Edge'):
    edge.set('ID', str(id))
    id += 1
    for child in edge.getchildren():
        if child.tag == 'StackOperations':
            edge.remove(child)
            print 'delete StackOperations '

for edge in tree.findall('Edge'):
    for child in edge.getchildren():
        if child.tag == 'LifecycleCallbacks':
            edge.remove(child)
            print 'delete LifecycleCallbacks'

tree.write('./test.xml', encoding='utf-8', xml_declaration=False)
