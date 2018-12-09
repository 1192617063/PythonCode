import requests
import json
import datetime
import threading
class HuaDan():
	def __init__(self):
		self.siteCode = {
			"jrl_00053":"武汉",
			"jrl_00022":"襄阳",
			"jrl_00012":"宜昌"
		}
		self.userData = [{"site":"jrl_00053","data":{
							"name":"1702838",
    						"password":"123456"
						}},
						{"site":"jrl_00022","data":{
    						"name":"080535",
    						"password":"Aa123456"
						}},
						{"site":"jrl_00012","data":{
							"name":"132595",
    						"password":"Aa123456"
						}}]
		self.queryData = {
						    "begintime":datetime.date.today() - datetime.timedelta(4),
						    "endtime":datetime.date.today(),
						    "siteId":"",
						    "page":"1",
						    "rows":"10",
						}
		self.session = requests.session()
		self.uploadList = []
		self.Flag = True
		self.E = threading.Event()
	def start(self):
		for u in self.userData:
			self.session.post("http://168.99.156.92:8080/CTIM/login/login",data=u["data"])
			self.query(u["site"])
			self.upload(u["site"])
	def query(self, site):
		rs = json.loads(self.session.post("http://168.99.156.92:8080/CTIM/record/siteUploadMessageList",data = self.queryData).text)
		for r in rs["rows"]:
			temp = {}
			if int(r["faild"]) != 0:
				temp["site"] = site
				temp["dateStr"] = r["dateOfRecord"]
				temp["status"] = "failed"
			elif int(r["local"]) != 0:
				temp["site"] = site
				temp["dateStr"] = r["dateOfRecord"]
				temp["status"] = "local"
			self.uploadList.append(temp)
		
	def upload(self,site):
		print("上传%s话单数据" %self.siteCode[site])
		for i,data in enumerate(self.uploadList):		
			if data != {}:
				temp = {}
				self.session.post("http://168.99.156.92:8080/CTIM/site/beginReupload",data={"siteId":data["site"],"dateStr":data["dateStr"],"uploadStatus":data["status"]})
				while not self.E.wait(3) and self.Flag:
					rsp = json.loads(self.session.post("http://168.99.156.92:8080/CTIM/site/reUploadLogList",data={"siteId":site}).text)["rows"][0]
					print("上传话单%d/%d，失败%d" %(rsp["successCount"],rsp["total"],rsp["failedCount"]))
					if int(rsp["total"]) == int(rsp["failedCount"]) + int(rsp["successCount"]):
						self.Flag = False
				self.Flag = True
				print("上传完成%d/%d" %(i+1,len(self.uploadList)))
				rsp = json.loads(self.session.post("http://168.99.156.92:8080/CTIM/site/reUploadLogList",data={"siteId":site}).text)["rows"][0]
				if rsp["failedCount"] != 0:
					temp["site"] = site
					temp["dateStr"] = data["dateStr"]
					temp["status"] = "failed"
					self.uploadList.append(temp)
		print("%s话单数据上传完毕" %self.siteCode[site])

h = HuaDan()
h.start()
