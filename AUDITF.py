from MFM import UserIDs,ACList,mfm,sel
from datetime import datetime
from CHECK import *
def auditf():
	rs = {'data':[]}
	                 #建行
	users = UserIDs('CCBHB')['data'] #UserIDs(clicode)['data'] ["wh304","wy292","wh129","wy293","wx276","wh365","wx305","wh208","wx308","wh377","wx84","wx318","wh381"]
	ulen = len(users)
	for i,user in enumerate(users):
		print("正在检查%s(%d/%d)"%(user,i+1,ulen))
		ACs = ACList( user , 'CCBHB' , '' , 'ALL' , '1' ,'B1')  #决定每个风控员检查案件数
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
				if td != [] and td[0].string != None and td[0].string[0] == 'w':
					               #工号 时间 记录
					viewArr.append('{0} {1} {2}'.format(td[0].string,td[1].string,td[3].string))									
					actview.append([td[0].string,datetime.date(datetime.strptime(td[1].string,'%Y/%m/%d %H:%M:%S')),td[3].string])
				else:
					continue
			viewStr = '\n'.join(viewArr)
			context = {'actview':actview,'date':datetime.date(datetime.strptime(values[1],'%Y%m%d'))}# if clicode != 'ALI' else {'actview':actview,'aliphStr':trs[1].select("td")[3].string}
			rr = CHECKF(context)
			rs['data'].append({"批次号":values[8],"卡号":values[4],"姓名":values[7],"工号":user,"委托日期":values[1],"首催":rr[0],"跟进频率":rr[1],"深挖":rr[2],"外访":rr[3],"行动记录":viewStr})
	return rs