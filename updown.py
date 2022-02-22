import sqlapi
import GlobalVariable
import jdcapi
import pandas as pd
import time

import configparser


def config():
    cp = configparser.RawConfigParser()
    cp.read('config.ini')
    sqlservice = cp.get('sql', 'sql')
    tgt = cp.get('jdc', 'WSKEY')
    return sqlservice, tgt


GlobalVariable.headers["wskey"] = config()[1]
GlobalVariable.service_headers["tgt"] = config()[1]

for feed_id in sqlapi.read_sql("name", "out")['feed_id']:
    # 公网ip，   上传，   cpu，mac，固件版本，wan口ip，？，  下载速度， 内存，运行模式，   在线时间，   运行模式， ap模式， sn
    public_ip, upload, cpu, mac, rom, wanip, romType, download, mem, model_name, onlineTime, model, ap_mode, sn = jdcapi.getControlDevice(
        feed_id, 2)
    data = pd.DataFrame(
        [[mac, int(time.time() / 1000) * 1000, round(int(upload) / 10), round(int(download) / 10), cpu, mem]],
        columns=['mac', 'time', 'upload', 'download', 'cpu', 'mem'])
    print(sqlapi.read_sql("sampling", "in", 'append', data))
