# -*- coding:utf-8 -*-
#!/usr/bin/python

##################################################
#
# HRBB OA SIGN BOT
# deviceId/deviceInfo需抓包获取后自行替换（注掉不送也行）
# 196行用户名密码自行替换或去掉197行注释从键盘获取
#
##################################################

import datetime
import getpass
import json
import logging
import random
import time
import uuid

import requests
from chinese_calendar import is_workday

logging.basicConfig(filename='oa_sign.log', level=logging.INFO,
                    format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%Y-%m-%d %a %H:%M:%S')

global curDate
curDate = datetime.datetime.now().strftime("%Y-%m-%d")

global nextDate
nextDate = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")

global reqHeader
reqHeader = {'Accept': '*/*',
             'X-Requested-With': 'XMLHttpRequest',
             'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
             'Accept-Encoding': 'gzip, deflate',
             'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
             'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Qiyuesuo/physicalSDK/E-Mobile7/7.0.60.20220124 NetType/4G Language/zh',
             'Origin': 'http://goa.hrbb.com.cn:10445'}

global longitude
longitude = str(random.uniform(126.5730, 126.5745))

global latitude
latitude = str(random.uniform(45.739, 45.740))


def getLoginInfoFromKB():
    emplId = ''
    passwd = ''
    while len(emplId) <= 0 or len(passwd) <= 0:
        emplId = input('\nOA登录用户名：')
        passwd = getpass.getpass('\n密码：')
    else:
        return emplId, passwd


def getCookies(emplId, passwd):
    resp = requests.post(url='http://goa.hrbb.com.cn:10445/api/hrm/login/checkLogin',
                         headers=reqHeader,
                         data=(('loginid', emplId),
                               ('userpassword', passwd),
                               ('islanguid', '1'),
                               ('logintype', '1')),
                         timeout=30)

    if(resp.status_code == 200):
        loginResp = json.loads(resp.text)
        if(loginResp['msgcode'] == '0' and loginResp['loginstatus'] == 'true'):
            cookieDict = requests.utils.dict_from_cookiejar(resp.cookies)
            logging.info('Cookie获取成功：' + str(cookieDict))
            cookieDict['__randcode__'] = str(uuid.uuid4())
            logging.info('Cookie添加伪随机数：' + cookieDict['__randcode__'])
            return cookieDict
        else:
            logging.error('Cookie获取失败：' + loginResp['msg'])
            return None
    else:
        logging.error('Cookie获取失败：' + resp.text)
        return None


def signOn(cookie):
    # minutesMargin = int((time.time() - time.mktime(time.strptime(curDate + " 00:06", "%Y-%m-%d %H:%M"))) / 60)
    punchResp = requests.post(url='http://goa.hrbb.com.cn:10445/api/hrm/kq/attendanceButton/punchButton',
                              headers=reqHeader,
                              cookies=cookie,
                              data=(('date', curDate),
                                    ('isfirstsign', '1'),
                                    ('belongdate', curDate),
                                    ('belongtime', '08:31'),
                                    ('datetime', curDate + ' 08:31:00'),
                                    ('signSection', curDate + ' 00:06:00#' + curDate + ' 10:01:59'),
                                    ('signSectionTime', curDate + ' 00:06:00'),
                                    ('signSectionEndTime', curDate + ' 10:01:59'),
                                    ('canSignTime', '00:06'),
                                    ('canSignEndTime', '10:01'),
                                    ('type', 'on'),
                                    ('across', '0'),
                                    ('min', '505'),
                                    ('islastsign', '1'),
                                    ('isYellow', '0'),
                                    ('isPunchOpen', '1'),
                                    ('isacross', '0'),
                                    ('pre', '0'),
                                    ('active', '1'),
                                    ('needSign', '1'),
                                    ('workmins', '539'),
                                    ('min_next', '90'),
                                    ('serialid', '9'),
                                    ('signAcross', '0'),
                                    ('signAcross_next', '0'),
                                    ('time', '08:31'),
                                    ('locationshowaddress', '0'),
                                    ('longitude', longitude),
                                    ('latitude', latitude),
                                    ('position', '中国哈尔滨市道里区上江街888号哈尔滨银行总部大厦'),
                                    ('positionInfo', '{"status":"1","time":' + str(int(round(time.time() * 1000))) + ',"clientType":"iPhone","province":"黑龙江省","country":"中国","district":"道里区","POIName":"哈尔滨银行总部大厦","street":"上江街","speed":-1,"latitude":' + latitude +
                                     ',"city":"哈尔滨市","adcode":"230102","accuracy":35,"altitude":' + longitude + ',"number":"888号","errMsg":"getLocation:ok","longitude":126.57424858940972,"locationType":"Amap","AOIName":"哈尔滨银行总部大厦","errCode":0,"citycode":"0451","address":"中国哈尔滨市道里区上江街888号哈尔滨银行总部大厦"}'),
                                    ('locationid', '9'),
                                    ('sid', ''),
                                    ('mac', ''),
                                    # ('deviceId', 'NOTE_REPLACE_THIS_STRING_WITH_REAL_DEVICE_ID'),
                                    # ('deviceInfo', '{"status":"1","clientType":2,"clientFont":"1","clientModel":"iPhone","clientVersion":"7.0.60.20220124","clientLang":"zh","osVersion":"15.6","deviceId":"NOTE_REPLACE_THIS_STRING_WITH_REAL_DEVICE_ID","networkType":"4G","SSID":"","BSSID":"","isDark":false,"secondsFromGMT":28800,"errCode":0,"clientTheme":"#ff861d","errMsg":"getClientInfo:ok"}'),
                                    ('browser', 'emobile'),
                                    ('_ec_ismobile', 'true'),
                                    ('_ec_browser', 'EMobile'),
                                    ('_ec_browserVersion', '7.0.60.20220124'),
                                    ('_ec_os', 'iOS'),
                                    ('_ec_osVersion', '15.6'),
                                    ('ismobile', '1')),
                              timeout=30)
    if(punchResp.status_code == 200):
        punchRespObj = json.loads(punchResp.text)
        if(punchRespObj['kqstatus'] == '0' and punchRespObj['success'] == '1'):
            logging.info('上班打卡成功:' +
                         punchRespObj['signdate'] + ' ' + punchRespObj['signtime'])
        else:
            logging.error(
                '上班打卡失败：' + punchRespObj.get('message', '服务器未返回失败原因'))
    else:
        logging.error('上班打卡失败：' + punchResp.text)


def signOff(cookie):
    # minutesMargin = int((time.time() - time.mktime(time.strptime(curDate + " 00:06", "%Y-%m-%d %H:%M"))) / 60)
    punchResp = requests.post(url='http://goa.hrbb.com.cn:10445/api/hrm/kq/attendanceButton/punchButton',
                              headers=reqHeader,
                              cookies=cookie,
                              data=(('date', curDate),
                                    ('belongdate', curDate),
                                    ('belongtime', '17:30'),
                                    ('datetime', curDate + ' 17:30:00'),
                                    ('signSectionBeginTime', curDate + ' 10:30:00'),
                                    ('signSectionTime', nextDate + ' 00:00:59'),
                                    ('signSection', curDate + ' 10:30:00#' + nextDate + ' 00:00:59'),
                                    ('canSignBeginTime', '10:30'),
                                    ('canSignTime', '00:00'),
                                    ('type', 'off'),
                                    ('across', '0'),
                                    ('min', '390'),
                                    ('islastsign', '1'),
                                    ('isYellow', '0'),
                                    ('isPunchOpen', '1'),
                                    ('isacross', '0'),
                                    ('pre', '0'),
                                    ('active', '1'),
                                    ('needSign', '1'),
                                    ('workmins', '539'),
                                    ('min_next', '420'),
                                    ('serialid', '9'),
                                    ('signAcross', '1'),
                                    ('signAcross_next', '0'),
                                    ('time', '17:30'),
                                    ('locationshowaddress', '1'),
                                    ('longitude', longitude),
                                    ('latitude', latitude),
                                    ('position', '中国哈尔滨市道里区上江街888号哈尔滨银行总部大厦'),
                                    ('positionInfo', '{"status":"1","time":' + str(int(round(time.time() * 1000))) + ',"clientType":"iPhone","province":"黑龙江省","country":"中国","district":"道里区","POIName":"哈尔滨银行总部大厦","street":"上江街","speed":-1,"latitude":' + latitude +
                                     ',"city":"哈尔滨市","adcode":"230102","accuracy":35,"altitude":'+longitude+',"number":"888号","errMsg":"getLocation:ok","longitude":126.57437445746528,"locationType":"Amap","AOIName":"哈尔滨银行总部大厦","errCode":0,"citycode":"0451","address":"中国哈尔滨市道里区上江街888号哈尔滨银行总部大厦"}'),
                                    ('locationid', '9'),
                                    ('sid', ''),
                                    ('mac', ''),
                                    # ('deviceId', 'NOTE_REPLACE_THIS_STRING_WITH_REAL_DEVICE_ID'),
                                    # ('deviceInfo', '{"status":"1","clientType":2,"clientFont":"1","clientModel":"iPhone","clientVersion":"7.0.60.20220124","clientLang":"zh","osVersion":"15.6","deviceId":"NOTE_REPLACE_THIS_STRING_WITH_REAL_DEVICE_ID","networkType":"4G","SSID":"","BSSID":"","isDark":false,"secondsFromGMT":28800,"errCode":0,"clientTheme":"#ff861d","errMsg":"getClientInfo:ok"}'),
                                    ('browser', 'emobile'),
                                    ('_ec_ismobile', 'true'),
                                    ('_ec_browser', 'EMobile'),
                                    ('_ec_browserVersion', '7.0.60.20220124'),
                                    ('_ec_os', 'iOS'),
                                    ('_ec_osVersion', '15.6'),
                                    ('ismobile', '1')),
                              timeout=30)
    if(punchResp.status_code == 200):
        punchRespObj = json.loads(punchResp.text)
        if(punchRespObj['kqstatus'] == '2' and punchRespObj['status'] == '1'):
            logging.info('下班打卡成功:' +
                         punchRespObj['signdate'] + ' ' + punchRespObj['signtime'])
        else:
            logging.error(
                '下班打卡失败：' + punchRespObj.get('message', '服务器未返回失败原因'))
    else:
        logging.error('下班打卡失败：' + punchResp.text)


if(__name__ == '__main__'):
    # userInfo = ('880000', 'OA_PASSWORD')
    userInfo = getLoginInfoFromKB()
    logging.info('============================================')
    if (is_workday(datetime.date.today()) and time.localtime().tm_hour < 12):
        logging.info(userInfo[0] + '上班打卡')
        cookies = getCookies(emplId=userInfo[0], passwd=userInfo[1])
        if not (cookies is None):
            signOn(cookie=cookies)

    elif(is_workday(datetime.date.today()) and time.localtime().tm_hour >= 12):
        logging.info(userInfo[0] + '下班打卡')
        cookies = getCookies(emplId=userInfo[0], passwd=userInfo[1])
        if not (cookies is None):
            signOff(cookie=cookies)

    else:
        logging.info(datetime.date.today().strftime('%Y-%m-%d') + '休息日无需打卡')
