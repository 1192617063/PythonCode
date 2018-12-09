import requests
from json import loads
class TRANS:
	def __init__( self ):
		self.BaseUrl = 'http://192.168.16.28:8080/recordTrans/'
		self.session = requests.Session()
		self.session.post('http://192.168.16.28:8080/recordTrans/login/login', data = {"name":"1702838","password":"123456","siteinfo":"武汉"})
	def __del__( self ):
		self.session = None
	def records( self , st , et , calledNo ):
		rs =  self.session.post(self.BaseUrl + 'record/listRecordData' , headers = {"Content-Type":"application/x-www-form-urlencoded","Accept":"application/json"} , data = {"agentID":"","dialTimeBegin":st+" 00:00:00","dialTimeEnd":et+" 00:00:00","callerNo":"","calledNo":calledNo,"id":"","calltype":"","custid":"","extension":"","page":"1","rows":"0"} )
		result = []
		for r in loads(rs.text)['rows']:
			if r['dialResult'] == "16":
				result.append([r['id'],str(r['dialTime']/1000)])
		return None if result == [] else result
	def down(self, fileid , folder , name ):
		with open(folder + name + ".wav","wb") as file:
			for data in self.session.post(self.BaseUrl + 'file/downLoadFileSite' ,headers = {"Content-Type":"application/x-www-form-urlencoded"}, data = {"id":fileid}).iter_content(1024):
				if data:
					file.write(data)
trans = TRANS()