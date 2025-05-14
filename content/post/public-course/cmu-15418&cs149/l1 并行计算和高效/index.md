---
title: 'Why parallelism? Why efficiency?'
date: 2024-03-01
lastmod: 2025-05-14
author: ['Ysyy']
categories: ['']
tags: ['cmu-15418&cs149']
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
## Parallelism

加速比 Speed up 是指：
程序在单处理器上运行的时间 / 程序在多处理器上运行的时间

我们一般会期望用两倍的硬件得到两倍的速度提升,但是实际上并不是这样的。

制约性能提升可能的因素有:

- 资源分配不均匀
- 通信开销
- 短板效应
- 共享资源读写冲突

为什么要去了解硬件？

- 什么是限制性能的因素？
- 导致性能瓶颈的原因是什么？

## Efficiency

fast != efficient

- 什么是效率？
  尽可能地利用资源，减少浪费

比如按时间租用服务器。

## 总结

并行程序的挑战：

- 负载均衡 Load balance
- 通信延迟 Communication latency
- 集体工作时，真正用于计算的时间很少