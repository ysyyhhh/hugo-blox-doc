# Netty

Netty是一个异步的、事件驱动的网络应用框架，用于快速开发高性能、高可靠性的网络服务器和客户端程序。

##  I/O模型

Netty的I/O模型是Reactor模型，Reactor模型是一种事件驱动模型，当有事件发生时，会调用相应的事件处理器进行处理。

BIO (Blocking I/O)：同步阻塞I/O模型，一个连接一个线程，即客户端有连接请求时服务端就需要启动一个线程进行处理，如果这个连接不做任何事情会造成不必要的线程开销。

NIO (Non-blocking I/O)：同步非阻塞I/O模型，一个线程处理多个连接，即客户端发送的连接请求都会注册到多路复用器上，多路复用器轮询到连接有I/O请求就进行处理。

AIO (Asynchronous I/O)：异步非阻塞I/O模型，AIO引入异步通道的概念，采用了Proactor模式，简化了程序编写，有效的请求才启动线程，它的特点是先由操作系统完成后才通知服务端启动线程去处理，一般适用于连接数较多且连接时间较长的应用。

## Netty的介绍

Netty是一个基于NIO的客户、服务器端编程框架，使用Netty可以快速开发网络应用，例如实现一个高性能的协议服务器/客户端。

NIO的缺点 && Netty的价值

NIO的编程模型相对底层，对开发人员的要求较高，需要了解Selector、Channel、Buffer等概念，开发工作量和难度较大。
NIO在面对复杂的网络应用时，容易出现Reactor模型中的两个重要问题：粘包和拆包。

粘包和拆包
- 粘包：多个小的包粘在一起发送，接收端无法区分
- 拆包：一个大的包被拆分成多个小的包发送，接收端无法区分

Netty优点
- API使用简单，开发工作量小
- 自带的编解码器，可以很好的解决粘包和拆包问题
- 简单的线程模型，可以处理成千上万的连接
- 自带各种协议栈
- 真正的无连接，无状态，高性能

Netty的应用场景
- 作为RPC框架的网络通信模块
- 实现HTTP服务器，功能包括处理常见的HTTP请求、响应、编解码、文件服务等
- 实现自定义的协议服务器，例如实现一个简单的聊天服务器
- 实现消息推送服务器，例如实现一个简单的即时通讯服务器

使用了Netty的开源项目
- Dubbo
- RocketMQ
- Elasticsearch
- Zookeeper
- gRPC


## Netty的核心组件

Channel：通道，Java NIO中的基础概念，代表一个打开的连接，可执行读取/写入操作。Netty对Channel的所有操作都是非阻塞的。

ChannelFuture：Java的Future接口的扩展，代表一个还没有发生的I/O操作。

EventLoop：事件循环，一个线程，一个EventLoop可以处理多个Channel，一个Channel只对应一个EventLoop。

ChannelHandler：事件处理器，处理I/O事件或者拦截I/O操作，并将其转发到其ChannelPipeline(业务逻辑处理链)中的下一个处理器。

ChannelPipeline：事件处理链，负责ChannelHandler的调度和执行。

ByteBuf：一个字节容器，Netty对ByteBuffer进行了封装，提供了更加强大和灵活的功能。

## Netty的使用

Netty的使用主要分为两个部分：服务端和客户端。


## Reactor线程模型

Reactor线程模型是Netty的核心，它是Netty高性能的关键。

Reactor线程模型是一种基于事件驱动的设计模式，主要用于处理并发I/O操作。

单线程Reactor模型
- 一个线程处理所有的I/O事件，包括接收客户端的连接、读取数据、发送数据等。
- 优点：编程简单，没有线程切换的开销
- 缺点：性能瓶颈，无法充分利用多核CPU

多线程Reactor模型

- 一个线程负责接收客户端的连接，多个线程负责处理I/O事件
- 优点：充分利用多核CPU
- 缺点：编程复杂，需要处理线程同步和数据共享问题
  - 并发连接数多时存在性能问题

主从Reactor模型

- 一组线程负责接收客户端的连接，一组线程负责处理I/O事件