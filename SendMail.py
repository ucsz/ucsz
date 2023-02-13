#!/usr/bin/python
# -*- coding UTF-8 -*-

# @Time     : 2023/2/10 14:20
# @Author   : Nick Huang (nick.huang@ucsz.com)
# @File     : SendMail.py
# Copyright (W) 2022 U.C.S.Z. Corp.
# License: ucsz.com

# 发送邮件主要用到了smtplib和email两个模块

import smtplib
from email.utils import formataddr
from email.header import Header
from email.mime.text import MIMEText

# 发送邮件
# fromMail  邮件发件人邮箱账号
# mailPassword  邮件发送账户密码
# mailSMTP  邮件发送SMTP服务器
# toMail 邮件收件人邮箱账号
# subject 邮件标题
# matter  邮件正文文本
def sendMail(fromMail, mailPassword, mailSMTP, toMail, subject, matter):
    msg = MIMEText(matter, 'plain', 'utf-8')
    # msg['From'] = Header('公允居间服务账户', 'utf-8').encode()
    msg['From'] = formataddr((Header('Brokerage service account', 'utf-8').encode(), fromMail))
    # msg['To']接收的是字符串而不是list,如果有多个邮件地址，此处用,分割即可
    # msg['To'] = Header('王工' 'utf-8').encode()
    msg['To'] = formataddr((Header('Transferee', 'utf-8').encode(), toMail))  # Remind the assignee
    msg['Subject'] = Header(subject, 'utf-8').encode()
    try:
        server = smtplib.SMTP_SSL(mailSMTP, 994)
        # server.set_debuglevel(1)  # 设置debug等级，用于调试（不设置不影响发邮件），设置了之后会输出通讯内容
        server.login(fromMail, mailPassword)
        server.sendmail(fromMail, [toMail], msg.as_string())
        server.quit()
        print("Ok，电邮送达成功。")
    except smtplib.SMTPException as e:
        print("Error:电邮丢失或者其他不可达。", e)
