#!/usr/bin/python
# -*- coding UTF-8 -*-

# @Time     : 2023/03/03 15:22
# @Author   : Nick Huang (nick.huang@ucsz.com)
# @File     : ExchangeRate.py
# Copyright (W) 2023 U.C.S.Z. Corp.
# License: ucsz.com


import sys
import os
import urllib

import requests


# 获取汇率信息


# 获取以美元USD为基准货币的其他货币信息
# 数据来源：https://www.exchangerate-api.com
# 数据调用接口 https://v6.exchangerate-api.com/v6/ + key_value + /latest/USD
def exchangeRate():
    rateResult = ""
    key_value = os.environ["EXCHANGERATE_KYE"]  # exchangerate-api key
    try:
        response = requests.get("https://v6.exchangerate-api.com/v6/" + key_value + "/latest/USD")
        #  Parse the results as JSON
        jsonData = response.json()
        strCode = jsonData['result'] if 'result' in jsonData else 'error'  # 接口返回状态
        #  print("jsonData:" + str(jsonData))
        if strCode == 'success':
            reteJson = jsonData['conversion_rates'] if 'conversion_rates' in jsonData else '{"CNY": 0.0}'
            rateCNY = reteJson['CNY'] if 'CNY' in reteJson else 0.0  # 换算CNY汇率
            rateResult = "1$ USD                " + str(rateCNY) + "¥ CNY"
    except urllib.error.HTTPError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except urllib.error.URLError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    return rateResult
