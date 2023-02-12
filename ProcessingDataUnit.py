#!/usr/bin/python
# -*- coding UTF-8 -*-

# @Time     : 2023/2/10 15:06
# @Author   : Nick Huang (nick.huang@ucsz.com)
# @File     : ProcessingDataUnit.py
# Copyright (W) 2022 U.C.S.Z. Corp.
# License: ucsz.com

import urllib.request
import json
import sys

# 处理数据格式

# 获取的天气json串转换为string格式
def weatherJsonToString(jsonValues):
    strResolvedAddress = str(jsonValues['resolvedAddress']) if 'resolvedAddress' in jsonValues else 0  # 解析地址
    #  strAddress = str(jsonValues['address']) if 'address' in jsonValues else 0  # 位置
    strLongitude = str(jsonValues['longitude']) if 'longitude' in jsonValues else 0  # 经度
    strLatitude = str(jsonValues['latitude']) if 'latitude' in jsonValues else 0  # 维度
    #  strTimezone = str(jsonValues['timezone']) if 'timezone' in jsonValues else 0  # 时区
    #  strTzoffset = str(jsonValues['tzoffset']) if 'tzoffset' in jsonValues else 0  # 时区对应夏令时补偿
    #  str = str(jsonValues['']) if '' in jsonValues else 0  #
    strInitHeader = strLongitude + ' ' + strLatitude + ' ' + strResolvedAddress
    strLogInit = "=================================\n" + strInitHeader + "\n================================="
    jsonDat = jsonValues['days'] if 'days' in jsonValues else '[{}]'
    print(strLogInit)
    strLogAllDayDate = ""
    for i in jsonDat:
        strDayDatetime = str(i['datetime']) if 'datetime' in i else '2023-01-01'  # 当前日期
        strDayTempMax = str(i['tempmax']) if 'tempmax' in i else '0.0'  # 区域内最高温度
        strDayTempmin = str(i['tempmin']) if 'tempmin' in i else '0.0'  # 区域内最低温度
        #  strDayTemp = str(i['temp']) if 'temp' in i else '0.0'  # 平均温度
        #  strDayFeelslikemax = str(i['feelslikemax']) if 'feelslikemax' in i else '0.0'  # 体感最高温度
        #  strDayFeelslikemin = str(i['feelslikemin']) if 'feelslikemin' in i else '0.0'  # 体感最低温度
        #  strDayFeelslike = str(i['feelslike']) if 'feelslike' in i else '0.0'  # 体感舒适温度
        #  strDayDew = str(i['dew']) if 'dew' in i else '0.0'  # 露点温度
        strDayHumidity = str(i['humidity']) if 'humidity' in i else '0.0'  # 湿度
        #  strDayPrecip = str(i['precip']) if 'precip' in i else '0.0'  # 降雨
        #  strDayPrecipprob = str(i['precipprob']) if 'precipprob' in i else '0.0'  # 降雨可能性
        strDayPreciptype = i['preciptype'] if 'preciptype' in i else 'null'  # 是否有雨（先返回一个list）
        # 如果有雨就返回Linux中的值，无雨就返回None
        strDayPreciptypeValue = strDayPreciptype if not isinstance(strDayPreciptype, list) else strDayPreciptype[0]
        #  strDaySnow = str(i['snow']) if 'snow' in i else '0.0'  # 是否下雪
        #  strDaySnowdepth = str(i['snowdepth']) if 'snowdepth' in i else '0.0'  # 下雪深度
        #  strDayWindgust = str(i['windgust']) if 'windgust' in i else '0.0'  # 阵风
        #  strDayWindspeed = str(i['windspeed']) if 'windspeed' in i else '0.0'  # 阵风风速
        #  strDayPressure = str(i['pressure']) if 'pressure' in i else '0.0'  # 气压
        #  strDayCloudcover = str(i['cloudcover']) if 'cloudcover' in i else '0.0'  # 云量
        #  strDayVisibility = str(i['visibility']) if 'visibility' in i else '0.0'  # 能见度
        #  strDaySolarradiation = str(i['solarradiation']) if 'solarradiation' in i else '0.0'  # 太阳辐射值
        #  strDaySolarenergy = str(i['solarenergy']) if 'solarenergy' in i else '0.0'  # 辐射指数
        #  strDayUvindex = str(i['uvindex']) if 'uvindex' in i else '0.0'  # 紫外线指数
        #  strDaySevererisk = str(i['severerisk']) if 'severerisk' in i else '0.0'  # 风险
        strDaySunrise = str(i['sunrise']) if 'sunrise' in i else '06:00:00'  # 日出时间
        strDaySunset = str(i['sunset']) if 'sunset' in i else '18:00:00'  # 日落时间
        strDayConditionsTemp = str(i['conditions']) if 'conditions' in i else '0.0'  # 当天天气条件
        strDayConditions = getTranslationJsonToString(strDayConditionsTemp)  # 描述换成中文
        strDayDescriptionTemp = str(i['description']) if 'description' in i else '0.0'  # 天气描述
        strDayDescription = getTranslationJsonToString(strDayDescriptionTemp)  # 描述换成中文
        #  strDay = str(i['']) if '' in i else '0.0'  #
        #  isRain = str(strDayPreciptypeValue) if strDayPreciptypeValue is not None else "无雨"
        isRain = None
        if strDayPreciptypeValue is not None:
            isRain = "有雨 -> " + str(strDayPreciptypeValue)
        else:
            isRain = "无雨"
        strLogDay = strDayTempmin + "℃" + "  <   " + strDayDatetime + "   <  " + strDayTempMax + "℃" \
                    + "\n日出" + strDaySunrise + "          " + strDaySunset + "日落" \
                    + "\n相对湿度" + "                     " + strDayHumidity + "%" \
                    + "\n" + isRain \
                    + "\n" + strDayConditions \
                    + "\n" + strDayDescription \
                    + "\n---------------------------------\n"
        strLogAllDayDate = strLogAllDayDate + strLogDay
    return strLogAllDayDate

