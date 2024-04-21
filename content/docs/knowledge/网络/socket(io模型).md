# I/O模型

## 一、什么是I/O模型 及 I/O模型的分类

Unix 有五种 I/O 模型：

阻塞式 I/O
非阻塞式 I/O
I/O 复用（select 和 poll）
信号驱动式 I/O（SIGIO）
异步 I/O（AIO）


## I/O 多路复用

它可以让单个进程具有处理多个 I/O 事件的能力。又被称为 Event Driven I/O，即事件驱动 I/O。

### select

### poll

### epoll





## 实际应用

### Reactor模式

### Proactor模式

### 事件驱动模式

## Socket

Socket listen怎么监听到TCP连接

释放连接的状态转换


