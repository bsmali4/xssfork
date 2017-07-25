## xssfork简介
xssfork作为sicklescan的一个功能模块，其开发主要目的是用于检测xss漏洞。
传统的xss探测工具，一般都是采用 payload in response的方式，即在发送一次带有payload的http请求后，通过检测响应包中payload的完整性来判断，这种方式缺陷，很多。  
第一：不能准确地检测dom类xss  
第二：用类似于requests之类的库不能真正的模拟浏览器  
第三：网页js无法交互  
怎么解决？如果能够用浏览器代替这个模块，去自动hook是最好的。所幸，我了解到phantomjs，当然现在google浏览器也支持headless模式，类似的，你也可以采用google浏览器去做检测。
## 原理
对于这类fuzz过程,基本都是预先准备好一些payload,然后加载执行。对于这类io型密集的扫描模型，后端使用多线程就比较适用，但是由于phantomjs你可以理解为一个无界面的浏览器，在加载的时候，其缺陷也比较明显，比较吃内存，用它来发包自然不像requests库轻量。
## 编码脚本
由于基础的payload模块，我收集了71个。
![](http://ohsqlm7gj.bkt.clouddn.com/17-7-24/38956876.jpg)
基础pyaload会在现有的基础上，会添加上各种闭合的情况。
![](http://ohsqlm7gj.bkt.clouddn.com/17-7-24/58148554.jpg)
除了这些基础的payload,xssfork还提供了几个编码脚本，查看脚本，可以看help
![](http://ohsqlm7gj.bkt.clouddn.com/17-7-24/12237078.jpg)
现阶段提供了10进制，16进制，随机大小写，关键字叠加四个脚本。
### 10hex_encode
将html标签内部字符10进制化
&lt;a href=&#x6a&#x61&#x76&#x61&#x73&#x63&#x72&#x69&#x70&#x74&#x3a&#x61&#x6c&#x65&#x72&#x74&#x28&#x36&#x35&#x35&#x33&#x34&#x29&#x3b&gt;aaa&lt;/a&gt;
![](http://ohsqlm7gj.bkt.clouddn.com/17-7-24/19641734.jpg)
其效果如下
![](http://ohsqlm7gj.bkt.clouddn.com/17-7-24/26774362.jpg)

### 16hex_encode
将html标签内部字符16进制化
### uppercase
随机大小写
将
&lt;script&gt;alert(65534);&lt;/script&gt;
转换成
&lt;ScRIPt&gt;alert(65534);&lt;/ScRIpT&gt;
### addkeywords
主要是应对过滤为replace('keyword&gt;s','')的情况  
&lt;script&gt;alert(65534);&lt;/script&gt;
变成
&lt;&lt;script&gt;script&gt;alert(65534);&lt;/script&gt;
当然默认开启的是轻量模式，即只返回一个payload，开启重量模式，可以生成更加丰富的pyaload，效果如下
&lt;script&gt;alert(65534);&lt;/script&gt;  
&lt;script&gt;alert(65534);&lt;/ScrIpt&gt;  
&lt;ScrIpt&gt;alert(65534);&lt;/sCrIpt&gt;  
&lt;scRiPt&gt;alert(65534);&lt;/script&gt;  
&lt;ScrIpt&gt;alert(65534);&lt;/script&gt;
## 演示
场景1.反射型xss  
![](http://shentoushi.top/manypic/Uploads/2016-09-26/%E5%8F%8D%E5%B0%84%E5%9E%8Bxss.gif)  
场景2.大小写绕过  
![](http://shentoushi.top/manypic/Uploads/2016-09-26/%E5%A4%A7%E5%B0%8F%E5%86%99%E7%BB%95%E8%BF%871%20xss.gif)
![](http://shentoushi.top/manypic/Uploads/2016-09-26/%E5%A4%A7%E5%B0%8F%E5%86%99%E7%BB%95%E8%BF%872%20xss.gif)  
场景3.dom型xss  
![](http://shentoushi.top/manypic/Uploads/2016-09-26/dom%20xss1.gif)
![](http://shentoushi.top/manypic/Uploads/2016-09-26/dom%20xss2.gif)
场景3.post类型
![](http://shentoushi.top/manypic/Uploads/2016-09-26/post%20xss1.gif)
场景4.需要验证cookie
![](http://shentoushi.top/manypic/Uploads/2016-09-26/cookie%20xss.gif)


![](http://ohsqlm7gj.bkt.clouddn.com/2017-07-24%20at%20%E4%B8%8B%E5%8D%884.23.gif)
![](http://ohsqlm7gj.bkt.clouddn.com/2017-07-24%20at%20%E4%B8%8B%E5%8D%884.27.gif)
 post类型  
 python xssfork.py -u "xx" -d "xx"
 存储型  
 python xssfork.py -u "xx" -d "xxx" -D "输出位置"
 带cookie
 python xssfork.py -u "xx" -c "xx"
## 说明
开源只为分享，请勿将本脚本做任何商业性质的集成。开发的时候，有可能很多情况没有考虑到，如果你有更好的建议或者发现bug，可以联系我邮箱,xssfork.codersec.net网站还在建设中,github不要吝啬你的star。
root@codersec.net  
开源地址 https://github.com/bsmali4/xssfork
记得不要吝啬你的star

