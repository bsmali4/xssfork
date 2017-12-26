##  重要说明
kali下无法使用的话，请下载正确的[phantomjs](http://phantomjs.org/download.html) 到目录thirdparty/phantomjs/Linux

更多信息访问[http://xssfork.secbug.net/](http://xssfork.secbug.net/)

由于使用的是phantomjs，所以使用期间可能会造成内存，cpu消耗过大。对网络造成的破坏，本人不负任何法律责任。

## 免责申明

xssfork保证竭诚为网络用户提供最安全的上网服务，但因不可避免的问题导致出现的问题，我们尽力解决，期间引起的问题我们不承担以下责任。
### 第 一 条

xssfork使用者因为违反本声明的规定而触犯中华人民共和国法律的，一切后果自己负担,xssfork.secbug.net站点以及作者不承担任何责任。
### 第 二 条

凡以任何方式直接、间接使用xssfork资料者，视为自愿接受xssfork.secbug.net声明的约束。
### 第 三 条

本声明未涉及的问题参见国家有关法律法规，当本声明与国家法律法规冲突时，以国家法律法规为准。
### 第 四 条

对于因不可抗力或xssfork不能控制的原因造成的网络服务中断或其它缺陷，xssfork.secbug.net网站以及作者不承担任何责任。
### 第 五 条
xssfork之声明以及其修改权、更新权及最终解释权均属xssfork.secbug.net网所有。



更多信息访问[http://xssfork.secbug.net/](http://xssfork.secbug.net/)

更新xssforkapi,提供分布式部署方案。
# 概述  
xssfork是新一代xss漏洞探测工具，其开发的目的是帮助安全从业者高效率的检测xss安全漏洞，关于xss的更多详情可以移步[Cross-site Scripting (XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS))。不管什么语言，传统的xss探测工具，一般都是采用第三方库向服务器发送一个注入恶意代码的请求，其工作原理是采用payload in response的方式，即通过检测响应包中payload的完整性来判断，这种方式缺陷，很多。
例如
1.不能检测dom类xss(无法从源代码中检查)
2.不能模拟真正的浏览器
3.网页js无法交互,第三方库不认识网页中的js的代码。
与传统的工具相比，xssfork使用的是 webkit内核的浏览器phantomjs，其可以很好的模拟浏览器。工具分为两个部分，xssfork和xssforkapi，其中xssfork在对网站fuzz xss的时候会调用比较多的payload。
# 两者结合  
可以使用xssforkapi来做批量xss检测工具,xssfork做深度fuzz工具。xssforkapi这种webservice方式十分适合分布式部署。
# 创建任务  
关于key,为了保证外部不能非法调用服务，xssforkapi采用的是http协议验证key的方式。
## key的获取方式  
在每次启动xssforkapi的时候，会将key写入到根目录authentication.key中，你也可以在每次启动服务的时候看到key。
![](http://ohsqlm7gj.bkt.clouddn.com/17-7-28/74466819.jpg)
key默认是每次启动服务不更新的，你也可以在下一次启动服务的时候强制更新，只需要启动的时候指定--refresh True即可。值得注意的时候，refresh指定为true之后，原有的保存在data目录下xssfork.db将会清除，这意味着你将清除你之前所有的检测纪录。
![](http://ohsqlm7gj.bkt.clouddn.com/17-7-28/52701244.jpg)
##新建扫描任务  
需要向服务传递两个参数,1.key(主要用于验证身份)；2.检测参数
### get协议检测
###创建任务
1.get反射型类型
```
req = requests.post('http://127.0.0.1:2333/xssfork/create_task/7T2o22NcQSLGk75',data=json.dumps({'url':'http://10.211.55.13/xss/example1.php?name=hacker', ), headers={'Content-Type':'application/json'})
return req.content
```
2.post反射类型
```
req = requests.post('http://127.0.0.1:2333/xssfork/create_task/7T2o22NcQSLGk75',data=json.dumps({'url':'http://10.211.55.13/xss/post_xss.php', 'data':'name=233'), headers={'Content-Type':'application/json'})
return req.content
```
3.get反射型类型，需要验证cookie
```
req = requests.post('http://127.0.0.1:2333/xssfork/create_task/7T2o22NcQSLGk75',data=json.dumps({'url':'http://10.211.55.13/xss/example1.php?name=hacker', 'cookie':'usid=admin'), headers={'Content-Type':'application/json'})
return req.content
```
4.post反射型类型，需要验证cookie
```
req = requests.post('http://127.0.0.1:2333/xssfork/create_task/7T2o22NcQSLGk75',data=json.dumps({'url':'http://10.211.55.13/xss/post_xss.php', 'data':'name=2333', 'cookie': 'usid=admin'), headers={'Content-Type':'application/json'})
return req.content
```
5.get储存型，需要验证cookie
```
req = requests.post('http://127.0.0.1:2333/xssfork/create_task/7T2o22NcQSLGk75',data=json.dumps({'url':'http://10.211.55.13/xss/example1.php?name=hacker', 'cookie':'usid=admin', 'destination': 'http://10.211.55.13/output.php'), headers={'Content-Type':'application/json'})
return req.content
```
4.post储存型，需要验证cookie
```
req = requests.post('http://127.0.0.1:2333/xssfork/create_task/7T2o22NcQSLGk75',data=json.dumps({'url':'http://10.211.55.13/xss/example1.php?name=hacker', 'data':'name=2333', 'cookie':'usid=admin', 'destination': 'http://10.211.55.13/output.php'), headers={'Content-Type':'application/json'})
return req.content
```
返回码

```
{"status": "success", "task_id": "1"}
```
调用者可以获取到任务id，以便于启动检测。
#启动任务
```
import requests
req = requests.get('http://127.0.0.1:2333/xssfork/start_task/tM0Xnl0qD6nsHku/%s' % (task_id))
print req.content
```
返回码

```
{"status": "success", "msg": "task will start"}
```
#查看状态
```
import requests
req = requests.get('http://127.0.0.1:2333/xssfork/task_status/tM0Xnl0qD6nsHku/%s' % (task_id))
print req.content
```
返回码分为4种，分别如下:  
1.任务不存在
```
{"status": -1, "msg": "task isn’t existed"}
```  
2.任务创建了，但是未启动
```
{"status": 0, "msg": "task isn't started"}
```  
3.任务正在作业中，未完成
```
{"status": 1, "msg": "task is working"}
```  
4.任务作业完成
```
{"status":2, "msg": "task has been done"}
```
#获取结果
```
req = requests.get('http://127.0.0.1:2333/xssfork/task_result/7T2o22NcQSLGk75/%s' % (task_id))
	print req.content
```
返回分为两种  
1.检测到漏洞，并且返回payload
```
{"payload": "{'url': "http://10.211.55.13/xss/example1.php?name=%22<xss></xss>//", 'data': null}"}
```  
2.未检测到漏洞
```
{"payload": null}
```
#结束任务
```
req = requests.get('http://127.0.0.1:2333/xssfork/kill_task/7T2o22NcQSLGk75/%s' % (task_id))
	print req.content
```
返回结果可能有4种
1.结束任务失败，因为任务不存在
```
{"status": "false", "msg": "task isn’t existed"}
```  
2.结束任务失败，因为任务根本没启动
```
{"status": "false", "msg": "task isn't started"}
```  
3.结束任务失败，因为任务本已经结束，不需要强制杀死
```
{"status": "false", "msg": "task has been done"}
```  
4.结束任务成功，任务原本是处于运行中的状态
```
{"status": "success", "msg": "task will be killed"}
```
#完整的例子
1.一次带有cookie验证的post xss
漏洞示例代码
```
<?php
if (isset($_COOKIE['usid']) && isset($_POST['id']))
{
	if ($_COOKIE['usid']=="admin")
		{
			echo $_POST['id'];
		}
}
?>
```
客户端代码
```
#! /usr/bin/env python
# coding=utf-8
import json
import time
import requests


def creat_task(url, data, cookie):
    json_data = json.dumps({'url': url, 'data': data, 'cookie': cookie})
    req = requests.post('http://127.0.0.1:2333/xssfork/create_task/7T2o22NcQSLGk75', data=json_data, headers={'Content-Type':'application/json'})
    return req.content


def start_task(task_id):
    req = requests.get('http://127.0.0.1:2333/xssfork/start_task/7T2o22NcQSLGk75/{}'.format(task_id))
    return req.content


def get_task_status(task_id):
    req = requests.get('http://127.0.0.1:2333/xssfork/task_status/7T2o22NcQSLGk75/{}'.format(task_id))
    return req.content


def get_task_result(task_id):
    req = requests.get('http://127.0.0.1:2333/xssfork/task_result/7T2o22NcQSLGk75/{}'.format(task_id))
    return req.content


def running(task_id):
    time.sleep(5)
    task_status = int(json.loads(get_task_status(task_id)).get('status'))
    return task_status in [0, 1]


if __name__ == "__main__":
    url = "http://10.211.55.3/xsstest/cookie_xss_post.php"
    data = "id=1"
    cookie = "usid=admin"
    task_id = json.loads(creat_task(url, data, cookie)).get('task_id')
    start_task(task_id)
    while running(task_id):
        print "the task is working"
    print get_task_result(task_id)

```


效果

![](http://ohsqlm7gj.bkt.clouddn.com/17-7-28/70449749.jpg)

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
基础payload会在现有的基础上，会添加上各种闭合的情况。
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
 
 支持伪静态的检测
## 说明
开源只为分享，请勿将本脚本做任何商业性质的集成。开发的时候，有可能很多情况没有考虑到，如果你有更好的建议或者发现bug，
root@codersec.net  
开源地址 https://github.com/bsmali4/xssfork
记得不要吝啬你的star

更新日志:2017-10-24 修复卡住进度bug
