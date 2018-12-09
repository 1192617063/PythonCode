from PIL import Image
from pyocr import pyocr
from io import BytesIO
tools = pyocr.get_available_tools()[0]
def ocr(im):
	im = Image.open(im)
	width = im.size[0] 
	height = im.size[1] 
	left = 3 
	top = 3 
	right = width - 3 
	bottom = height - 3 
	box = (int(left), int(top), int(right), int(bottom)) 
	im = im.crop(box) 
	im = im.resize((width * 4, height * 4), Image.BILINEAR) 
	# 转为灰度图 
	im = im.convert('L')
	# 去噪 
	threshold = 140 
	table = [] 
	for i in range(256): 
		if i < threshold: 
			table.append(0) 
		else: 
			table.append(1) 
	im = im.point(table, '1')
	return tools.image_to_string(im,lang='eng').replace('| ','I').replace(' ','').replace('/3','A').replace('!','I')