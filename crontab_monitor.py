#!/usr/bin/python
# -*- coding:utf8 -*-
# Python:          2.7.14
# Platform:        Windows
# blog:            www.k4ubb.com

'''
crontab：
*/10 * * * * python /root/python/crontab_monitor.py
'''

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
import time
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def main(script_path, sleep_time):
    log_path = script_path+'log.txt'
    os.popen("nohup nethogs -t -v 1 > %s 2>&1 &" %log_path)
    pid = os.popen("ps aux | grep nethogs | awk '{print $2}'").readlines()[0].strip()
    time.sleep(sleep_time)
    data = open(log_path,'rb').read().split('Refreshing:')[-1].strip()
    msg = ''.join(os.popen("iftop -t -n -s 3 |tail -9").readlines())
    msg += ''.join(os.popen("cat %s | tail -n %s |awk '{print $1%s$(NF-1)%s}'" %(log_path, len(data.splitlines()), '" --- "', '" kb"')).readlines()[:-1]).strip()
    send_mail(msg+'\ntime: %s' %time.strftime('%m-%d %H:%M:%S',time.localtime(time.time())))
    os.popen("kill -9 %s | :> %s" % (pid, log_path))

def send_mail(msg):
    mail_host="mail.k4ubb.com"
    mail_user="monitor"
    mail_pass="monitor123"
    sender = 'monitor@k4ubb.com'
    receivers = ['admin@k4ubb.com']
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header("monitor", 'utf-8')
    message['To'] =  Header("admin", 'utf-8')
    subject = '流量监控'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print u"邮件发送成功"
    except smtplib.SMTPException:
        print u"Error: 无法发送邮件"

if __name__ == '__main__':
    script_path = '/root/python/' # 脚本路径
    sleep_time = 5 # nethogs每次开启持续时间
    main(script_path, sleep_time)
