# Redis应用



## Redis应用

### 分布式锁

分布式锁实现：

原始方式：setnx key true（死锁）/set key true ex 30 nx（锁误删）-> 锁重入问题。


Redisson 框架实现方式：Redis + Lua 实现。


### 分布式session登录



## Redis集群：


22、Redis集群的原理是什么？

Redis集群的原理是将数据分散到多个节点上存储，通过主从复制和哨兵机制保证数据的可用性和一致性。

23、Redis集群会导致整个集群不可用的情况有哪些？

Redis集群会导致整个集群不可用的情况包括节点故障、网络分区等。

24、Redis支持的Java客户端有哪些？

Redis支持的Java客户端包括Jedis、Lettuce、Redisson等，官方推荐使用Lettuce。

25、Jedis与Redisson对比的优缺点有哪些？

Jedis与Redisson对比的优缺点包括性能、功能、易用性等方面。

26、Redis的密码可以通过哪些方式设置和验证？

Redis的密码可以通过配置文件设置，验证密码可以使用AUTH命令。

27、Redis哈希槽的概念是什么？

Redis哈希槽的概念是将所有的key分散到不同的槽中存储，每个槽对应一个节点，通过哈希算法计算key所在的槽。


Redis为何用哈希槽而不用一致性哈希？

[得物面试：为啥Redis用哈希槽，不用一致性哈希？](https://mp.weixin.qq.com/s/Q68UN34-BqxyQFtkJL98lg)



28、Redis集群的主从复制模型是什么？

Redis集群的主从复制模型是将数据分散到多个节点上存储，每个节点都可以作为主节点或从节点，通过主从复制保证数据的可用性和一致性。

29、Redis集群不会有写操作丢失吗？

Redis集群不会有写操作丢失，因为它采用了主从复制和哨兵机制，可以保证数据的可用性和一致性。

30、Redis集群之间如何进行数据复制和故障转移？

Redis集群之间通过主从复制和哨兵机制进行数据复制和故障转移。

31、Redis集群最大节点个数是多少？

Redis集群最大节点个数是16384。

32、Redis集群可以选择不同的数据库吗？

Redis集群可以选择不同的数据库，通过SELECT命令进行切换。

33、如何测试Redis的连通性？

可以使用PING命令测试Redis的连通性。



