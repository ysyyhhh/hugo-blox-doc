---
title: '杂'
date: 2023-07-23
lastmod: 2024-04-17
author: ['Ysyy']
categories: ['']
tags: ['qa']
description: ''
weight: None
draft: False
comments: True
showToc: True
TocOpen: True
hidemeta: False
disableShare: False
showbreadcrumbs: True
summary: ''
---
session权限问题

<https://blog.51cto.com/u_15162069/2778036>

##### RSA前后端解密出错

14：07

JSEncrypt支持的是[openssl](https://so.csdn.net/so/search?q=openssl&spm=1001.2101.3001.7020)生成的pkcs1格式私钥，java需要pkcs8格式私钥，公钥格式不变

前端加入替换 encodeURI(encodeData).replace(/\\+/g, '%2B')

后端接口加入 URLDecoder.decode(password,"UTF-8");

<https://blog.csdn.net/qq_42979402/article/details/109184787>

真正错误是密码加了hash函数后，返回值是数字而不是字符串！！！

#### 数据库返回乱码

https://www.cnblogs.com/fanbi/p/13940432.html

#### [实际上是apigateway 放入 header 后再取出 乱码](https://blog.csdn.net/qq_31277409/article/details/118544597)

#### 存储过程返回多结果集并接收

#### test时报错 AOP之类的

[禁用字节码校验](https://blog.csdn.net/crxk_/article/details/103196146)