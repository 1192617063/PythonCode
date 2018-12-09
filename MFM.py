import requests
import datetime
from bs4 import BeautifulSoup
from re import match,findall
from TOOLS import *
def sel(selector,dw,oneToStr = True):
	names = dw.select('input[name="{0}"]'.format(selector))
	if len(names) == 1 and oneToStr:
		return names[0]['value']
	else:
		rs = []
		for name in names:
			rs.append(name['value'])
		return rs
class MFM:
	def __init__( self ,username = 'wh351' , password = 'flink0.1'):
		self.BaseUrl = 'http://168.99.156.87/asp/'
		self.session = requests.Session()
		self.headers = {"Content-Type":"application/x-www-form-urlencoded","User-Agent":"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)"}
		self.downPage("main",{"show":"","func":"L002","usercode":username,"userpasswd":password,"login":" ��¼ "})
		self.downPage("main",{"func":"F020","page":"1","showmode":"1","fresh":"1","requery":"0"})
		self.wp = self.downPage("main",{"func":"B010","page":"1","showmode":"1","fresh":"1","requery":"0"},1)	
	def __del__( self ):
		self.session = None
	def downPage( self , r , data , type = 0 ):
		rs = self.session.post(self.BaseUrl + r + '.asp', headers = self.headers , data = data )
		rs.encoding = 'GBK'
		if type == 1:
			return BeautifulSoup( rs.text , "html5lib" )
		return rs.text.replace('<link type="text/css" rel="stylesheet" href="mainframe.css">','')
mfm = MFM()
def nome():
	rs = {'data':[]}
	for sel in mfm.wp.select('#Squery > select:nth-of-type(1) > option'):
		d = sel.string.split(' ')
		if len(d) > 1:
			rs['data'].append({'工号':d[0].strip(),'姓名':d[1].strip()})
	return rs
def payback(d):  #回款统计表（按催收员）请求方式为http://localhost:8080/payback/开始时间&结束时间[&工号]
	if len(d) == 2:
		d.append('ALL')
	return mfm.downPage("report/report_N2D", dict(datedict(d[0:2]),**{"x":"","groupcode":"grp_w","usercode":d[2],"clientcode":"ALL","typecode":"","excenum":"","batchno":"","citys":"","khdm":"","paystatus":"01"}))
def paybackG(d):
	return mfm.downPage("report/report_N2G",dict(datedict(daterange(d[0])),**{"x":"","groupcode":"grp_w","usercode":"ALL","clientcode":d[1],"typecode":"","excenum":"","batchno":d[2]}))
def paybackGH(d):
	return mfm.downPage("report/report_N2G_HZ",dict(datedict(daterange(d[0])),**{"x":"","groupcode":"grp_w","usercode":"ALL","clientcode":d[1],"typecode":"","excenum":"","batchno":d[2]}))
def paybackT(d):
	return mfm.downPage("report/report_N2G_HZ",dict(datedict(daterange(d[0])),**{"x":"","groupcode":"grp_w","usercode":"ALL","clientcode":'CCBHB',"typecode":"","excenum":"","batchno":''}))
def returnList(d):
	return mfm.downPage('report/report_N25',dict(datedict(d[0:2]),**{"x":"","groupcode":"grp_w","usercode":"ALL","clientcode":"ALL","typecode":"","excenum":"","batchno":"","city":""}))
def inquiryBack(d):
	rs = {'data':[]}
	dw =  mfm.downPage('report/report_N117',{"countdate":d[0],"groupcode":"grp_w","usercode":"ALL","cday":d[1]},1).select("body > table > tbody > tr")
	for i , tr in enumerate(dw):
		trigger = True
		if i == 0 or i == len(dw) -1:
			continue
		else:
			td = tr.select("td")
			ps = td[8].select("table > tbody > tr")
			pay = []
			for p in ps:
				t = p.select('td')
				if len(t[0].string.strip()) == 0:
					trigger = False
				pay.append({"催收员":t[0].string.strip(),"还款日期":t[1].string.strip(),"还款金额":t[2].string.strip()})
			if trigger:
				rs['data'].append({"日期":td[6].string.strip().replace("-",""),"卡号":td[2].string.strip(),"客户&期数":td[1].string.strip().split("1")[0] + td[3].string.strip(),"回款情况":pay})
	return rs
