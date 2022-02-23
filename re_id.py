import sqlapi
import GlobalVariable
import jdcapi

GlobalVariable.headers["wskey"] = GlobalVariable.sqlservice
GlobalVariable.service_headers["tgt"] = GlobalVariable.tgt
print(sqlapi.read_sql("name", "in", 'replace', jdcapi.getListAllUserDevices()))
