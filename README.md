本文档参考了该[博客][referblog]和其[源代码][code]

不过为了方便，我没有使用beautifulsoup和pdfkit，而是直接通过python自带的HTMLParser来处理html，然后解析出html中的主体内容，然后重新生成一个新的html，并重命名为章节内容。

首先我们看一下廖雪峰python的网页结构
![网页结构][webstruct]
分为：目录、正文、其他。对于我们有用的信息都在目录和正文中，而且目录我们只需要解析一次，因为各个页面中的目录都是一样的。
所以我们的解析思路是这样的：
1. 从第一页中解析目录，提取目录各项名称和对应的url地址，分别保存到两个列表中,即titleList和addrList
2. 创建一个以titleList中各项为文件名的html文件并打开，将文件名写入文件开头作为标题，
3. 依次次访问addrlist中对应的各个网页，提取网页中的正文部分，并将正文部分内容写入到之前打开的文件中，同时规划好各个部分的格式。

##从首页中获取目录信息

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
首先通过urllib.response的函数来获取网页内容，然后我们创建一个hp对象来处理读取的html文档内容。
对于hp类是继承自HTMLParser类的，同时需要重载HTMLParser的三个函数handle_starttag、handle_endtag和handle_data
当检测到节点头时，就会触发handle_starttag的调用，例如```<div>```
当检测到节点尾时，就会触发handle_endtag的调用，例如```</div>```
当检测到其他内容是会调用handle_data，这个通常来处理节点头和节点尾之间的文本节点，例如```<div>ABC</div>```中的ABC
另外节点头中通常包含有属性值，这些值通常在调用handle_starttag是通过attr这样的一个元组序列来保存传递的。
于是，当我们需要判断某一个节点头中是否包含我们需要的属性值是，我们就需要遍历这个attr，比如有这样一个代码：
```
<div class="start">
python教程
</div>
```
判断该段代码头是否class="start"
```
for each in attr:
    if class == each[0] and "start"== each[1]:
        return True
return False
```
为了方便使用我们将它写成一个函数
```
#属性匹配
def findattr(attr,name,val):
	for each in attr:
		if name == each[0] and val == each[1]:
			return True
	return False
```
通过查看F12开发者模式我们可以发现，目录页面是包含在**第二个**class="uk-nav uk-nav-side"的```<div>```标签中

同时正文内容包含在第一个class="x-wiki-content"的```<div>```标签中

##目录提取
```
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
```
首先我们通过urllib.request.urlopen访问http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000网址，这个网址是廖雪峰python教程的第一个网页，因为刚才说过每个页面中的目录内容都是相同的，所以我们通过访问第一个页面即可提取出目录内容。
然后通过response.read()来读取网页内容。
然后定义了一个继承自HTMLParser的hp类，同时定义了hp对象来解析网页内容。
我们来看看hp类的原理。
```
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
```
首先我们在handle_starttag函数中来匹配class="uk-nav uk-nav-side"的类，由于这样的类有两个，我们要匹配第二个，所以在self.cnt=2的时候设置匹配成功标志self.classGroup=True，其他的正文获取都是在匹配成功的前提下来进行操作的，所以都会有if self.classGroup== True的条件判断，通过观察网页内容，我们可以知道通过判断ul的结束符即可判断class="uk-nav uk-nav-side"的结束，而在handle_data函数中，我们就需要将读取到的内容保存到titleList，而地址实在节点头的href属性中的。

##获取目录对应的正文页。
接下来我们就要解析之前获取到的addrList各个地址的内容，套路跟获取目录差不多。
首先我们需要遍历titleList和addrList
```
for i in range(len(titleList)):
```
然后根据titleList的内容在本地新建一个html文件，并写入titleList的内容作为标题
```
filename=titleList[i].replace('/','_')		#titleList中的内容会用来作为文件名，所以首先需要替换文件名不支持的字符
filename=filename.replace('-','_')
currentPath='%s\\%d_%s.html' %(os.path.dirname(__file__),i,filename)
print(currentPath)
currentFile=open(currentPath,'w')
temp='<h1>%s</h1>\r\n' %(titleList[i])		#写入标题
currentFile.write(temp)
```
接着访问addrList对应的网页，并获取网页内容，预先定义好一个继承自HTMLParser的webContext类，通过这个类的对象来解析正文网页，并将正文按照相应的格式写入html文件中。
```
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
```
然后我们看看webContext类
handle_starttag负责节点头的处理和属性处理
```
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
```
首先匹配class="x-wiki-content"，查找到正文的开始地方。查找到第一个即表明匹配成功self.contextFlag=True。然后将节点头内容写入本地的html文件中，需要做特殊处理的就是img节点头。这个节点头的格式是这样的```<img src="xxxxxxx"/>```这个节点是只有节点头，没有节点尾，而且src对应的网址也有两种类型，一种绝对http型，一种相对本站性，相对本站性需要加上站头'http://www.liaoxuefeng.com'来形成完整的图片地址。然后在handle_data中解析并保存正文内容
```
def handle_data(self,data):
    if self.contextFlag == True:
        currentFile.write(data)
```
好了整个思路就是这样的，下面是运行效果


运行截图
![running][running]
保存截图
![htmlsave][htmlsave]
预览截图
![htmlview][htmlview]

[完整源码][mycode]

笔记：

1. 变量的作用域
2. 全局变量和局部变量以及global关键字
3. 文件操作
4. 全局变量与None
5. urllib库使用
6. HTMLParser工作机制
7. 网页访问机制
8. html dom文档结构


[referblog]:http://mp.weixin.qq.com/s?__biz=MjM5MzgyODQxMQ==&mid=2650366762&idx=1&sn=bfe7c2b4df42ff8669d6963602a0a9e1&chksm=be9cd87e89eb5168232334ef8cb164341138c6b8223464fe90eaf165691ba0751dfe1bec9f00&mpshare=1&scene=23&srcid=0216nHi7EfIghfjnC5x8POe1#rd
[code]:https://github.com/lzjun567/crawler_html2pdf
[mycode]:https://github.com/qiuzhiqian/CrawlHtml

[webstruct]:./doc/img/webstruct.png
[running]:./doc/img/running.png
[htmlsave]:./doc/img/htmlsave.png
[htmlview]:./doc/img/htmlview.png