def mission(d):       #行程表   请求方式为http://localhost:8080/mission/[201805|20185]
	return mfm.downPage("report/report_N115", dict(datedict(daterange(d[0]),"vdate_"),**{"y":"","groupcode":"grp_w","usercode":"ALL"}))
def caseStatus(d):
	d.append(None)
	return mfm.downPage("report/report_W16B",dict(datedict(daterange(d[1]) if d[1] else [datetime.date(datetime.date.today().year,datetime.date.today().month,1)- datetime.timedelta(62),datetime.date.today()]),**{"x":"","clientcode":d[0],"batchno":"","khdm":""}))
def detailOfCaseStatus(d):
	return mfm.downPage("report/report_N45",{"batchno":d[0],"x":"","start_year":"","start_month":"","start_day":"","end_year":"","end_month":"","end_day":"","groupcode":"grp_w","usercode":"ALL","typecode":"","clientcode":"ALL","excenum":d[1],"city":"","cstatus":"ALL"})
def dCaseStatus(d):
	return mfm.downPage("report/report_N44",{"batchno":d[0],"x":"","start_year":"","start_month":"","start_day":"","end_year":"","end_month":"","end_day":"","groupcode":"grp_w","usercode":"ALL","typecode":"","clientcode":"ALL","excenum":d[1],"city":"","cstatus":"ALL"})
def mailList(d):
	return mfm.downPage("report/report_N125",dict(datedict(daterange(d[0])),**{'batchno':'','x':'','type':'recordtime','groupcode':'grp_w','usercode':'ALL'}))
def operateReport(d):
	return mfm.downPage("report/report_P02",dict(datedict(d[:2]),**{'clientcode':d[2],'batchno':'','x':'','groupcode':d[3],'usercode':'ALL','excenum':d[4]}))
def UserIDs(clicode = 'ALL'):
	rs = {'data':[]}
	ls = set()
	dw = mfm.downPage('report/report_N49',{"clientcode":clicode,"x":"","start_year":"","start_month":"","start_day":"","end_year":"","end_month":"","end_day":"","batchno":"","excenum":"","city":"","ST":"usercode"},1)
	for tr in dw.select("body > table:nth-of-type(2) > tbody > tr"):
		ID = tr.select('td')[1].string.strip()
		if ID not in ['工号','w01','wh074']:
			ls.add(ID)
	rs['data'] = list(ls)
	return rs
def ACList( user , clicode = '' , batchno = '' , duntype = 'ALL' , page = '1' , casetype = 'ALL', acno = ''):
	dw = mfm.downPage('main',{"USERCODE":user,"clicode":clicode,"duntype":duntype,"page":page,"batchno":batchno,"func":"B010","showmode":"1","fresh":"1","requery":"0","qsign":"1","COMCODE":"755","GROUPCODE":"grp_w","status":"ALL","casetype":casetype,"specoption":"ALL","acno":acno,"acname":"","city":"","excenum":"","acid":"","pageno1":"","pageno2":"","gotopage":"GO","DUN":'&nbsp;催 收&nbsp;'.encode('GBK'),"MODIFY":'&nbsp;刷 新&nbsp;'.encode('GBK'),"PREVIEW":'&nbsp;打印预览&nbsp;'.encode('GBK'),'PRINT':'&nbsp;打 印&nbsp;'.encode('GBK')},1)
	return [sel('index',dw,False),{'func':'B011','page':'1','showmode':sel('showmode',dw),'fresh':sel('fresh',dw),'requery':sel('requery',dw),'COMCODE':sel('COMCODE',dw),'GROUPCODE':sel('GROUPCODE',dw),'USERCODE':user,'status':'ALL','duntype':duntype,'casetype':'ALL','specoption':'ALL','clicode':clicode,'batchno':batchno,'acno':'','acname':'','city':'','excenum':'','acid':'','pageno1':'','pageno2':'','gotopage':'GO','DUN':'&nbsp;催 收&nbsp;'.encode('GBK'),'MODIFY':'&nbsp;刷 新&nbsp;','PREVIEW':'&nbsp;打印预览&nbsp;'.encode('GBK'),'PRINT':'&nbsp;打 印&nbsp;'.encode('GBK')}]
