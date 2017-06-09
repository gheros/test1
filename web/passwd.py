#coding=utf-8
#-*- coding: utf-8 -*-

import random
import string
import smtplib
import email.mime.multipart
import email.mime.text
import os,sys
# import paramiko


def inputpasswd():
    host= input("Enter your host ip:")
    oldpasswd = input("Enter your oldpasswd:")
    print("您的密码为")

#密码生成模块
def saltauto():
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    return salt
#修改机器密码模块
# def cpasswd(oldpasswd,new):
#     port = 22
#     username = 'ubuntu'
#     file = open('ip.list')
#     for line in file:
#         hostname = str(line.split('\t')[0])
#         oldpasswd = str(line.split('\t')[1]).strip()
#         newpasswd = str(line.split('\t')[2]).strip()
#         print("#########################", hostname, "###################")
#         s = paramiko.SSHClient()
#         s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         s.connect(hostname, port, username, oldpasswd)
#         stdin, stdout, sterr = s.exec_command('echo %s | passwd --stdin root' % (newpasswd))
#         print (stdout.read())
#         s.close()
#     file.close()
    # knife ssh 'name:*' 'ls' -x ubuntu -P test12345
    # knife ssh 'name:*' 'echo Ubuntu:new |chpasswd' -x ubuntu -P test12345
    #echo Ubuntu:new |chpasswd
#发件模块
def sentmail(oldpasswd):
    msg=email.mime.multipart.MIMEMultipart()
    msg['from']='我发的'
    msg['to']='给你的'
    msg['subject']='这是一封测试邮件'
    newpasswd=saltauto()
    content='''
    您好，您的密码已修改为
    '''+newpasswd
    txt=email.mime.text.MIMEText(content)
    msg.attach(txt)
    smtp=smtplib
    smtp=smtplib.SMTP()
    smtp.connect('smtp.exmail.qq.com')
    smtp.login('peng.gao@credittone.com','Gp888666')
    smtp.sendmail('peng.gao@credittone.com','peng.gao@credittone.com',str(msg))
    smtp.quit()
    return

if __name__ == '__main__':
    sentmail('111')