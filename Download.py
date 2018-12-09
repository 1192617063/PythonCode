from bottle import route,run,static_file
@route('/download')
def download():
	return static_file('search1.xls',root = '/',download = 'search1.xls')
run(host = "192.168.16.164",port=8080)