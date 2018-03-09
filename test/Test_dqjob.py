# -*-  coding:utf-8 -*-
"""
@Author       : "Alex Yean"    
@Create Date  : "2018-02-27"
@Email        : "ytf513@foxmail.com"
@Description  : 
"""
import sys
reload(sys)
from lxml import html
sys.setdefaultencoding("utf-8")

import requests
import json
import Queue
import threading
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
headers_input = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

#适配器，重试5次，回避参数0.2
s=requests.session()
s.keep_alive = False
retries=Retry(total=5,backoff_factor=0.2,status_forcelist=[500,502,503,504])
s.mount('http://',HTTPAdapter(max_retries=retries))

#全局队列
queue = Queue.Queue()

def get_job_links(input_str):
	#因js中对keyword escape处理，所以做对应转义
	input_str=json.dumps(input_str).replace("\\","%") #将Python数据类型列表进行json格式的编码解析
	input_str=json.loads(input_str)#解码python json格式

	Have_Content=True
	i=1
	#f=open('search_dqjob.txt','a')
	while Have_Content:
		print "开始爬取第%s个网页..." % i

		params={'keyWord':input_str,'function2':'','function1':'','workprovince':'','record':0,'workTime':0,'chkabove':'','page':i}
		r = s.get('http://www.dqjob.com.cn/SearchResult.aspx',headers=headers_input,params=params)
		r.encoding = r.apparent_encoding #从内容分析出的响应内容编码方式
		resp_text=r.text

		tree=html.fromstring(resp_text)

		list_ul=tree.xpath('//div[@id="hoverZW"]/ul')
		if list_ul:
			for ul in list_ul:
				li=ul.xpath('./li[@class="sepc1"]/a')
				li1=ul.xpath('./li[@class="sepc2"]/a')
				#print li
				queue.put("http://www.dqjob.com.cn%s" % li[0].get('href'))
				# f.write(li[0].text+' '+li1[0].text+' '+li[0].get('href'))
				# f.write('\n')
		else:
			Have_Content=False

		i=i+1

def get_title(url):
	r = s.get(url, headers=headers_input)
	r.encoding = r.apparent_encoding  # 从内容分析出的响应内容编码方式
	resp_text = r.text
	tree = html.fromstring(resp_text)
	title=tree.xpath("//title")
	print title[0].text,r.url

class DatamineThread(threading.Thread):
	"""Threaded Url Grab"""

	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			# grabs host from queue
			chunk = self.queue.get()
			# 处理程序
			get_title(chunk)
			# signals to queue job is done
			self.queue.task_done()

if __name__ == "__main__":
	get_job_links("泰开")

	for i in range(5):
		dt = DatamineThread(queue)
		dt.setDaemon(True)
		dt.start()

	# wait on the queue until everything has been processed
	queue.join()