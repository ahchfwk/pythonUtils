#! /bin/bash
# -*- coding: UTF-8 -*-

#This is code clone SourcererCC program
#Writen by LS in 2017_7_5
#Modify time in 2017_7_17 and Modify the read directory problem by LS

fatherdir=".."
DetectId=1
DetectGranu="Functions"
DetectPerc=0.80
IFS_old=$IFS
IFS=$'\n'

function SourcererCC(){

        Detection_Id=$1
        Repository_Id=$2
        Release_Id=$3
        Detection_Granularity=$4
        Detection_Percent=$5


        ##修改目录权限
        cd /mnt/winE/SourcererCC/clone-detector/input
        chmod -R 777 ./dataset


        cd /mnt/winE/SourcererCC/clone-detector/parser/java
        ##程序运行日期时间
        RUN_DATE=`date`
        ##程序第一部分运行开始时间
	START1=$(date +%s)
        java -jar InputBuilderClassic.jar /mnt/winE/SourcererCC/clone-detector/input/dataset /mnt/winE/SourcererCC/clone-detector/input/query/tokens.file /mnt/winE/SourcererCC/clone-detector/input/bookkeping/headers.file functions java 0 0 10 0 false false false 8
        ##程序第一部分运行结束时间
        END1=$(date +%s)
        ##计算程序第一部分运行时间
        RUN_TIME1=$(( $END1 - $START1 ))

        ##同上  
        cd /mnt/winE/SourcererCC/clone-detector
        START2=$(date +%s)
        java -jar dist/indexbased.SearchManager.jar index 8
        END2=$(date +%s)
        RUN_TIME2=$(( $END2 - $START2 ))
	##同上  
        cd /mnt/winE/SourcererCC/clone-detector
        START3=$(date +%s)
        java -jar dist/indexbased.SearchManager.jar search 8
        END3=$(date +%s)
        RUN_TIME3=$(( $END3 - $START3 ))

        #程序总运行时间
        RUN_TIME=$(( $RUN_TIME1 + $RUN_TIME2 + $RUN_TIME3))


        ##新建一个保存Detection信息的文件
        touch Detection.txt

        #echo 'The detection file path:'
        #pwd

        ##将Detection信息重定向到文件
        echo $Detection_Id >> Detection.txt
        echo $Repository_Id >> Detection.txt
        echo $Release_Id >> Detection.txt
        echo $Detection_Granularity >> Detection.txt
        echo $Detection_Percent >> Detection.txt
        echo $RUN_DATE >> Detection.txt
        echo $RUN_TIME >> Detection.txt
        echo $RUN_TIME1 >> Detection.txt
        echo $RUN_TIME2 >> Detection.txt
        echo $RUN_TIME3 >> Detection.txt

}


for ffd in ls /home/fdse/Downloads/AndroidRelease/
do
	ProjectId=0	
	if [ -d $ffd ] 
	then
		cd $ffd
		for fd in `ls .`
		do
			if [ -d $fd ]
			then
				cd $fd
				ReleaseId=0
				for d in `ls .`
				do
					#ReleaseId=0
					if [ -d $d ]
					then
						selfpwd=`pwd`
						#echo "$f"
						cp -r $d /mnt/winE/SourcererCC/clone-detector/input/dataset/
							
						python2 /usr/local/sbin/CodeClone/RepositoryPy.py $DetectId $ProjectId $selfpwd
						python2 /usr/local/sbin/CodeClone/ReleasePy.py $DetectId $ProjectId $ReleaseId $selfpwd $d					
						
						#执行Sourcerer
						SourcererCC $DetectId $ProjectId $ReleaseId $DetectGranu $DetectPerc

						#执行Python数据库插入
						python2 /usr/local/sbin/CodeClone/GroupPy.py $DetectId $ProjectId $ReleaseId
						python2 /usr/local/sbin/CodeClone/InsertPy.py
						python2 /usr/local/sbin/CodeClone/BlockPy.py $DetectId $ProjectId $ReleaseId $selfpwd
						python2 /usr/local/sbin/CodeClone/FilePy.py $DetectId $ProjectId $ReleaseId $selfpwd			
						
						#删除每个Release克隆产生的文件
						rm -f /mnt/winE/SourcererCC/clone-detector/Detection.txt
						rm -f /mnt/winE/SourcererCC/clone-detector/input/bookkeping/headers.file
						rm -f -r /mnt/winE/SourcererCC/clone-detector/input/dataset/
						mkdir /mnt/winE/SourcererCC/clone-detector/input/dataset/
						rm -f /mnt/winE/SourcererCC/clone-detector/input/query/tokens.file
						rm -f /mnt/winE/SourcererCC/clone-detector/output8.0/tokensclones_index_WITH_FILTER.txt
						#echo 'Done !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
						#返回项目目录
						cd $selfpwd
						#ReleaseId自增1
						ReleaseId=`expr $ReleaseId + 1`

					fi
					#ReleaseId=`expr $ReleaseId + 1`
				done
				echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
				echo "Clone Done $ProjectId "
				echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
				#项目Id自增1
				ProjectId=`expr $ProjectId + 1`
				cd $fatherdir
			fi	
		done
	fi

done

IFS=$IFS_old

