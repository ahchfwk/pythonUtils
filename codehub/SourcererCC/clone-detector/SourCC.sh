#!/bin/bash

## This is SourcererCC Code Clone AutoExecute Program
## Writen by LS 2017_6_26

Detection_Id=1
Repository_Id=1
Release_Id=1
Detection_Granularity='Functions'
Detection_Percent=0.90

##修改目录权限
## cd /mnt/winE/SourcererCC/clone-detector/input
cd /home/fdse/fwk/SourcererCC/clone-detector/input
chmod -R 777 ./dataset

## cd /mnt/winE/SourcererCC/clone-detector/parser/java
cd /home/fdse/fwk/SourcererCC/clone-detector/parser/java
##程序第一部分运行开始时间
RUN_DATE=`date`
START1=$(date +%s)
## java -jar InputBuilderClassic.jar /mnt/winE/SourcererCC/clone-detector/input/dataset /mnt/winE/SourcererCC/clone-detector/input/query/tokens.file /mnt/winE/SourcererCC/clone-detector/input/bookkeping/headers.file functions c 0 0 10 0 false false false 8
java -jar InputBuilderClassic.jar /home/fdse/fwk/SourcererCC/clone-detector/input/dataset /home/fdse/fwk/SourcererCC/clone-detector/input/query/tokens.file /home/fdse/fwk/SourcererCC/clone-detector/input/bookkeping/headers.file functions java 0 0 10 0 false false false 8

##程序第一部分运行结束时间
END1=$(date +%s)
##计算程序第一部分运行时间
RUN_TIME1=$(( $END1 - $START1 ))

##同上
cd /home/fdse/fwk/SourcererCC/clone-detector
START2=$(date +%s)
java -jar dist/indexbased.SearchManager.jar index 9
END2=$(date +%s)
RUN_TIME2=$(( $END2 - $START2 ))

##同上
cd /home/fdse/fwk/SourcererCC/clone-detector
START3=$(date +%s)
java -jar dist/indexbased.SearchManager.jar search 9
END3=$(date +%s)
RUN_TIME3=$(( $END3 - $START3 ))

#程序总运行时间
RUN_TIME=$(( $RUN_TIME1 + $RUN_TIME2 + $RUN_TIME3))


##新建一个保存Detection信息的文件
touch Detection.file

echo 'The detection file path:'
pwd

##将Detection信息重定向到文件
echo $Detection_Id >> Detection.file
echo $Repository_Id >> Detection.file
echo $Release_Id >> Detection.file
echo $Detection_Granularity >> Detection.file
echo $Detection_Percent >> Detection.file
echo $RUN_DATE >> Detection.file
echo $RUN_TIME >> Detection.file
echo $RUN_TIME1 >> Detection.file
echo $RUN_TIME2 >> Detection.file
echo $RUN_TIME3 >> Detection.file
