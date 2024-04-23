# Linux命令

## 常用命令

ls
mkdir
cp
mv


nohup


df


## QA
文件过滤用什么, 用法
grep

grep命令一般怎么使用？
grep [option] pattern file


Linux统计一个文件有多少行的命令？
wc -l filename

## 资源相关

### 内存相关

内存查看
free -m

内存使用情况
```shell
              total        used        free      shared  buff/cache   available
Mem:           1888         155        1406           0         326        1616
Swap:          2047           0        2047
```

- total: 总内存
- used: 已使用内存
- free: 空闲内存
- shared: 共享内存
- buff/cache: 缓存内存
- available: 可用内存

### 磁盘相关

磁盘查看
df -h

磁盘使用情况
```shell
Filesystem      Size  Used Avail Use% Mounted on
udev            935M     0  935M   0% /dev
tmpfs           192M  1.4M  191M   1% /run

```

- Size: 总磁盘大小
- Used: 已使用磁盘大小
- Avail: 可用磁盘大小
- Use%: 使用百分比
- Mounted on: 挂载点

### CPU相关

CPU查看
top

CPU使用情况
```shell
top - 10:00:01 up  1:00,  1 user,  load average: 0.00, 0.00, 0.00
Tasks:  88 total,   1 running,  87 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem :  1936 total,  1456 free,   116 used,   364 buff/cache

```

- load average: 1分钟、5分钟、15分钟的平均负载
- Tasks: 进程信息
- %Cpu(s): CPU使用情况
- KiB Mem: 内存使用情况

## 进程相关

### 进程查看

ps
含义: 显示当前用户的进程信息
不加aux的话, 只会显示当前终端的进程

ps aux
含义: a表示显示所有进程，u表示显示用户信息，x表示显示没有控制终端的进程

ps -ef
- e: 显示所有进程
- f: 显示全格式

ps -ef | grep java

输出:
```shell
root      1023     1  0 10:00 ?        00:00:00 /usr/bin/java
```


找内存占用最高的进程
ps aux --sort=-%mem | head





## 网络相关

### 网络配置查看

ifconfig
包含的信息:

```
eth0      Link encap:Ethernet  HWaddr 00:0C:29:3D:5D:7A
          inet addr:
            Bcast:
            Mask:
            inet6 addr:
            UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
            RX packets:0 errors:0 dropped:0 overruns:0 frame:0
            TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
            collisions:0 txqueuelen:1000

```
网口的连接状态标志: UP表示网口已经启用，DOWN表示网口未启用, RUNNING表示网口正在运行，而STOPPED表示网口已经停止

MTU大小: 默认值是 1500 字节，其作用主要是限制网络包的大小，如果 IP 层有一个数据报要传，而且网络包的长度比链路层的 MTU 还大，那么 IP 层就需要进行分片

网口的 IP 地址、子网掩码、MAC 地址、网关地址

网络包收发的统计信息

- RX packets: 接收的数据包的数量
- TX packets: 发送的数据包的数量

errors: 出错的数据包的数量
dropped: 丢弃的数据包的数量
overruns: 数据包在接收时超出了缓冲区的大小
frame: 数据包在接收时出现了 CRC 错误

### socket信息查看

netstat
含义: 显示网络状态信息

netstat -an
含义: 显示所有的网络连接，不进行域名解析
输出
```
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0
tcp6       0      0
udp        0      0
udp6       0      0
```

netstat -an | grep 8080
含义: 查看端口是否被占用


ss
含义: 显示套接字信息

ss -ltnp
- l: 显示LISTIEN监听状态的套接字
- t: 显示 TCP 协议的套接字
- n: 不显示名字,而是以数字的方式显示ip和端口
- p: 显示进程信息

输出
```
State      Recv-Q Send-Q Local Address:Port               Peer Address:Port
LISTEN     0      128
```


都包含了:

socket 的状态（State）
接收队列（Recv-Q）
发送队列（Send-Q）
本地地址（Local Address）
远端地址（Foreign Address）
进程 PID 
进程名称（PID/Program name）

接收队列（Recv-Q）和发送队列（Send-Q）比较特殊，在不同的 socket 状态。它们表示的含义是不同的。

当 socket 状态处于 Established时：

Recv-Q 表示 socket 缓冲区中还没有被应用程序读取的字节数；
Send-Q 表示 socket 缓冲区中还没有被远端主机确认的字节数；

而当 socket 状态处于 Listen 时：

Recv-Q 表示全连接队列的长度；
Send-Q 表示全连接队列的最大长度；

![](img/Linux命令/TCP三次握手.png)

全连接队列指的是服务器与客户端完了 TCP 三次握手后，还没有被 accept() 系统调用取走连接的队列。


### 网络吞吐量查看

sar
含义: 查看系统的网络吞吐量

用法是给 sar 增加 -n 参数就可以查看网络的统计信息，比如

sar -n DEV，显示网口的统计数据；
sar -n EDEV，显示关于网络错误的统计数据；
sar -n TCP，显示 TCP 的统计数据

输出

```
10:00:01        IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s
10:10:01        eth0
10:20:01        eth0
```

它们的含义：

rxpck/s 和 txpck/s 分别是接收和发送的 PPS，单位为包 / 秒。
rxkB/s 和 txkB/s 分别是接收和发送的吞吐率，单位是 KB/ 秒。
rxcmp/s 和 txcmp/s 分别是接收和发送的压缩数据包数，单位是包 / 秒。

