#coding=utf-8
from appium import webdriver
import string
import linecache
import os
import array_operations

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.4.2'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['app']='E:\\PythonTest\\app-debug.apk'
#desired_caps['appPackage'] = 'com.android.calculator2'
#desired_caps['appActivity'] = '.Calculator'
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
file = open(r'E:\PythonTest\AppiumClientPython\route_10.txt','r')
num=1
#os.system('adb shell /system/bin/screencap -p /sdcard/screenshot0.png')
#os.system('adb pull /sdcard/screenshot0.png E:\down1')
#在开始时先截一个源屏
#line = input()

while 1:
    string="num:\n"
    line = file.readline()
    if line==string:
        os.system('adb shell /system/bin/screencap -p /sdcard/screenshot' + str(num) + '.png')
        os.system('adb pull /sdcard/screenshot' + str(num) + '.png E:\down1')
        x=1
        num=num+x
        while 1:
            line = file.readline()
            string00 = "\n"
            string1="resource window:\n"
            string2="target window:\n"
            string3="resource_id:\n"
            string4="event_type:\n"


            if line == string1:
                line = file.readline()
                print(line)
            if line == string2:
                line = file.readline()
                print(line)
            if line == string3:
               line = file.readline()
               #find_element_by_id()是appium中寻找按钮的方法
               next1 = driver.find_element_by_id(line.strip())
               next1.click()
               #os.system('adb shell /system/bin/screencap -p /sdcard/screenshot'+str(num)+'.png')
               #os.system('adb pull /sdcard/screenshot'+str(num)+'.png E:\down1')
               # x = 1
               #num = num + x
            if line == string4:
                line = file.readline()
                print(line)
                #else if line == package:
                #    print line,
            #if not line:
            #    break
            #pass  # do something
            if line == string00:
                break



        os.system('adb shell /system/bin/screencap -p /sdcard/screenshot'+str(num)+'.png')
        os.system('adb pull /sdcard/screenshot'+str(num)+'.png E:\down1')
        x=1
        num=num+x
#os.system('adb shell screencap -p/sdcard/screenshot.png')
#os.system('adb pull /sdcard/screenshot.png E:\down')
#os.system('adb shell /system/bin/screencap -p /sdcard/screenshot2.png')
#os.system('adb pull /sdcard/screenshot2.png E:\down2')
    if not line:
        break
    pass  # do something

# -------------------------------------------------------------
switch, path, event = array_operations.getUniquePath('apv.xml')
actList = array_operations.getJumpTypeAndButtonId('apv.xml')
for i in range(len(switch)):
    source = switch[i][0]
    target = switch[i][-1]
    print 'source:'+source, 'target:'+target
    for e in event[i]:
        if e == 'click' or e == 'long_click':
            for act in actList:
                if act[0] == source and act[1] == target:
                    next = driver.find_element_by_id(act[2])
                    next.click()

        else:
            print e+':not click, will be realized...'
# -------------------------------------------------------------

