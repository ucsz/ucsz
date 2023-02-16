#!/usr/bin/python
# -*- coding UTF-8 -*-

# @Time     : 2023/2/10 11:32
# @Author   : Nick Huang (nick.huang@ucsz.com)
# @File     : visualcrossing.py
# Copyright (W) 2022 U.C.S.Z. Corp.
# License: ucsz.com
import time
import urllib.request
import sys
import os
import json
import SendMail
import ProcessingDataUnit

maillog = ProcessingDataUnit.splicingString()
to_addr = os.environ["MASTER_MAIL_SMTP_TOADDRESS"]  # 接收邮箱
mail_arg = os.environ["MASTER_MAIL_SMTP_163QY_SSL"]  # 发送协议地址
# mail_port = os.environ["MASTER_MAIL_SMTP_SSL_PORT"]  # 发送协议端口
mail_account = os.environ["MASTER_MAIL_SMTP_FROMADDRESS"]  # 发送邮件账号
mail_password = os.environ["MASTER_MAIL_SMTP_163QY_PASSWORD"]  # 发送邮件账号密码
strSub = '出行前置信息之天气汇总' + time.strftime("%Y%m%d%H%M%S%p")  # 邮件标题
SendMail.sendMail(mail_account, mail_password, mail_arg, to_addr, strSub, str(maillog))
ProcessingDataUnit.file_in("weather", maillog)
