# MySQL

39.Mysql的存储引擎有什么
40.Innodb的特性
41.Mysql有几种锁
42.怎么避免锁全表
43.Insert into和replace into有什么区别
44.Union和union all的区别
45.常用的几种连接
46.Join和leftjoin什么区别


MySQL


## 引擎

### **InnoDB和MyISAM的区别**

- **事务支持**：InnoDB支持事务，MyISAM不支持事务
- **外键支持**：InnoDB支持外键，MyISAM不支持外键
- **锁级别**：InnoDB支持行级锁，MyISAM支持表级锁
- **MVCC**：InnoDB支持MVCC，MyISAM不支持MVCC
- **表的具体行数**：InnoDB不保存表的具体行数，执行select count(*) from table时需要全表扫描。MyISAM保存表的具体行数，执行上述语句时直接读取保存的行数。
- **异常奔溃后的恢复**：InnoDB是崩溃后完全恢复（依赖redo log），MyISAM是损坏后无法恢复
- 索引实现不一样：InnoDB是聚集索引，MyISAM是非聚集索引


## 读写分离(主从表)

读写分离主要是为了将对数据库的读写操作分散到不同的数据库节点上。

一般情况下，我们都会选择一主多从，也就是一台主数据库负责写，其他的从数据库负责读。主库和从库之间会进行数据同步，以保证从库中数据的准确性。

### 如何实现读写分离

- 多台数据库, 1台主库, 多台从库
- 保证主从库的数据一致性 -- 主从复制
- 将写操作发送到主库，读操作发送到从库


#### 代理方式

在应用和数据中加一个代理层,代理层来分离读写请求.

类似的中间件有: 
- MySQL Pouter(官方)
- Mysql Proxy
- MaxScale
- MyCat

#### 组件方式

引入第三方组件来实现读写分离

如sharding-jdbc

### 主从复制的原理

基于二进制日志的复制  (binlog)

binlog记录了数据库执行的所有DDL和DML语句

过程:
- 主库将数据库变化写入binlog
- 从库连接到主库
- 创建一个IO线程请求主库的binlog
- 主库创建一个binlog dump线程,将binlog的内容发送给从库
- 从库的IO线程接收到binlog后,写入relay log
- 从库的SQL线程读取relay log,并执行其中的内容

应用:
- 阿里开源的 canal
- 分布式缓存组件 Redis 也是通过主从复制实现的读写分离。

### 如何避免主从延迟

问题: 写完主库之后，主库的数据同步到从库是需要时间的，这个时间差就导致了主库和从库的数据不一致性问题

1. 强制把读请求给主库
2. 延迟读取, 等待从库同步完成后再读取

## 日志类型

### 重做日志（redo log）

作用：保证事务的持久性

内容：记录数据页的物理修改，而不是逻辑修改

什么时候产生

事务开始之后就产生redo log，redo log的落盘并不是随着事务的提交才写入的，而是在事务的执行过程中，便开始写入redo log文件中。

什么时候释放

当对应事务的脏页写入到磁盘之后，redo log的使命也就完成了，重做日志占用的空间就可以重用（被覆盖）。

### 回滚日志（undo log）

作用：保证事务的原子性

内容：记录数据页的逻辑修改

在执行undo操作时，会将undo log中的数据写入到数据页中

事务开始之前就产生undo log

当事务提交之后，undo log并不能立马被删除，

而是放入待清理的链表，由purge线程判断是否由其他事务在使用undo段中表的上一个事务之前的版本信息，决定是否可以清理undo log的日志空间。


### 二进制日志（binlog）

作用： 用于主从复制

内容：包括执行了的sql语句和反向的sql语句



其他： 错误日志（errorlog）、慢查询日志（slow query log）、一般查询日志（general log），中继日志（relay log）



## 分布式场景


### 分布式场景中如何保证主键的唯一性

- 使用全局唯一ID
- UUID 不依赖中心认证即可自动生成全局唯一ID。

32个十六进制数组成的字符串，且分隔为五个部分，如：
467e8542-2275-4163-95d6-7adc205580a9
各部分的数字个数为：8-4-4-4-12

#### 生成方式

- 基于时间戳
- 基于随机数
- 基于名字空间



#### 使用UUID的好处

- 生成简单，不依赖数据库
- 生成速度快

#### 使用UUID的坏处

- 无序性，不适合作为主键
- 占用空间大，16个字节

## SQL语法

### 修改表结构

增加一列
```sql
ALTER TABLE table_name ADD column_name column_definition;
```

修改某一列的类型
```sql
ALTER TABLE table_name MODIFY column_name column_type;
```