#  内容写入文件,传入需要写入文件名,需要写入的内容
def file_in(file_name,number_data):
    print(file_name + "文件准备写入：" + number_data)
    with open('./'+file_name+'.log', 'w', encoding='utf-8') as f:
        f.write(str(number_data))
        f.close()

#  内容写入文件末尾,传入需要写入文件名,需要追加写入的内容
def file_add_content(file_name,number_data):
    with open('./'+file_name+'.log', 'a', encoding='utf-8') as f:
        f.write('\n' + str(number_data))
        f.close()

# 传入含空格的字符串，并将字符串中的空格替换成'%20'
def spaceCharacterConvertString(conString):
    replaceString = " "
    replace_dict = {k: "%20" for k in replaceString}
    dataResult = str(conString)
    for k, v in replace_dict.items():
        dataResult = dataResult.replace(k, v)
    # print("dataResult:" + dataResult)
    return dataResult

# 获取的翻译接口返回的json串，截取串中的中文翻译结果字串
def translationJsonToString(enJsonString):
    translateResult = None
    #  Parse the results as JSON
    strErrorCode = int(enJsonString['errorCode']) if 'errorCode' in enJsonString else -1  # 接口返回状态
    print("strErrorCode:" + str(strErrorCode))
    if strErrorCode == 0:
        translateDate = list(enJsonString['translateResult']) if 'translateResult' in enJsonString else '[]'
        if len(translateDate) > 0:
            tgt = str(translateDate[0][0]['tgt'])
            translateResult = tgt
    return translateResult

# 传入英文文本并调用的翻译接口返回json串，截取串中的中文翻译结果字串
def getTranslationJsonToString(enString):
    translateResult = None
    inString = spaceCharacterConvertString(enString)
    try:
        resultJson = urllib.request.urlopen(
            # "http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=en&tl=zh-CN&q=" + enString
            "https://fanyi.youdao.com/translate?&doctype=json&type=EN2ZH_CN&i=" + inString)
        #  Parse the results as JSON
        jsonData = json.load(resultJson)
        strErrorCode = int(jsonData['errorCode']) if 'errorCode' in jsonData else -1  # 接口返回状态
        # print("strErrorCode:" + str(strErrorCode))
        if strErrorCode == 0:
            translateDate = list(jsonData['translateResult']) if 'translateResult' in jsonData else '[]'
            if len(translateDate) > 0:
                tgt = str(translateDate[0][0]['tgt'])
                translateResult = tgt
    except urllib.error.HTTPError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except urllib.error.URLError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    return translateResult
