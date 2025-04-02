---
title: '6.5840 Lab 1: MapReduce'
date: 2024-03-05
lastmod: 2025-04-02
author: ['Ysyy']
categories: ['']
tags: ['mit-6.5840(6.824)']
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
## Introduction
在这个实验中，你将构建一个 MapReduce 系统。你将实现一个工作节点进程，调用应用程序的 Map 和 Reduce 函数，处理文件的读写，以及一个协调器进程，向工作节点分发任务，并处理失败的工作节点。你将构建类似于 [MapReduce 论文](https://pdos.csail.mit.edu/6.824/labs/lab-mr.html)中描述的系统。（注意：**这个实验使用“协调器”而不是论文中的“主节点”。**）




## Getting started

准备工作:
[安装Go](https://pdos.csail.mit.edu/6.824/labs/go.html)
[安装Git](https://git-scm.com/)

获取项目:
```bash
git clone git://g.csail.mit.edu/6.5840-golabs-2024 6.5840
cd 6.824
ls
# 输出为 Makefile  src
```

我们为你提供了一个简单的顺序 MapReduce 实现，位于 src/main/mrsequential.go 中。
它一次只在单个进程中运行一个 Map 和一个 Reduce。

我们还为你提供了几个 MapReduce 应用程序：在 `mrapps/wc.go` 中是单词计数，而在 `mrapps/indexer.go` 中是文本索引器。你可以按顺序运行单词计数如下：

```bash
# 生成 wc.so 文件
go build -buildmode=plugin ../mrapps/wc.go

# 删除 mr-out* 文件 这是输出文件
rm mr-out*

# 运行 mrsequential.go 使用 wc.so 插件处理 pg*.txt 文件, 这是提供的线性处理程序
# pg*.txt 是输入文件, 包含了一些文本
go run mrsequential.go wc.so pg*.txt

# 查看输出文件 mr-out-0 的内容
more mr-out-0
```

Go 将其输出保留在文件 mr- out-0中，输入来自名为 pg-xxx.txt 的文本文件。

可以随意借用 mrSequential.go 的代码。您还应该查看 mrapps/wc.go，看看 MapReduce 应用程序代码是什么样的。


## 任务

你的任务是实现一个分布式的 MapReduce，包括两个程序，协调器和工作节点。将只有一个协调器进程，以及一个或多个并行执行的工作节点进程。在一个真实的系统中，工作节点可能会在一堆不同的机器上运行，但是对于这个实验，你会将它们全部运行在单个机器上。工作节点将通过 RPC 与协调器通信。

每个工作节点进程都会循环询问协调器要一个任务，从一个或多个文件中读取任务的输入，执行任务，将任务的输出写入一个或多个文件，然后再次向协调器请求一个新的任务。

如果一个工作节点在合理的时间内（在这个实验中，使用十秒）没有完成它的任务，协调器应该注意到，并将相同的任务分配给另一个工作节点。


协调器和 worker 的“ main”例程位于 main/mrCollaborator.go 和 main/mrworker.go 中; 不要更改这些文件。

只修改mr/coordinator.go, mr/worker.go, and mr/rpc.go

### 示例
下面是如何在单词计数 MapReduce 应用程序上运行代码的方法。首先，确保单词计数插件是新构建的:

```bash
go build -buildmode=plugin ../mrapps/wc.go 
rm mr-out* 
go run mrcoordinator.go pg-*.txt
```
其中 pg-.txt 参数是输入文件；每个文件对应一个“分片”，是一个 Map 任务的输入。

然后,在一个或多个其他窗口中，运行一些工作节点：
`go run mrworker.go wc.so`

在`mr-out-*`文件中，可以单词计数的输出。



当coordinator完成所有任务后, 会输出如下内容:
```bash
cat mr-out-* | sort | more
```


### 测试

我们在 main/test-mr.sh 中为你提供了一个测试脚本。
这些测试检查当给定 pg-xxx.txt 文件作为输入时，wc 和 indexer MapReduce 应用程序是否产生正确的输出。
测试还会检查你的实现是否并行运行 Map 和 Reduce 任务，并且你的实现是否能够从在运行任务时崩溃的工作节点中恢复。

运行测试脚本的方法如下：
```bash
bash test-mr.sh
```

tips:

> 如果现在直接执行mrcoordinator会一直卡在那, 因为`mr/coordinator.go`中的Done函数没有被实现.
> 一直返回false, 无法结束任务.
> 如果想先测试一下流程,直接把`mr/coordinator.go`中的`Done`函数改成`return true`就可以了.


这个测试脚本会输出到 `mr-out-X`中

如果全部完成了,可以看到输出的内容:
```bash
*** Starting wc test.
--- wc test: PASS
*** Starting indexer test.
--- indexer test: PASS
*** Starting map parallelism test.
--- map parallelism test: PASS
*** Starting reduce parallelism test.
--- reduce parallelism test: PASS
*** Starting job count test.
--- job count test: PASS
*** Starting early exit test.
--- early exit test: PASS
*** Starting crash test.
--- crash test: PASS
*** PASSED ALL TESTS
```

### 一些可以忽略的问题

`rpc.Register: method "Done" has 1 input parameters; needs exactly three`
这个
将协调器注册为 RPC 服务器检查它的所有方法是否适合 RPC (有3个输入) ; 
我们知道RPC并没有调用 Done。


另外，根据你终止工作进程的策略，你可能会看到一些形式的错误。
` dialing:dial unix /var/tmp/5840-mr-501: connect: connection refused`
每个测试可以看到一些这样的消息; 当协调器退出后，工作者无法与协调器 RPC 服务器联系时，就会出现这些消息。


## A few rules

- Map 阶段应该将中间键分成 nReduce 个 reduce 任务的桶，其中 nReduce 是 reduce 任务的数量 -- 这是 main/mrcoordinator.go 传递给 MakeCoordinator() 的参数。每个 Mapper 应该为 Reduce 任务创建 nReduce 个中间文件以供使用。

- Worker 的实现应该将第 X 个 reduce 任务的输出放入文件 mr-out-X 中。

- mr-out-X 文件应该包含一个 Reduce 函数输出的行。这一行应该用 Go 的 "%v %v" 格式生成，调用时传入键和值。在 main/mrsequential.go 中找到被注释为 "这是正确的格式" 的行。如果你的实现与这个格式相差太远，测试脚本会失败。

- 你可以修改 mr/worker.go、mr/coordinator.go 和 mr/rpc.go。你可以临时修改其他文件进行测试，但确保你的代码与原始版本一起工作；我们将使用原始版本进行测试。

- Worker 应该将中间 Map 输出放在当前目录中的文件中，以便稍后的 Reduce 任务读取它们作为输入。

- main/mrcoordinator.go 期望 mr/coordinator.go 实现一个 Done() 方法，在 MapReduce 作业完全完成时返回 true；此时，mrcoordinator.go 将退出。

- 当作业完全完成时，工作进程应该退出。实现这一点的一个简单方法是使用 call() 的返回值：如果工作节点无法联系到协调器，它可以假设协调器已经退出，因为作业已经完成，所以工作节点也可以终止。根据你的设计，你可能还会发现有一个“请退出”的伪任务对协调器给工作节点很有帮助。

## Hints

- [指南页面](https://pdos.csail.mit.edu/6.824/labs/guidance.html)上有一些关于开发和调试的提示。
- 开始的一种方法是修改 mr/worker.go 中的 Worker()，向协调器发送一个 RPC 请求任务。然后修改协调器以响应一个尚未启动的 Map 任务的文件名。然后修改工作节点以读取该文件并调用应用程序的 Map 函数，就像在 mrsequential.go 中一样。
- 应用程序的 Map 和 Reduce 函数是在运行时使用 Go 插件包加载的，文件的名称以 .so 结尾。
- 如果你改变了 mr/ 目录中的任何内容，你可能需要重新构建你使用的任何 MapReduce 插件，例如使用 go build -buildmode=plugin ../mrapps/wc.go。
- 这个实验依赖于**工作节点共享文件系统**。当所有工作节点运行在同一台机器上时，这很简单，但如果工作节点在不同的机器上运行，则需要像 GFS 这样的全局文件系统。
- 中间文件的一个合理命名约定是 mr-X-Y，其中 X 是 Map 任务编号，Y 是 reduce 任务编号。
- 工作节点的 Map 任务代码将需要一种方法来将**中间键/值对存储在文件中**，以便在 reduce 任务期间正确读取回来。一种可能性是使用 Go 的 encoding/json 包。要将键/值对以 JSON 格式写入到打开的文件中：
  ```go
    enc := json.NewEncoder(file)
    for _, kv := ... {
    err := enc.Encode(&kv)
  ```
  并读取回来：
  ```go
    dec := json.NewDecoder(file)
    for {
        var kv KeyValue
        if err := dec.Decode(&kv); err != nil {
          break
        }
        kva = append(kva, kv)
    }
  ```
- 你的工作节点的 Map 部分可以使用 ihash(key) 函数（在 worker.go 中）来选择给定键的 reduce 任务。
- 你可以从 mrsequential.go 中偷一些代码来读取 Map 输入文件，对 Map 和 Reduce 之间的中间键/值对进行排序，并将 Reduce 输出存储在文件中。
- 作为一个 RPC 服务器的协调器将是并发的；不要忘记锁定共享数据。
- 使用 Go 的竞争检测器，使用 go run -race。test-mr.sh 在开头有一条注释，告诉你如何用 -race 运行它。当我们评估你的实验时，我们不会使用竞争检测器。**尽管如此，如果你的代码有竞争条件，即使没有竞争检测器，也有很大可能会在我们测试时失败**。
- 工作节点有时需要等待，例如在最后一个 Map 完成之前不能开始 Reduce。一种可能性是让工作节点定期向协调器请求工作，在每个请求之间使用 time.Sleep() 进行睡眠。另一种可能性是让协调器中相应的 RPC 处理程序具有等待循环，可以使用 time.Sleep() 或 sync.Cond 进行等待。Go 在自己的线程中运行每个 RPC 的处理程序，因此一个处理程序在等待时不会阻止协调器处理其他 RPC。
- 协调器不能可靠地区分崩溃的工作节点、仍然存活但由于某种原因停滞不前的工作节点以及执行但速度太慢以至于无用的工作节点。你能做的最好的事情是让协调器等待一段时间，然后放弃并将任务重新分配给另一个工作节点。对于这个实验，让协调器等待十秒；之后，**协调器应该假设工作节点已经死亡**（当然，它可能没有）。
- 如果选择实现备份任务（第 3.6 节），请注意我们测试你的代码在工作节点执行任务而不崩溃时不安排多余的任务。备份任务应该只在一段相对较长的时间（例如，10 秒）之后才被安排。
- 为了测试崩溃恢复，你可以使用 mrapps/crash.go 应用程序插件。它会在 Map 和 Reduce 函数中随机退出。
- 为了确保在崩溃的情况下没有人观察到部分写入的文件，MapReduce 论文提到了使用临时文件并在完全写入后以原子方式重命名它的技巧。你可以使用 ioutil.TempFile（或者如果你正在运行 Go 1.17 或更高版本，则可以使用 os.CreateTemp）来创建临时文件，并使用 os.Rename 来原子地重命名它。
- test-mr.sh 在子目录 mr-tmp 中运行所有进程，所以如果出了问题，你想查看中间文件或输出文件，请查看那里。可以随意暂时修改 test-mr.sh，在失败的测试后退出，这样脚本就不会继续测试（并覆盖输出文件）。
- test-mr-many.sh 连续多次运行 test-mr.sh，这样做可以帮助你发现低概率的错误。它接受一个参数，指定运行测试的次数。你不应该并行运行多个 test-mr.sh 实例，因为协调器会重用相同的套接字，导致冲突。
- Go RPC 只发送字段名称以大写字母开头的结构字段。子结构体也必须具有大写的字段名称。
- 在调用 RPC 的 call() 函数时，应答结构体应包含所有默认值。RPC 调用应该像这样：
  ```go
      reply := SomeType{}
      call(..., &reply)
  ```
  在调用之前不设置任何 reply 字段。如果传递具有非默认字段的 reply 结构体，则 RPC 系统可能会静默返回不正确的值。

## 挑战

- 实现你自己的 MapReduce 应用程序（参见 mrapps/* 中的示例），例如，分布式 Grep（MapReduce 论文第 2.3 节）。

- 让你的 MapReduce 协调器和工作节点在不同的机器上运行，就像在实际中一样。你需要设置你的 RPC 以通过 TCP/IP 进行通信，而不是 Unix 套接字（参见 Coordinator.server() 中的注释行），并使用共享文件系统进行文件读写。例如，你可以 ssh 进入麻省理工学院的多个 Athena 集群机器，它们使用 AFS 共享文件；或者你可以租用几个 AWS 实例，并使用 S3 进行存储。