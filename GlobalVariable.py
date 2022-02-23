import os
import configparser
# 全局参数
# API
jd_base_url = "https://router-app-api.jdcloud.com/v1/regions/cn-north-1/"
jd_service_url = "https://gw.smart.jd.com/f/service/"

# RequestHeader
headers = {
    "x-app-id": "996",
    "Content-Type": "application/json"
}

accessKey = "b8f9c108c190a39760e1b4e373208af5cd75feb4"

service_headers = {
    "tgt": "JDRouterPush",
    "Authorization": "JDRouterPush",
    "accesskey": accessKey,
    "pin": "JDRouterPush",
    "appkey": "996",
    "User-Agent": "ios",
    "Host": "gw.smart.jd.com"
}

cmds = [
    "get_device_list",  # 获取设备列表 在线与离线的客户端状态
    "get_router_status_info",  # 获取路由器状态信息 上传与下载
    "get_router_status_detail",  # 获取路由器版本 mac  sn  上传  下载  cpu  路由在线时间(秒)  wanip  内存
    "jdcplugin_opt.get_pcdn_status",  # 获取路由器插件版本   缓存大小
    "reboot_system"  # 重启路由器
]

# 请求参数
# service_pram = {
#     "hard_platform": 'MI 6',
#     "app_version": "6.5.5",
#     "plat_version": 9,
#     "channel": "jdCloud",
#     "plat": "Android"
# }

service_pram = {
    "hard_platform": 'iPhone10,1',
    "app_version": "6.5.5",
    "plat_version": "15.3.1",
    "channel": "jdCloud",
    "plat": "ios"
}


hmacKey = "706390cef611241d57573ca601eb3c061e174948"

# 请求体
service_body = '{"feed_id":"%s","command":[{"current_value":{"cmd":"%s"},"stream_id":"SetParams"}]}'

def config():
    cp = configparser.RawConfigParser()
    cp.read('/jdc/data/config/config.ini')
    sqlservice = cp.get('sql', 'sql')
    tgt = cp.get('jdc', 'WSKEY')
    return sqlservice, tgt

sqlservice, tgt=config()