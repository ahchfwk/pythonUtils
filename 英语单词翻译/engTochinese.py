# -*- coding:utf-8 -*-

import urllib2
import re


def translate(word):
    url = "http://dict.youdao.com/w/eng/%s/#keyfrom=dict2.index"
    request = urllib2.Request(url % word)
    response = urllib2.urlopen(request)
    response = response.read()

    pattern = re.compile(r'<div class="trans-container">\s+<ul>\s+<li>(.{1,50}?)</li>\s+<li>(.{1,50}?)</li>\s+<li>(.{1,50}?)</li>.*?</ul>', re.S)
    pattern2 = re.compile(r'<div class="trans-container">\s+<ul>\s+<li>(.{1,50}?)</li>\s+<li>(.{1,50}?)</li>.*?</ul>', re.S)
    pattern3 = re.compile(r'<div class="trans-container">\s+<ul>\s+<li>(.{1,50}?)</li>.*?</ul>', re.S)
    soundmarkPattern = re.compile(r'</span>\s+<span class="pronounce">美\s+<span class="phonetic">(.*?)</span>', re.S)
    result = re.findall(pattern, response)
    result2 = re.findall(pattern2, response)
    result3 = re.findall(pattern3, response)
    soundmark = re.findall(soundmarkPattern, response)

    if result:
        if soundmark:
            with open("eng.txt","a") as f:
                f.write(word+"  "+soundmark[0]+result[0][0]+" "+result[0][1]+" "+result[0][2]+"\n")
        else:
            with open("eng.txt","a") as f:
                f.write(word+"  "+result[0][0]+" "+result[0][1]+" "+result[0][2]+"\n")
    elif result2:
        if soundmark:
            with open("eng.txt","a") as f:
                f.write(word+"  "+soundmark[0]+result2[0][0]+" "+result2[0][1]+"\n")
        else:
            with open("eng.txt","a") as f:
                f.write(word+"  "+result2[0][0]+" "+result2[0][1]+"\n")
    elif result3:
        if soundmark:
            with open("eng.txt","a") as f:
                f.write(word+"  "+soundmark[0]+result3[0]+"\n")
        else:
            with open("eng.txt","a") as f:
                f.write(word+"  "+result3[0]+"\n")


def transBat(wordfile):
    with open(wordfile, "r") as f:
        wordlist = f.readlines()
        wordlist = [x.strip() for x in wordlist]
        for w in wordlist:
            translate(w)


if __name__ == "__main__":
    transBat("word.txt")
    # translate("paralyze")