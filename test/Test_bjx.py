# -*-  coding:utf-8 -*-
"""
@Author       : "Alex Yean"    
@Create Date  : "2018-02-27"
@Email        : "ytf513@foxmail.com"
@Description  : 
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import requests
import json
headers_input = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
							   'Content-type':'application/json', 'Accept': 'text/plain'}

#因js中对keyword escape处理，所以做对应转义
input_str='思源电气'
input_str=json.dumps(input_str).replace("\\","%") #将Python数据类型列表进行json格式的编码解析
input_str=json.loads(input_str)#解码python json格式
#print input_str

from lxml import html
Have_Content=True
i=1
f=open('search_bjx.txt','a')
while Have_Content and i<2:
	print "开始爬取第%s个网页..." % i

	params = {'keyWord': unicode(input_str)+"&function1=&function2=&class1=&class2=&record=0&workTime=0&workprovince=&chkabove="}
	r = requests.get('http://hr.bjx.com.cn/SearchResult.aspx',headers=headers_input,params=params,timeout=5)  #params=params时会出错
	r.encoding = r.apparent_encoding #从内容分析出的响应内容编码方式
	resp_text=r.text
	print r.url
	tree=html.fromstring(resp_text)

	list_ul=tree.xpath('//div[@id="hoverZW"]//ul/li')
	print len(list_ul)
	if list_ul:
		for ul in list_ul:
			#print ul
			li=ul.xpath('.//dd[@class="selected"]//a')
			li1=ul.xpath('.//dd[@class="selected2"]//a')
			#print li
			res=li[0].text+' '+li1[0].text+' '+li[0].get('href')
			print res
			f.write(res)
			f.write('\n')
	else:
		Have_Content=False

	i=i+1

f.close()