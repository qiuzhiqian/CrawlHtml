本文档参考了该[博客][referblog]和其[源代码][code]

不过为了方便，我没有使用beautifulsoup和pdfkit，而是直接通过python自带的HTMLParser来处理html，然后解析出html中的主体内容，然后重新生成一个新的html，并重命名为章节内容。

[referblog]:http://mp.weixin.qq.com/s?__biz=MjM5MzgyODQxMQ==&mid=2650366762&idx=1&sn=bfe7c2b4df42ff8669d6963602a0a9e1&chksm=be9cd87e89eb5168232334ef8cb164341138c6b8223464fe90eaf165691ba0751dfe1bec9f00&mpshare=1&scene=23&srcid=0216nHi7EfIghfjnC5x8POe1#rd
[code]:https://github.com/lzjun567/crawler_html2pdf