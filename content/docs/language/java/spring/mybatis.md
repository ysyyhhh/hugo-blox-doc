# MyBatis

## MyBatis 概念

MyBatis 是一个优秀的持久层框架，它对 JDBC 的操作数据库的过程进行封装，使开发者只需要关注 SQL 本身，而不需要花费精力去处理例如注册驱动、创建连接、创建 Statement、手动设置参数、结果集检索等JDBC繁杂的过程代码。

与 MyBatis Plus 的区别：
- MyBatis 是一个持久层框架，它是对 JDBC 的封装，它的目的是为了简化 JDBC 的操作。
- MyBatis Plus 是在 MyBatis 的基础上进行了功能的增强，它是一个持久层框架，它的目的是为了简化开发。
- MyBatis Plus 多了一些功能，例如：分页、逻辑删除、性能分析等。


## 语法

### #{} 与 ${} 的区别

- #{} 是预编译处理，${} 是字符串替换。
- #{} 是将传入的数据当做一个字符串，会在#{}所在的位置加一个占位符?，然后使用 PreparedStatement 的 setString() 方法来设置?的值。
- ${} 是将传入的数据直接拼接在 SQL 中，会导致 SQL 注入的问题。

## MyBatis 的执行流程

1. 加载配置文件
2. 创建 SqlSessionFactory 工厂
3. 创建 SqlSession
4. 执行 SQL
5. 关闭 SqlSession
6. 关闭 SqlSessionFactory
7. 释放资源

## xml中的标签

sql相关: insert 、 update delete、select
参数相关: parameterMap、parameterType、resultMap、resultType
其他: sql、include、trim、where、set、foreach、if、choose、when、otherwise

## Dao接口的工作原理

Dao 接口的工作原理是动态代理，MyBatis 会根据 Dao 接口的方法名和参数类型来生成一个代理对象，代理对象会调用 SqlSession 的方法来执行 SQL 语句。

Mapper接口没有实现类， 调用接口方法时，接口全限定名+方法名就是对应的SQL语句的ID，可唯一定位一个MappedStatement对象。

Dao接口里的方法可以重载，但Mybatis xml里的ID不允许重复
重载需要满足的条件：
- 仅有一个无参 和 有参
- 或者， 多个有参方法，但参数数量必须一一对应，使用相同的@Param注解

xml中id，在namespace下唯一，不同namespace下可以有相同的id

## MyBatis 的延迟加载

MyBatis 的延迟加载是指在需要使用数据时才去查询数据库，而不是在一开始就把所有数据都查询出来。

原理是（和Hibernate的延迟加载原理一致）
使用 CGLIB 创建目标对象的代理对象，当调用目标方法时，进入拦截器方法，比如调用 a.getB().getName() ，拦截器 invoke() 方法发现 a.getB() 是 null 值，那么就会单独发送事先保存好的查询关联 B 对象的 sql，把 B 查询上来，然后调用 a.setB(b)，于是 a 的对象 b 属性就有值了，接着完成 a.getB().getName() 方法的调用。这就是延迟加载的基本原理。


## 批处理

使用 BatchExecutor 批处理器，可以将多个 SQL 语句一次性发送到数据库执行，减少网络开销。

## Executor 

Executor 是 MyBatis 的执行器，它负责执行 MyBatis 的 SQL 语句，它有三种实现：
- SimpleExecutor：每执行一次 update 或 select 都会开启一个 Statement 对象，用完立刻关闭 Statement 对象。
- ReuseExecutor：执行 update 或 select 时，会创建 Statement 对象，用完后不会关闭 Statement 对象，而是放置于 Map<String, Statement> 中，供下一次使用。
- BatchExecutor：执行 update（没有 select，JDBC 批处理不支持 select），将所有 SQL 都添加到批处理中（addBatch()），等待统一执行（executeBatch()）。

如何选择 Executor：
- 默认情况下，MyBatis 使用 SimpleExecutor。
- 在 MyBatis 的配置文件中可以配置使用哪种 Executor。
- 一般情况下，如果是单线程环境，使用 SimpleExecutor 就可以了。
- 如果是多线程环境，使用 ReuseExecutor。
- 如果是批处理，使用 BatchExecutor。

## MyBatis 映射枚举类

MyBatis 3.4.5 之后，MyBatis 支持枚举类型的映射。

## MyBatis xml文件中 A include了B，B能否定义在A的后面

可以，MyBatis 会先解析所有的 sql 语句，然后再解析所有的 include 标签。

## MyBatis 的一级缓存和二级缓存

一级缓存是 SqlSession 级别的缓存，当调用 SqlSession 的修改、添加、删除、commit()、close()等方法时，就会清空一级缓存。

二级缓存是 Mapper 级别的缓存，多个 SqlSession 可以共用二级缓存，二级缓存是跨 SqlSession 的。

## MyBatis 的缓存机制

MyBatis 的缓存机制是通过 Cache 接口来实现的，MyBatis 默认使用 PerpetualCache 作为一级缓存，使用 LruCache 作为二级缓存。

## ORM

ORM（Object-Relational Mapping）对象关系映射，是一种程序设计技术，用于实现面向对象编程语言里不同类型系统的数据之间的转换。

MyBatis 是一种半自动化的 ORM 框架，它需要程序员手动编写 SQL 语句，但是不需要程序员手动处理结果集。

Hibernate 是一种全自动化的 ORM 框架，它不需要程序员手动编写 SQL 语句，也不需要程序员手动处理结果集。
