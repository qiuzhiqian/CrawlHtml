本文档参考了该[博客][referblog]和其[源代码][code]

不过为了方便，我没有使用beautifulsoup和pdfkit，而是直接通过python自带的HTMLParser来处理html，然后解析出html中的主体内容，然后重新生成一个新的html，并重命名为章节内容。

运行截图
![running][running]
保存截图
![htmlsave][htmlsave]
预览截图
![htmlview][htmlview]

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

[running]:./doc/img/running.png
[htmlsave]:./doc/img/htmlsave.png
[htmlview]:./doc/img/htmlview.png