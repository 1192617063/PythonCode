import requests
import datetime
from json import loads
data = {"jrl_00053":["武汉",{"name":"1702838","password":"123456"}],"jrl_00022":["襄阳",{"name":"080535","password":"Aa123456"}],"jrl_00012":["宜昌",{"name":"132595","password":"Aa123456"}]}
class CTIM:
	def __init__( self ):
		self.BaseUrl = 'http://168.99.156.92:8080/CTIM/'
		self.session = requests.Session()
	def __del__( self ):
		self.session = None
	def login( self , data ):
		self.session.post( self.BaseUrl + 'login/login' , data = data )
	def down( self , r , data ):
		rs =  self.session.post(self.BaseUrl + r  , data = data , headers = {"Content-Type":"application/x-www-form-urlencoded","Accept":"application/json"} )
		return loads(rs.text)['rows']
ctim = CTIM()
def outcome(time):
	rs = {'data':[]}
	for site , value in data.items():
		ctim.login( value[1] )
		for r in ctim.down( 'record/listRecordData' , {"siteID":site,"dialTimeBegin":time[0]+" 00:00:00","dialTimeEnd":time[1]+" 00:00:00","id":""	,"calledNo":"","extension":"","agentID":"","page":"1","rows":"0"} ):
			dt = datetime.datetime.fromtimestamp(r['dialTime']/1000).strftime("%Y-%m-%d %H:%M:%S")
			cl = 0 if r['connectTime'] == 0 or datetime.datetime.fromtimestamp(r['connectTime']/1000).strftime("%Y-%m-%d %H:%M:%S") == "1970-01-01 08:00:00" else r['calllength']
			d = {'区域':r['sitename'],'分机号':r['extension'],'姓名':r['extensionName'],'拨打时间':dt,'通话时长':cl}
			rs['data'].append(d)
		print("%s数据下载成功" %value[0])
	return rs