对于带宽，我们可以使用 ethtool 命令来查询，它的单位通常是 Gb/s 或者 Mb/s，不过注意这里小写字母 b ，表示比特而不是字节。我们通常提到的千兆网卡、万兆网卡等，单位也都是比特（bit）。如下你可以看到， eth0 网卡就是一个千兆网卡：


### 连通性和延时

ping
含义: 测试网络连通性

ping -c 4 www.baidu.com

- c: 指定发送的数据包数量
- i: 指定发送数据包的时间间隔
- s: 指定发送数据包的大小

输出
```
PING baidu.com (39.156.66.10) 56(84) bytes of data.
64 bytes from 39.156.66.10 (39.156.66.10): icmp_seq=1 ttl=50 time=24.2 ms
64 bytes from 39.156.66.10 (39.156.66.10): icmp_seq=2 ttl=50 time=23.1 ms
64 bytes from 39.156.66.10 (39.156.66.10): icmp_seq=3 ttl=50 time=25.8 ms
^C
--- baidu.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2053ms
rtt min/avg/max/mdev = 23.114/24.375/25.778/1.092 ms
```

- icmp_seq: ICMP 数据包的序列号
- ttl: 生存时间
- time: 延迟时间

ping 不通服务器并不代表 HTTP 请求也不通，因为有的服务器的防火墙是会禁用 ICMP 协议的


traceroute
含义: 显示数据包到达目的地的路径

traceroute www.baidu.com

```
traceroute to www.baidu.com (180.101.50.242), 30 hops max, 60 byte packets
 1  LAPTOP-7CCB4DQK.mshome.net (172.19.208.1)  0.254 ms  0.233 ms  0.224 ms
 2  172.21.24.1 (172.21.24.1)  9.785 ms  9.779 ms  9.772 ms
 3  172.28.255.52 (172.28.255.52)  9.766 ms  7.236 ms  9.754 ms
 4  * * *
 5  58.213.8.1 (58.213.8.1)  12.624 ms  12.618 ms  12.613 ms
 6  58.217.231.201 (58.217.231.201)  9.715 ms 58.217.231.217 (58.217.231.217)  8.304 ms 61.155.254.37 (61.155.254.37)  8.291 ms
 7  * * *
 8  58.213.95.54 (58.213.95.54)  6.556 ms 58.213.94.222 (58.213.94.222)  7.334 ms 58.213.95.222 (58.213.95.222)  6.338 ms
 9  * * *
```

- 1: 第几跳
- 2: 路由器的 IP 地址
- 3: 三次 ICMP 数据包的延迟时间
- *: 丢包



## 日志分析

如何从日志分析 PV、UV？

很多时候，我们观察程序是否如期运行，或者是否有错误，最直接的方式就是看运行日志，当然要想从日志快速查到我们想要的信息，前提是程序打印的日志要精炼、精准。

但日志涵盖的信息远不止于此，比如对于 nginx 的 access.log 日志，我们可以根据日志信息分析用户行为。

什么用户行为呢？比如分析出哪个页面访问次数（PV）最多，访问人数（UV）最多，以及哪天访问量最多，哪个请求访问最多等等。


### 查看日志大小

`ls -lh`
- l: 列表显示
- h: 显示文件大小
- a: 显示所有文件, 包括隐藏文件

通过这个查看日志大小后

如果日志文件数据量太大, 使用cat会导致终端卡死


可以使用scp传到其他服务器上查看

### 用less,而不是cat

less不会一次性读取整个文件, 而是按需读取, 所以对于大文件来说, less更加高效

如果想要查看文件的最后几行, 可以使用tail

如果想要实时查看文件, 可以使用tail -f

### 日志分析 PV分析 Page View

用户访问一个页面就是一次 PV

对于日志文件来说, 行数可以代表 PV

Linux统计一个文件有多少行
wc -l filename

### PV分组

nginx的access.log日志文件中, 有访问时间的西欧模型/

如果要按时间分组, 可以先把时间提取出来, 然后再统计

时间在第四列, 可以使用awk提取

awk '{print $4}' access.log
输出
```
[10/Dec/2021:10:00:01
[10/Dec/2021:10:00:02
[10/Dec/2021:10:00:03
```



也可以继续使用awk的substr 函数提取时间

```
awk '{print substr($4, 2, 11)}' access.log
```

输出
```
10/Dec/2021
10/Dec/2021
10/Dec/2021
```

可以使用sort排序, 然后使用uniq统计

uniq -c是统计重复行的次数

```
awk '{print substr($4, 2, 11)}' access.log | sort | uniq -c
```

输出
```
  3 10/Dec/2021
```



使用 uniq -c 命令前，先要进行 sort 排序

uniq 的去重是基于相邻行的.

### UV分析 Unique Visitor

UV是指独立访客数，即一天内访问网站的不同IP地址的人数

如果要统计UV, 可以使用awk提取IP地址

```
awk '{print $1}' access.log
```


### 终端分析

如果要统计不同终端的访问量, 可以使用awk提取终端信息

```
awk '{print $12}' access.log
```

### TOP3请求

如果要统计访问量最多的请求, 可以使用awk提取请求信息
然后使用sort排序, 然后使用uniq统计
最后使用head -n 3查看前三个


```
awk '{print $7}' access.log | sort | uniq -c | sort -nr | head -n 3
```


