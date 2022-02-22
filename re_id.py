import sqlapi
import GlobalVariable
import jdcapi
import configparser


def config():
    cp = configparser.RawConfigParser()
    cp.read('config.ini')
    sqlservice = cp.get('sql', 'sql')
    tgt = cp.get('jdc', 'WSKEY')
    return sqlservice, tgt


GlobalVariable.headers["wskey"] = config()[1]
GlobalVariable.service_headers["tgt"] = config()[1]
print(sqlapi.read_sql("name", "in", 'replace', jdcapi.getListAllUserDevices()))
