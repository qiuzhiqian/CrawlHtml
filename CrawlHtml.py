# coding=utf-8
import os,sys
import re
import time
import logging
#import pdfkit
#import requests
from html.parser import HTMLParser  

import urllib.request

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>

"""

addrList=[]
titleList=[]
currentPath=''
currentFile=None

#属性匹配
def findattr(attr,name,val):
	for each in attr:
		if name == each[0] and val == each[1]:
			return True
	return False

#获取链接列表的时候使用
class hp(HTMLParser):  
	classTag =False
	classGroup = False
	listTag = False
	cnt = 0
      
	def handle_starttag(self,tag,attr):
		self.classTag=findattr(attr,"class","uk-nav uk-nav-side")
		
		if self.classTag== True:
			self.cnt=self.cnt+1
			if self.cnt==2:
				self.classGroup=True
			
		if self.classGroup== True:	
			if tag == 'a':  
				self.listTag = True  
				#print (dict(attr))  
				for each in attr:
					if each[0] == 'href':
						#print(each[1])
						addrList.append(each[1])
              
	def handle_endtag(self,tag): 
		if self.classGroup== True:	
			if tag == 'a':  
				self.listTag = False  
				
			if tag == 'ul':
				self.classGroup=False
              
	def handle_data(self,data):  
		if self.classGroup == True and self.listTag == True:  
			#print (data) 
			titleList.append(data)

#获取网页内容的时候使用
class webContext(HTMLParser):
	classTag =False
	contextFlag=False
	textFlag=False		#有效文本标志
	divcnt=0
	cnt=1
	
	
	def handle_starttag(self,tag,attr):
		self.classTag=findattr(attr,"class","x-wiki-content")	#匹配x-wiki-content类
		
		if self.classTag == True:
			self.cnt=self.cnt+1
			self.contextFlag=True
			
		if self.contextFlag==True:
			
			temp='<%s ' %(tag)
			imgsrc=''
			for each in attr:
				if tag=='img' and each[0] == 'src':		#each为元组，元组拥有不可变性
					if(each[1].find('http')!=0):
						imgsrc='http://www.liaoxuefeng.com%s' %(each[1])
					else:
						imgsrc=each[1]
					temp=temp+each[0]+'='+imgsrc
					break
				#else:
				#	temp=temp+each[0]+'='+each[1]
			
			if tag == 'img':
				temp=temp+'/>'
			else:
				temp=temp+'>'
			currentFile.write(temp)
	
	def handle_endtag(self,tag):
		if self.contextFlag == True:
			if tag == 'div':
				self.cnt=self.cnt-1
				if self.cnt==0:
					self.contextFlag=False	#说明查找结束
			
			temp='</%s>\r\n' %(tag)
			currentFile.write(temp)
	
	def handle_data(self,data):
		if self.contextFlag == True:
			currentFile.write(data)


def get_url_list():
	"""
	获取所有URL目录列表
	:return:
	"""
	response = urllib.request.urlopen("http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000")
	
	htmlcontext=response.read().decode("UTF-8")
	
	myHp=hp()
	myHp.feed(htmlcontext)
	myHp.close()
	
#	for i in range(len(titleList)):
#		print(titleList[i])
#		print(addrList[i])


def main():
	global currentPath
	global currentFile
	start = time.time()
	get_url_list()
	for i in range(len(titleList)):
		filename=titleList[i].replace('/','_')
		filename=filename.replace('-','_')
		currentPath='%s\\%d_%s.html' %(os.path.dirname(__file__),i,filename)
		print(currentPath)
		currentFile=open(currentPath,'w')
		temp='<h1>%s</h1>\r\n' %(titleList[i])		#写入标题
		currentFile.write(temp)
		
		req = urllib.request.Request('http://www.liaoxuefeng.com'+addrList[i])
		try:
			response = urllib.request.urlopen(req)
		except HTTPError as e:
			print('The server couldn\'t fulfill the request.')
			print('Error code: ', e.code)
		except URLError as e:
			print('We failed to reach a server.')
			print('Reason: ', e.reason)
		else:
			print("good!")
			
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
			req.add_header('Connection','keep-alive')
			htmlcontext=response.read().decode("UTF-8")
			htmlFile=webContext()
			htmlFile.feed(htmlcontext)
			htmlFile.close()
			
		currentFile.close()
	
	total_time = time.time() - start
	print(u"总共耗时：%f 秒" % total_time)


if __name__ == '__main__':
	main()
