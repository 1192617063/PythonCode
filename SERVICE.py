from bottle import run, route
from CTIM import *
from MFM import *
from AUDIT import audit
from AUDITF import auditf
from VISIT import *
@route("/:func/:param")
def interfunction(func,param):
	return globals().get(func)(param.split("&"))
@route("/:func")
def interfunction(func):
	return globals().get(func)()
run(host = "127.0.0.1",port=8080)
