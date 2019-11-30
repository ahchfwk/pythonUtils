# -*- coding:utf-8 -*-
# 使用之前请先安装paramiko模块， pip install paramiko
import paramiko

def getCode(filepath, start, end):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('10.141.221.83', 22, 'fdse', 'cloudfdse')
    ftp = client.open_sftp()
    with ftp.open(filepath) as f:
        return ''.join(f.readlines()[start-1:end])

if __name__ == '__main__':
    print getCode('/home/fdse/data/releases1_unzip/JakeWharton/ActionBarSherlock/4.3.0/ActionBarSherlock-4.3.0/actionbarsherlock/src/com/actionbarsherlock/internal/nineoldandroids/animation/PropertyValuesHolder.java',595,609)