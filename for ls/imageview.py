#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
import json

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("S_3.xml")
root = DOMTree.documentElement
nodes = root.getElementsByTagName("node")
parent = []
grand = []

layout = ['android.widget.LinearLayout',
          'android.widget.RelativeLayout', 'android.widget.FrameLayout']
ln = len(nodes)
for i in range(1, ln - 1):
    if nodes[i].getAttribute('class') == 'android.widget.ImageView':
        if nodes[i - 1].getAttribute('class') == 'android.widget.ImageView' and nodes[i + 1].getAttribute('class') == 'android.widget.ImageView':
            p = nodes[i].parentNode
            if p.getAttribute('class') in layout and p not in parent:
                parent.append(p)

for i in range(2, ln - 2):
    if nodes[i].getAttribute('class') in layout and len(nodes[i].childNodes) > 1 and hasattr(nodes[i].childNodes[1], 'getAttribute') and nodes[i].childNodes[1].getAttribute('class') == 'android.widget.ImageView':
        if nodes[i - 2].getAttribute('class') in layout and len(nodes[i - 2].childNodes) > 1 and hasattr(nodes[i - 2].childNodes[1], 'getAttribute') and nodes[i - 2].childNodes[1].getAttribute('class') == 'android.widget.ImageView':
            if nodes[i + 2].getAttribute('class') in layout and len(nodes[i + 2].childNodes) > 1 and hasattr(nodes[i + 2].childNodes[1], 'getAttribute') and nodes[i + 2].childNodes[1].getAttribute('class') == 'android.widget.ImageView':
                p = nodes[i].parentNode
                # 防止跨度过大
                if nodes[i].parentNode == nodes[i - 2].parentNode == nodes[i + 2].parentNode:
                    if p not in grand:
                        grand.append(p)
count = 1


f = open('ls.json', 'w')
tem = {}

for i in parent:
    print '------------------%d------------------' % count

    for j in i.childNodes:
            # if j.nodeType == 1:
            #     a = j.getAttribute('bounds').split(',')[1].split(']')[0]
            #     b = j.getAttribute('bounds').split(',')[2][:-1]
        if j.nodeType == 1:
            print j.getAttribute('scrollable'), j.getAttribute('bounds')
            print j.getAttribute('bounds').split(',')[1].split(']')[0], j.getAttribute('bounds').split(',')[2][:-1]
            if int(j.getAttribute('bounds').split(',')[1].split(']')[0]) < 266 and int(j.getAttribute('bounds').split(',')[2][:-1]) < 266:
                tem[count] = [j.getAttribute('scrollable'), 'top']
                print "top"
            elif int(j.getAttribute('bounds').split(',')[1].split(']')[0]) > 266 and int(j.getAttribute('bounds').split(',')[1].split(']')[0]) < 532 and int(j.getAttribute('bounds').split(',')[2][:-1]) > 266 and int(j.getAttribute('bounds').split(',')[2][:-1]) < 532:
                print 'middle'
                tem[count] = [j.getAttribute('scrollable'), 'middle']
            elif int(j.getAttribute('bounds').split(',')[1].split(']')[0]) > 532 and int(j.getAttribute('bounds').split(',')[2][:-1]) > 532:
                print "bottom"
                tem[count] = [j.getAttribute('scrollable'), 'bottom']
    count += 1
    print '---------------------------------------\n'

for i in grand:
    print '------------------%d------------------' % count

    for j in i.childNodes:
        # if j.nodeType == 1:
        #     a = j.childNodes[1].getAttribute('bounds').split(',')[1].split(']')[0]
        #     b = j.childNodes[1].getAttribute('bounds').split(',')[2][:-1]
        if j.nodeType == 1:
            print j.childNodes[1].getAttribute('scrollable'), j.childNodes[1].getAttribute('bounds')
            print j.childNodes[1].getAttribute('bounds').split(',')[1].split(']')[0], j.childNodes[1].getAttribute('bounds').split(',')[2][:-1]
            if int(j.childNodes[1].getAttribute('bounds').split(',')[1].split(']')[0]) < 266 and int(j.childNodes[1].getAttribute('bounds').split(',')[2][:-1]) < 266:
                print "top"
                tem[count] = [j.getAttribute('scrollable'), 'top']
            elif int(j.childNodes[1].getAttribute('bounds').split(',')[1].split(']')[0]) > 266 and int(j.childNodes[1].getAttribute('bounds').split(',')[1].split(']')[0]) < 532 and int(j.childNodes[1].getAttribute('bounds').split(',')[2][:-1]) > 266 and int(j.childNodes[1].getAttribute('bounds').split(',')[2][:-1]) < 532:
                print 'middle'
                tem[count] = [j.getAttribute('scrollable'), 'middle']
            else:
                print "bottom"
                tem[count] = [j.getAttribute('scrollable'), 'bottom']
    count += 1
    print '-------------------------------------\n'


json.dump(tem, f)
f.close()
