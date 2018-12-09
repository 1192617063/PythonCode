from MFM import UserIDs,ACList,mfm,sel
from datetime import datetime
from CHECK import *
#tp = '', number = 50 , clicode = 'ALI' , batchno = ''
def audit( d ):
	tp,number,clicode,batchno = d
	rs = {'data':[]}
	users = ['wh208','wx276','wh333','wh330','wh102','wy281','wh304','wh368','wh129','wx305','wh377','wx84','wy280','wy282','wy283','wy285','wh318','wh381','wh348','wy292','wh365','wh326','wy274','wh335','wy286','wx309','wx308','wy297','wy293'] #UserIDs(clicode)['data'] ["wh304","wy292","wh129","wy293","wx276","wh365","wx305","wh208","wx308","wh377","wx84","wx318","wh381"]
	ulen = len(users)
	if tp not in ['VIEW', 'CALL']:
		return {'data':[]}
	for i,user in enumerate(users):
		print("正在检查%s(%d/%d)"%(user,i+1,ulen))
		if tp == 'VIEW':
			page = '1000'
		elif tp == 'CALL':
			page = '1000'
		ACs = ACList( user , clicode , batchno , 'ALL' , page )  #决定每个风控员检查案件数
		nlen = len(ACs[0])
		for j,index in enumerate(ACs[0]):
			print('正在处理%d/%d个'%( j+1 , nlen ))
			dw = mfm.downPage('main',dict({'index':index},**ACs[1]), 1)
			dix = sel('dunindex',dw)
			if dix == []:
				continue
			values = dix.split(',')
			actview = []
			viewArr = []
			trs = dw.select('#actview > tbody > tr')[::-1]
			for tr in trs:
				td = tr.select('td.mainctrl_view_detail')
				if td != [] and td[0].string == user:
					viewArr.append('{0} {1} {2}'.format(td[0].string,td[1].string,td[3].string))
					actview.append([td[0].string,datetime.strptime(td[1].string,'%Y/%m/%d %H:%M:%S'),td[3].string])
				else:
					continue
			viewStr = '\n'.join(viewArr)
			context = {'actview':actview} if clicode != 'ALI' else {'actview':actview,'aliphStr':trs[1].select("td")[3].string}
			if tp == 'VIEW':
				rr = ViewCheck(context)
				if rr:
					rs['data'].append({"批次号":values[8],"卡号":values[4],"姓名":values[7],"工号":user,"电话拨打规范":rr[0],"电话跟进规范":rr[1],"行动记录":viewStr})
					print('完成%d/%s'%(len(rs['data']),number))
			elif tp == 'CALL':
				rc = CallCheck(context,user,values[7])
				if rc:
					rs['data'].append({"工号":user,"姓名":values[7],"卡号":values[4],"有效录音":rc[0],"录音地址":rc[1],"行动记录":viewStr})
					print('完成%d/%s'%(len(rs['data']),number))
			if len(rs['data']) >= int(number):
				return rs
	return rs