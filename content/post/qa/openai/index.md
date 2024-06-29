---
title: 'openai 相关QA'
date: 2023-12-08
lastmod: 2024-06-29
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
## 无法连接

Q:

```shell
openai.error.APIConnectionError: Error communicating with OpenAI: HTTPSConnectionPool(host='api.openai.com', port=443): Max retries exceeded with url: /v1/chat/completions (Caused by ProxyError('Unable to connect to proxy', SSLError(SSLZeroReturnError(6, 'TLS/SSL connection has been closed (EOF) (_ssl.c:1131)'))))
```

A:

```shell
问题出在模块 urllib3 的版本，报错的是 1.26.3，没报错的是 1.25.11

在原报错环境中使用下面命令重装低版本 urllib3：

pip install urllib3==1.25.11
然后测试果然就没问题了。
```