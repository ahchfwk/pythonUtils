# -*- coding:utf-8 -*-
"""created by fwk
   2018/09/03
   parse nicad result
"""
from xml.dom.minidom import parse
from xml.dom import minidom
from collections import namedtuple


def parseXml(xmlfile):
    try:
        result = {}
        dom = parse(xmlfile).documentElement
        for group in dom.getElementsByTagName("class"):
            #print group.getAttribute("classid")
            instances = []
            instance = namedtuple("ins", "path start end")
            for i in group.getElementsByTagName("source"):
                instances.append(instance(i.getAttribute("file"), i.getAttribute("startline"), i.getAttribute("endline")))
            result[group.getAttribute("classid")] = tuple(instances)
        return result
    except Exception:
        return None

if __name__ == "__main__":
    s = parseXml("JHotDraw54b1_functions-clones-0.30-classes.xml")
    for k,v in s.items():
        print k, "----------"
        for i in v:
            print i