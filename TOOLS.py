import datetime
from calendar import monthrange
def datedict(d,mb = ""):
	if type(d[0]) == str:
		d[0] = datetime.datetime.strptime(d[0],"%Y-%m-%d")
		d[1] = datetime.datetime.strptime(d[1],"%Y-%m-%d")
	return {mb+"start_year":str(d[0].year), mb+"start_month":str(d[0].month), mb+"start_day":str(d[0].day), mb+"end_year":str(d[1].year), mb+"end_month":str(d[1].month), mb+"end_day":str(d[1].day)}
def daterange(ym):
	year, month = int(ym[0:4]), int(ym[4:])
	mdays = monthrange(year,month)[1]
	sd = datetime.date(year,month,1)
	today = datetime.date.today()
	ed = sd +datetime.timedelta(mdays-1) 
	if today < ed:
		ed = today
	return [sd,ed]