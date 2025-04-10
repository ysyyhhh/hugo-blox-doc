
# TCP


控制位:
ACK：该位为 1 时，「确认应答」的字段变为有效，TCP 规定除了最初建立连接时的 SYN 包之外该位必须设置为 1 。
RST：该位为 1 时，表示 TCP 连接中出现异常必须强制断开连接。
SYN：该位为 1 时，表示希望建立连接，并在其「序列号」的字段进行序列号初始值的设定。
FIN：该位为 1 时，表示今后不会再有数据发送，希望断开连接。当通信结束希望断开连接时，通信双方的主机之间就可以相互交换 FIN 位为 1 的 TCP 段。


netstat -napt


## 三次握手

![](img/TCP/三次握手.png)

- 一开始，客户端和服务端都处于 CLOSE 状态。先是服务端主动监听某个端口，处于 LISTEN 状态
- 客户端会随机初始化序号（client_isn），将此序号置于 TCP 首部的「序号」字段中，同时把 SYN 标志位置为 1，表示 SYN 报文。接着把第一个 SYN 报文发送给服务端，表示向服务端发起连接，该报文不包含应用层数据，之后客户端处于 SYN-SENT 状态。
- 服务端收到客户端的 SYN 报文后，首先服务端也随机初始化自己的序号（server_isn），将此序号填入 TCP 首部的「序号」字段中，其次把 TCP 首部的「确认应答号」字段填入 client_isn + 1, 接着把 SYN 和 ACK 标志位置为 1。最后把该报文发给客户端，该报文也不包含应用层数据，之后服务端处于 SYN-RCVD 状态。
- 客户端收到服务端报文后，还要向服务端回应最后一个应答报文，首先该应答报文 TCP 首部 ACK 标志位置为 1 ，其次「确认应答号」字段填入 server_isn + 1 ，最后把报文发送给服务端，这次报文可以携带客户到服务端的数据，之后客户端处于 ESTABLISHED 状态。
- 服务端收到客户端的应答报文后，也进入 ESTABLISHED 状态。

第三次握手是可以携带数据的，前两次握手是不可以携带数据的，这也是面试常问的题。

## 四次挥手

- 客户端打算关闭连接，此时会发送一个 TCP 首部 FIN 标志位被置为 1 的报文，也即 FIN 报文，之后客户端进入 FIN_WAIT_1 状态。
- 服务端收到该报文后，就向客户端发送 ACK 应答报文，接着服务端进入 CLOSE_WAIT 状态。
- 客户端收到服务端的 ACK 应答报文后，之后进入 FIN_WAIT_2 状态。

- 等待服务端处理完数据后，也向客户端发送 FIN 报文，之后服务端进入 LAST_ACK 状态。
- 客户端收到服务端的 FIN 报文后，回一个 ACK 应答报文，之后进入 TIME_WAIT 状态
- 服务端收到了 ACK 应答报文后，就进入了 CLOSE 状态，至此服务端已经完成连接的关闭。
- 客户端在经过 2MSL 一段时间后，自动进入 CLOSE 状态，至此客户端也完成连接的关闭。


## TCP和HTTP的keep-alive区别

### TCP的keep-alive

TCP 的 Keepalive 是 **TCP 的保活机制**，检测的是对端主机是否存活（而不是进程）

原理：

![](img/TCP/TCP保活机制.png)

1. 如果两端的 TCP 连接一直没有数据交互，达到了触发 TCP 保活机制的条件，那么内核里的 TCP 协议栈就会发送探测报文。
2. 如果对端程序是正常工作的。当 TCP 保活的探测报文发送给对端, 对端会正常响应，这样 TCP 保活时间会被重置，等待下一个 TCP 保活时间的到来。
3. 如果对端主机宕机（注意**不是进程崩溃，进程崩溃后操作系统在回收进程资源的时候，会发送 FIN 报文**，而主机宕机则是无法感知的，所以需要 TCP 保活机制来探测对方是不是发生了主机宕机）。或对端由于其他原因导致报文不可达。当 TCP 保活的探测报文发送给对端后没有响应，连续几次，**达到保活探测次数**后，TCP 会报告该 TCP 连接已经死亡。

TCP 保活机制可以在双方没有数据交互的情况，通过探测报文，来确定对方的 TCP 连接是否存活，**这个工作是在内核完成的**。

默认情况：
默认情况TCP 保活机制是关闭的，应用程序需要通过设置需要通过 socket 接口设置 SO_KEEPALIVE 选项才能够生效。

### HTTP的keep-alive

![](img/TCP/HTTP长连接.png)

HTTP 的 Keepalive 是 **HTTP 长连接**，目的是在一次TCP连接中可以发送多个HTTP请求，减少建立和关闭连接的开销。


在 HTTP 1.0 中默认是关闭的，如果浏览器要开启 Keep-Alive，它必须在请求的包头中添加：`Connection: Keep-Alive`。

在 HTTP 1.1 开始, 默认是开启的，如果要关闭 Keep-Alive，可以在请求的包头中添加：`Connection: close`。

HTTP长连接支持了HTTP流水线,但同时也带来了队头阻塞问题。

同时为了避免TCP连接一直保持，web 服务软件一般都会提供 keepalive_timeout 参数，用来指定 HTTP 长连接的超时时间。

#### HTTP 流水线

![](img/TCP/HTTP流水线.png)

HTTP 流水线: 客户端可以先一次性发送多个请求，而在发送过程中不需先等待服务器的回应，可以减少整体的响应时间。

- 服务器还是按照顺序响应, 即先响应第一个请求，再响应第二个请求，以此类推。

- 而且要等服务器响应完客户端**第一批发送的请求**后，客户端**才能发出下一批的请求**

于是就有了队头阻塞问题，即前面的请求处理时间过长，导致后面的请求被阻塞。

#### 队头阻塞

实际上队头阻塞问题由两种,一种是TCP本身的队头阻塞，一种是HTTP的队头阻塞。

- TCP本身的队头阻塞：TCP是一个面向字节流的协议，如果一个数据包丢失，那么后面的数据包都会被阻塞，直到丢失的数据包被重传成功。
- HTTP/1.x 的队头阻塞: 当顺序发送的请求序列中的一个请求因为某种原因被阻塞时，在后面排队的所有请求也一并被阻塞
- HTTP/2 的队头阻塞: HTTP/2 通过多路复用解决了HTTP/1.x的队头阻塞问题，可以同时发送多个请求，而且不会被阻塞。
- HTTP/3 的队头阻塞: HTTP/3 使用了 UDP + QUIC 协议，解决了TCP队头阻塞问题。



## 面向字节流的协议



QUIC


