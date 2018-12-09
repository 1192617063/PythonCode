from re import findall
from datetime import datetime,timedelta
from TRANS import trans
import os
def callview( view ):
	acts = []
	for v in view['actview']:
		r = findall(r'^(?:日间去电|夜间去电|网查|经查找)[^0-9-]+([0-9-]{5,15})(\D.*)',v[2])
		if r != []:	    #userID 时间 电话号码 结果
			acts.append([v[0],v[1],r[0][0],r[0][1],v[3]])
	return acts
def ViewCheck( view ):
	rs = [1,1]
	acts = callview(view)
	if acts == []:
		rs[0] = 0
		return None
	if view.get('aliphStr'):
		if acts[0][2][-11:] not in findall(r'支付宝绑定手机,\w+,(\d{11,13})',view['aliphStr']):
			rs[0] = 0
			return None
	if rs[0] == 1:
		phones = []
		for act in acts: #拒接
			if findall(r'来电提醒|线路忙|用户正忙|挂断|暂停服务|无此号码|电话故障|呼叫限制|无登记|停用|正在通话|通话中|号码不存在|空号|无应答|停机|无人接听|无人接|致电留言|未接|盲音|忙音|嘟嘟|占线|关机|失联|无法接通|电话欠费|无此号码|设置',act[3]) != []:
				phones.append(act[2])
		for phone in phones:
			if phones.count(phone) > 4:
				rs[0] = 0
				return None
	for i in range(len(acts)):
		if i == 0:
			continue
		else:
			if (acts[i][1] - acts[i-1][1]).days > 7:
				rs[1] = 0
				return None
	return rs
def CallCheck( view , userID , name ):
	acts = callview(view)
	calls = []
	for act in acts:
		if findall(r'来电提醒|拒接|不了解|线路忙|用户忙|用户正忙|挂断|暂停服务|无此号码|电话故障|呼叫限制|无登记|停用|正在通话|通话中|号码不存在|打错|空号|无应答|停机|无人接听|无人接|致电留言|未接|盲音|忙音|嘟嘟|占线|关机|失联|无法接通|电话欠费|无此号码|设置',act[3]) == []:		
			calls.append(act[1:3])
	if len(calls) not in range(3,6):
		return None
	else:
		IDs = []
		for call in calls:
			rcs = trans.records(datetime.strftime(call[0],'%Y-%m-%d'),datetime.strftime(call[0]+timedelta(1),'%Y-%m-%d'),call[1])
			if not(rcs):
				return None
							  # 电话                   拨打时间
			IDs.append( [ rcs ,  call[1] , datetime.strftime(call[0],'%Y%m%d') ] )
		addr = 'E:/稽核报告/录音抽检/电催录音/{0}/{1}/'.format(userID,name)
		for ID in IDs:
			if not os.path.exists(addr):
				os.makedirs(addr)
			for i in ID[0]:
				trans.down(i[0],addr,'{0}-{1}-{2}'.format(ID[2] , ID[1] , i[1]))
		return [len(IDs),addr]
def CHECKF( view ):
	rs = [1,1,1,1]
	vs = view['actview']
	td = datetime.date(datetime.today())
	sd = view['date']
	ed = lambda x , y : (x-y).days	
	r0 = [v[1] for v in vs if findall(r'^(?:日间去电|夜间去电)[^0-9-]+([0-9-]{5,15})(\D.*)',v[2]) != []]
	r1 = [v[1] for v in vs if findall(r'日间去电|夜间去电|网查',v[2]) != []]
	r2 = [v[1] for v in vs if findall(r'有线|户籍|电表|水表|宽带|村委|村书记',v[2]) != []]
	r3 = [v[1] for v in vs if findall(r'同意查访',v[2]) != []]		
	if r0 == []:
		if ed(td,sd) > 2:
			rs[0] = 0
	elif ed(r0[0],sd) > 2:
		rs[0] = 0
	if r1 == []:
		rs[1]  = 0
	else:
		if ed(td,r1[-1]) > 3:
			rs[1] = 0
		else:
			for i in range(len(r1)):
				if i == 0:
					continue
				if ed(r1[i],r1[i-1]) > 3:
					rs[1] = 0
	if r2 == []:
		rs[2] = 0
	if r3 == []:
		if ed(td,sd) > 30:
			rs[3] = 0
	elif ed(r3[0],sd) > 30 :
		rs[3] = 0
	return rs