def LASTC():
	rs = {'data':[]}
	dw = mfm.downPage('main',{"USERCODE":'ALL',"clicode":'',"duntype":'LAST',"page":'1000',"batchno":'',"func":"B010","showmode":"1","fresh":"1","requery":"0","qsign":"1","COMCODE":"755","GROUPCODE":"grp_w","status":"ALL","casetype":'ALL',"specoption":"ALL","acno":"","acname":"","city":"","excenum":"","acid":"","pageno1":"","pageno2":"","gotopage":"GO","DUN":'&nbsp;催 收&nbsp;'.encode('GBK'),"MODIFY":'&nbsp;刷 新&nbsp;'.encode('GBK'),"PREVIEW":'&nbsp;打印预览&nbsp;'.encode('GBK'),'PRINT':'&nbsp;打 印&nbsp;'.encode('GBK')},1)
	for tr in dw.select('tr.mainctrl_list_detail'):
		tds = tr.select('td')
		rs['data'].append({'客户':findall(r'^[A-Z]{2,6}',tds[3].string.strip())[0],'工号':tds[9].string.strip()})
	return rs
def temp(batchno):
	rs = {'data':[]}
	dw = mfm.downPage('main',{"USERCODE":'ALL',"clicode":'',"duntype":'ALL',"page":'1000',"batchno":batchno,"func":"B010","showmode":"1","fresh":"1","requery":"0","qsign":"1","COMCODE":"755","GROUPCODE":"grp_w","status":"ALL","casetype":'ALL',"specoption":"ALL","acno":"","acname":"","city":"","excenum":"","acid":"","pageno1":"","pageno2":"","gotopage":"GO","DUN":'&nbsp;催 收&nbsp;'.encode('GBK'),"MODIFY":'&nbsp;刷 新&nbsp;'.encode('GBK'),"PREVIEW":'&nbsp;打印预览&nbsp;'.encode('GBK'),'PRINT':'&nbsp;打 印&nbsp;'.encode('GBK')},1)
	for tr in dw.select('tr.mainctrl_list_detail'):
		tds = tr.select('td')
		oid = tr.select('input[name="index"]')[0]['value'].split(',')[2]
		rs['data'].append({'工号':tds[9].string.strip(),'姓名':tds[6].string.strip(),'身份证号码':oid,'委托金额':tds[7].string.strip()})
	return rs
def CASEInFO(acid):
	dw = mfm.downPage('main',{"USERCODE":'ALL',"clicode":'',"duntype":'ALL',"page":'1',"batchno":'',"func":"B010","showmode":"1","fresh":"1","requery":"0","qsign":"1","COMCODE":"755","GROUPCODE":"grp_w","status":"ALL","casetype":'ALL',"specoption":"ALL","acno":"","acname":"","city":"","excenum":"","acid":acid,"pageno1":"","pageno2":"","gotopage":"GO","DUN":'&nbsp;催 收&nbsp;'.encode('GBK'),"MODIFY":'&nbsp;刷 新&nbsp;'.encode('GBK'),"PREVIEW":'&nbsp;打印预览&nbsp;'.encode('GBK'),'PRINT':'&nbsp;打 印&nbsp;'.encode('GBK')},1)
	index = sel('index',dw)
	if index == []:
		return {'data':['','']}
	data = {'index':index,'func':'B011','page':'1','showmode':sel('showmode',dw),'fresh':sel('fresh',dw),'requery':sel('requery',dw),'COMCODE':sel('COMCODE',dw),'GROUPCODE':sel('GROUPCODE',dw),'USERCODE':'ALL','status':'ALL','duntype':'ALL','casetype':'ALL','specoption':'ALL','clicode':'','batchno':'','acno':'','acname':'','city':'','excenum':'','acid':'','pageno1':'','pageno2':'','gotopage':'GO','DUN':'&nbsp;催 收&nbsp;'.encode('GBK'),'MODIFY':'&nbsp;刷 新&nbsp;','PREVIEW':'&nbsp;打印预览&nbsp;'.encode('GBK'),'PRINT':'&nbsp;打 印&nbsp;'.encode('GBK')}
	dwd = mfm.downPage('main',data, 1)
	dtime = dwd.select('#caseview > tbody > tr:nth-of-type(1) > td:nth-of-type(4)')[0].string
	for td in dwd.select('#addview > tbody > tr > td.mainctrl_view_detail'):
		txt = findall(r'\w*孝感\w+',td.text)
		if txt != [] and len(txt[0]) > 10:
			return {'data':[dtime,txt[0]]}
	return {'data':[dtime,'']}
