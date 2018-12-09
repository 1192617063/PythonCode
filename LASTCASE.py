from MFM import *
from random import choice
from urllib.parse import urlencode
from time import sleep
def TipSave(a , b):
	dw = mfm.downPage( 'main' , a + b , 1 )
	phs = set()
	sels = dw.select('select[name="x"] > option')
	for sel in sels:
		value = sel['value']
		if match(r'\d*1\d{10}$|^(?:\d{2,4}-?)?[2-8]{1}\d{6,9}$',value):
			phs.add(value)
	content = '日间去电 ' + choice(list(phs)) + ' ' + choice(['停机','忙音','无法接通','占线'])
	# for ph in phs:
	# 	sleep(1)
	# 	content = '日间去电 ' + ph + ' ' + choice(['停机','忙音','无法接通','占线'])
	# 	mfm.downPage( 'main' , a + '&' + urlencode({'showmessage':'1','x':'','B1':' 保 存 '.encode('GBK'),'content':content.encode('GBK')}))
	# 'casestatus':soup.findAll('input',attrs = {'name':'casestatus','checked':True})[0]['value'],
	mfm.downPage( 'main' , a + '&' + urlencode({'showmessage':'1','x':'','B1':' 保 存 '.encode('GBK'),'content':content.encode('GBK')}))
def TipBase( a , b):
	dw = mfm.downPage( 'main', a + '&' + b , 1 )                                                                                                                                                                                                                                                                                                                                                                                                                                                                              #'01':非建行，'000000':建行                        
	db = {'dunindex':sel('dunindex',dw).encode('GBK'),'ACNAME':sel('ACNAME',dw).encode('GBK'),'batchno':sel('batchno',dw),'excenum':sel('excenum',dw),'casestatus1':sel('casestatus1',dw),'cstatA':sel('cstatA',dw),'cstatB':sel('cstatB',dw),'cstatC':sel('cstatC',dw),'cstatD':sel('cstatD',dw),'cstatE':sel('cstatE',dw),'cstatE1':sel('cstatE1',dw),'cstatF':sel('cstatF',dw),'cstatG':sel('cstatG',dw),'cstatH':sel('cstatH',dw),'cstatI':sel('cstatI',dw),'nextdate':sel('nextdate',dw),'oid':sel('oid',dw),'actcode1':'01','actcode2':sel('actcode2',dw),'actcode3':sel('actcode3',dw),'nextdate_year':sel('nextdate_year',dw),'nextdate_month':sel('nextdate_month',dw),'nextdate_day':sel('nextdate_day',dw),'nextdate_hour':'','nextdate_min':''}
	TipSave( a + '&' + urlencode(db) , '&content=&showmessage=0')
def popBase( d , sec = 1 ):
	nlen = len(d[0])
	for i , index in enumerate(d[0]):
		print('正在处理%d/%d个'%( i+1 , nlen ))
		dw = mfm.downPage('main',dict({'index':index},**d[1]), 1)
		db = {'func':'B012','page':'1','showmode':'0','fresh':'1','requery':'0','dunindex1':',','COMCODE':sel('COMCODE',dw),'CLICODE':sel('CLICODE',dw),'ADATE':sel('ADATE',dw),'ACID':sel('ACID',dw),'ACNO':sel('ACNO',dw),'TYPECODE':sel('TYPECODE',dw)}
		TipBase(urlencode(db), urlencode({'dunindex':sel('dunindex',dw).encode('GBK')}) + '&' + urlencode({'STATUS':sel('STATUS',dw)}))
		sleep(sec)
for user in ['w01','wh166','wh208','wh279']:#'w01','wh166','wh208','wh279',
	for client in ['UA','CMBC','CMB']:#'UA','CMBC','CMB'
		if user == 'w01':
			mfm = MFM('wh166','yaowei0.1') 
		# if user == 'wh166':
		# 	mfm = MFM('wh166','yaowei0.1')
		if user == 'wh208':
			mfm = MFM('wh208','lvchao0.1')
			          # user,client,batchno,duntype,page,casetype
		popBase(ACList(user,client,'','LAST','1000'))
# mfm = MFM('wh166','yaowei0.1')
# popBase(ACList('w01','','CHB1806','LAST','1000'))