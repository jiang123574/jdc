import sqlapi
import json
import requests
import datetime
import hashlib
import hmac
import base64
import GlobalVariable
import pandas as pd


# 获取今天是第几天
def distanceDate():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    months = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
    totalDays = months[month - 1]
    totalDays += day
    if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
        if month > 2:
            totalDays += 1
    return totalDays


# 通过秒数计算时间
def calculatingTime(onlineTime):
    day = 0
    hour = 0
    minute = int(int(onlineTime) / 60)
    second = int(onlineTime) % 60
    if (minute > 60):
        hour = int(minute / 60)
        minute %= 60
    if hour > 24:
        day = int(hour / 24)
        hour %= 24
    return "%s天%s小时%s分钟%s秒" % (day, hour, minute, second)


# 计算authorization
def getAuthorization(body, accessKey):
    totalDays = distanceDate()
    deviceKey = "ios6.5.5iPhone10,115.3.1:%s" % (totalDays)
    deviceKey = hashlib.md5(deviceKey.encode()).hexdigest()
    time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    text = "%spostjson_body%s%s%s%s" % (deviceKey, body, time, accessKey, deviceKey)
    digest = hmac.new(GlobalVariable.hmacKey.encode(), text.encode(), hashlib.sha1).digest()
    decode = base64.b64encode(digest).decode()
    authorization = "smart %s:::%s:::%s" % (accessKey, decode, time)
    return authorization


# 获取设备昵称
def getListAllUserDevices():
    df = []
    url = GlobalVariable.jd_service_url + "listAllUserDevices"
    body = ''
    GlobalVariable.service_headers["Authorization"] = str(getAuthorization(body, GlobalVariable.accessKey))
    res = requests.post(url, params=GlobalVariable.service_pram, headers=GlobalVariable.service_headers, data=body)
    if res.status_code == 200:
        res = res.json()
        resultLists = res["result"][0]["list"]
        for resultList in resultLists:
            device_id = resultList["device_id"]
            device_name = resultList["device_name"]
            feed_id = resultList["feed_id"]
            df.append([device_id, device_name, feed_id])
        return pd.DataFrame(df, columns=['device_id', 'device_name', 'feed_id'])
    else:
        print("Request getListAllUserDevices failed!")


def getControlDevice(feed_id, i):
    url = GlobalVariable.jd_service_url + "controlDevice"
    body = GlobalVariable.service_body % (feed_id, GlobalVariable.cmds[i])
    GlobalVariable.service_headers["Authorization"] = str(getAuthorization(body, GlobalVariable.accessKey))
    res = requests.post(url, params=GlobalVariable.service_pram, headers=GlobalVariable.service_headers, data=body)
    if res.status_code == 200 and res.json()["result"] is not None:
        res = res.json()
        result = json.loads(res["result"])
        streams = result["streams"][0]
        current_value = json.loads(streams["current_value"])
        if current_value.get("data"):
            data = current_value["data"]
            if i == 0:
                pass
            elif i == 1:
                # 上传与下载
                upload = data["upload"]
                download = data["download"]
                bandwidth = data["bandwidth"]
                # return upload, download, bandwidth
            elif i == 2:
                # 运行信息
                if isinstance(data, str):
                    print("无法获取运行信息!")
                    print("信息如下:", data)
                public_ip = data["public_ip"]
                upload = data["upload"]
                cpu = data["cpu"]
                mac = data["mac"]
                rom = data["rom"]
                wanip = data["wanip"]
                romType = data["romType"]
                download = data["download"]
                mem = data["mem"]
                model_name = data["model_name"]
                onlineTime = data["onlineTime"]
                model = data["model"]
                ap_mode = data["ap_mode"]
                sn = data["sn"]
                return public_ip, upload, cpu, mac, rom, wanip, romType, download, mem, model_name, onlineTime, model, ap_mode, sn

            elif i == 3:
                # 插件版本
                if isinstance(data, str):
                    print("无法获取插件信息!")
                    print("信息如下:", data)
                else:
                    pcdn_list = data["pcdn_list"]
                    # print(pcdn_list)
                    status = ""
                    # name = ""
                    cache_size = ""
                    for pcdn_st in pcdn_list:
                        status += f'''{pcdn_st["nickname"]}({pcdn_st["status"]})   '''
                        # name += f'''{pcdn_st["nickname"]}({pcdn_st["name"]})   '''
                        cache_size += f'''{pcdn_st["nickname"]}({str(round(int(pcdn_st["cache_size"]) / 1048 / 1000, 2))}GB)   '''
                    extstorage_exist = data["extstorage_exist"]
                    extstorage_enable = data["extstorage_enable"]
                    board = data["board"]
    else:
        if res.json()["error"] is not None:
            error = res.json()["error"]
            errorCode = error['errorCode']
            errorInfo = error['errorInfo']
            print("错误代码:%s,错误信息:%s" % (errorCode, errorInfo))
        print("Request getControlDevice failed!")