def VisitList(d):
	return mfm.downPage("report/report_N115_fp", dict(datedict(daterange(d[0]),"vdate_"),**{"y":"","groupcode":"grp_w","usercode":"ALL"}))
def PostVisit(d):
	l = ACList( "ALL" , '' , '' , 'ALL' , '1000' , 'ALL', d[0])
	i = l[0]
	if len(i) > 1:
		return {'卡号':d[0],'结果':'多账户'}
	elif len(i) == 0:
		return {'卡号':d[0],'结果':'无账户'}
	dw = mfm.downPage('main',dict({'index':i},**l[1]), 1)
	dwm = mfm.downPage('main',{'func':'B01G','page':'1','showmode':'0','fresh':'1','requery':'0','dunindex':sel('dunindex',dw).encode("GBK"),'dunindex1':sel('dunindex1',dw),'COMCODE':sel('COMCODE',dw),'CLICODE':sel('CLICODE',dw),'ADATE':sel('ADATE',dw),'ACID':sel('ACID',dw),'ACNO':sel('ACNO',dw),'TYPECODE':sel('TYPECODE',dw),'STATUS':sel('STATUS',dw),'Select':''},1)
	nd = sel('nextdate',dwm).split(' ')[0].split('/')
	mfm.downPage('main',{'func':'B01G','page':'1','showmode':'0','fresh':'1','requery':'0','relation':'01','showmessage':'1','exes2':d[15],'exes3':'','hymemo':'','proamt':'','prodate_year':'','prodate_month':'','prodate_day':'','newdata1':'','xjcs':'','xjcsmemo':'','dzsx':'','dzsxmemo':'','dzzx':'','newdata2':'','xx':'','ymrmemo':'','ACTIONTYPE':d[14],'ACTIONEFFECT':'01','DATACHK':'02','B1':'��  ��','visitdate_year':d[1],'visitdate_month':d[2],'visitdate_day':d[3],'arrivetime':d[4],'leavetime':d[5],'period':d[6],'vaddress':d[7].encode('GBK'),'vname':sel('ACNAME',dwm).encode('GBK'),'dunindex':sel('dunindex',dwm).encode('GBK'),'COMCODE':sel('COMCODE',dwm),'CLICODE':sel('CLICODE',dwm),'ADATE':sel('ADATE',dwm),'ACID':sel('ACID',dwm),'ACNO':sel('ACNO',dwm),'TYPECODE':sel('TYPECODE',dwm),'ACNAME':sel('ACNAME',dwm).encode('GBK'),'batchno':sel('batchno',dwm),'nextdate':sel('nextdate',dwm),'ymr':d[8],'hy':d[9],'ds':sel('ACNAME',dwm).encode('GBK'),'NEXTACTION':d[10].encode('GBK'),'exes1':d[11], 'vman':d[12],'vmanb':d[13],'nextdate_year':nd[0],'nextdate_month':nd[1],'nextdate_day':nd[2]})
	return {'卡号':d[0],'结果':'成功'}
	