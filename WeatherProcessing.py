#!/usr/bin/python
# -*- coding UTF-8 -*-
import datetime
# @Time     : 2023/2/27 15:06
# @Author   : Nick Huang (nick.huang@ucsz.com)
# @File     : ProcessingDataUnit.py
# Copyright (W) 2023 U.C.S.Z. Corp.
# License: ucsz.com

import urllib.request
import json
import sys
import os

# 处理数据格式


# 将所有方法获取的字串进行拼接
def splicingString():
    strLogAllDate = "\n=================================" + qweatherWeatherJsonToString
    return strLogAllDate


# 获取的7天内的天气json串转换为string格式
# 和风天气接口地址 https://devapi.qweather.com/v7/weather/7d?location=101210101&key=key_value
def qweatherWeatherJsonToString():
    strLogAllDayDate = ""
    key_value = os.environ["QWEATHERAPI_KEY"]  # visualcrossing key
    try:
        ResultBytes = urllib.request.urlopen(
            "https://devapi.qweather.com/v7/weather/7d?location=101210101&key=" + key_value)
        #  Parse the results as JSON
        jsonValues = json.load(ResultBytes)
        # str = str(jsonValues['']) if '' in jsonValues else 0  #
        strCode = int(jsonValues['code']) if 'code' in jsonValues else 400  # 接口返回状态
        if strCode == 200:
            jsonDat = jsonValues['daily'] if 'daily' in jsonValues else '[{}]'
            for i in jsonDat:
                strDayDatetime = str(i['fxDate']) if 'fxDate' in i else '1986-04-01'  # 预报日期
                strDayTempMax = str(i['tempMax']) if 'tempMax' in i else '0.0'  # 预报当天最高温度
                strDayTempMin = str(i['tempMin']) if 'tempMin' in i else '0.0'  #  预报当天最低温度
                strDaySunrise = str(i['sunrise']) if 'sunrise' in i else '06:30'  # 日出时间，在高纬度地区可能为空
                strDaySunset = str(i['sunset']) if 'sunset' in i else '17.30'  # 日落时间，在高纬度地区可能为空
                strDayHumidity = str(i['humidity']) if 'humidity' in i else '00'  # 相对湿度，百分比数值
                strDayUvIndex = str(i['uvIndex']) if 'uvIndex' in i else '1'  # 紫外线强度指数
                strDayTextDay = str(i['textDay']) if 'textDay' in i else '唯一'  # 预报白天天气状况文字描述，包括阴晴雨雪等天气状态的描述
                strDayTextNight = str(i['textNight']) if 'textNight' in i else '0.0'  # 预报晚间天气状况文字描述，包括阴晴雨雪等天气状态的描述
                #  strDay = str(i['']) if '' in i else '0.0'  #
                strLogDay = "\n" + strDayTempMin + "℃" + "  <   " + strDayDatetime + "   <  " + strDayTempMax + "℃" \
                            + "\n日出" + strDaySunrise + "          " + strDaySunset + "日落" \
                            + "\n紫外线" + " -->   " + strDayUvIndex \
                            + "\n相对湿度" + "                     " + strDayHumidity + "%" \
                            + "\n白天 " + " -->   " + strDayTextDay \
                            + "\n夜间 " + " -->   " + strDayTextNight \
                            + "\n---------------------------------"
                strLogAllDayDate = strLogAllDayDate + strLogDay
    except urllib.error.HTTPError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except urllib.error.URLError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    return strLogAllDayDate


# 获取的当前最新天气json串转换为string格式
# 和风天气接口地址 https://devapi.qweather.com/v7/weather/now?location=101210101&key=key_value
def qweatherNewWeatherJsonToString():
    strLogDayDate = ""
    key_value = os.environ["QWEATHERAPI_KEY"]  # visualcrossing key
    try:
        ResultBytes = urllib.request.urlopen(
            "https://devapi.qweather.com/v7/weather/now?location=101210101&key=" + key_value)
        #  Parse the results as JSON
        jsonValues = json.load(ResultBytes)
        # str = str(jsonValues['']) if '' in jsonValues else 0  #
        strCode = int(jsonValues['code']) if 'code' in jsonValues else 400  # 接口返回状态
        if strCode == 200:
            jsonDat = jsonValues['now'] if 'now' in jsonValues else '[{}]'
            strDayObsTime = str(jsonDat['obsTime']) if 'obsTime' in jsonDat else '1986-04-01T00:00+08:00'  # 数据观测时间
            # 格式化时间 将2023-02-02T11:12+08:00 格式化成2023-02-02 11:12:00
            strFormatTime = strDayObsTime[:10] + " " + strDayObsTime[-11:-6] + strDayObsTime[-3:]
            strDayTemp = str(jsonDat['temp']) if 'temp' in jsonDat else '30'  # 当前温度，默认单位：摄氏度
            strDayFeelsLike = str(jsonDat['feelsLike']) if 'feelsLike' in jsonDat else '20'  # 体感温度，默认单位：摄氏度
            strDayHumidity = str(jsonDat['humidity']) if 'humidity' in jsonDat else '00'  # 相对湿度，百分比数值
            strDayText = str(jsonDat['text']) if 'text' in jsonDat else '无'  # 天气状况的文字描述，包括阴晴雨雪等天气状态的描述
            # strLogDay = str(jsonValues) + "\n" + str(jsonDat)
            strLogDay = "\n时间标记" + strFormatTime \
                        + "\n当前温度" + " -->   " + strDayTemp + "℃" \
                        + "\n体感温度" + " -->   " + strDayFeelsLike + "℃" \
                        + "\n相对湿度" + " -->   " + strDayHumidity \
                        + "\n天气状况" + " -->   " + strDayText
            strLogAllDayDate = strLogDayDate + strLogDay
    except urllib.error.HTTPError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except urllib.error.URLError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    return strLogAllDayDate
