from bottle import run,route,request
@route('/')
def vote():
	return '''<!DOCTYPE html>
			<html>
			<head>
				<meta charset="utf-8">
				<title>你青睐的项目组长是谁？</title>
			</head>
			<body>
			<form method = 'post' action='/recieve'>
			武汉分公司拟按照项目组化运作业务，各项目小组承接公司指派相关业务。
			为推进项目小组组建决策，考虑员工意愿。
			开展此调研，请在意愿加入项目组长名字后打勾。注：此调研仅做调整参考。
				<h1>为你心目中的项目组长投票（投票范围：正式员工）</h1>
				<input type="radio" name="teamleader" value = 'wh166'>姚伟
				<input type="radio" name="teamleader" value = 'wh187'>刘刚
				<input type="radio" name="teamleader" value = 'wh208'>吕超
				<br/><br/>
				你的工号 <input type="text" name="cid" onchange="checkid(this.value)">
				<input type="submit" id = "submit" name="提交" disabled>
			</form>
			<script>
				function checkid(s){
					var patt = /^wh\d{2,3}$/
					var sub = document.getElementById("submit")
					if(s.search(patt) != -1){
						sub.removeAttribute('disabled')
					}else{
						sub.setAttribute('disabled','true')
					}
				}
			</script>
			</body>
			</html>'''
@route('/recieve',method = 'POST')
def recieve():
	ip = request.environ.get('REMOTE_ADDR')
	fms = request.forms
	with open('result.txt','a') as file:
		file.write('ip:{0} voter:{1} voted:{2}\n'.format(ip,fms['cid'],fms['teamleader']))
	return '投票完成'
run(host = "192.168.16.164",port = '80')