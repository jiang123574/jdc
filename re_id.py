import sqlapi
import GlobalVariable
import jdcapi
GlobalVariable.headers["wskey"] = GlobalVariable.WSKEY
GlobalVariable.service_headers["tgt"] = GlobalVariable.WSKEY
print(sqlapi.read_sql("name", "in", 'replace', jdcapi.getListAllUserDevices()))