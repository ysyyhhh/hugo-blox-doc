 示例表：

![image-20230309100013301](img/Sql实例解析与连接方式/image-20230309100013301.png)



## 1.SQL实例处理：字符串

SQL不专门用于处理复杂的字符串，但内置了很多有用的字符串。

### 1.1遍历字符串

SQL没有Loop功能, 需要使用数据透视表

![image-20230227163824652](img/Sql实例解析与连接方式/image-20230227163824652.png)

循环的次数是字符串的长度, 用where来终止.



### 1.2嵌入引号

![image-20230227163859353](img/Sql实例解析与连接方式/image-20230227163859353.png)

### 1.3统计字符出现的次数

![image-20230227163927154](img/Sql实例解析与连接方式/image-20230227163927154.png)

sql server 是用len

### 1.4删除不想要的字符



![image-20230227164016283](img/Sql实例解析与连接方式/image-20230227164016283.png)

替换多个字符时可以使用: **translate**

![image-20230227164049652](img/Sql实例解析与连接方式/image-20230227164049652.png)

先全部一致替换为a,再把a给删除.

但mysql中没有translate.

阿里的OceanBase同时支持replace和translate

### 1.5判断是否只含有字母和数字



![image-20230227164123913](img/Sql实例解析与连接方式/image-20230227164123913.png)

Mysql可以直接使用正则表达式. [] 内表示范围 ^ 表示否定

OceanBase 的0 1相反

![image-20230309101159648](img/Sql实例解析与连接方式/image-20230309101159648.png)



思考题

![image-20230227164306073](img/Sql实例解析与连接方式/image-20230227164306073.png)

​	





## 2.SQL实例解析 数值处理

虽然SQL不容易处理，但硬要在SQL中完成比如字符串，比如日期，比如今天的数值计算。

数值处理在数据库完成，可以减少数据库和服务器的交互。

能在数据库中，写个**完整功能的SQL**，让查询优化器统一优化，一般来说对整个系统的吞吐量会有非常大的提升.



### 2.1计算平均值

空值默认是忽略

![image-20230227164534143](img/Sql实例解析与连接方式/image-20230227164534143.png)

**coalesce 空值设置为0**

当使用聚合函数时通常要考虑空值的处理.

![image-20230227164603887](img/Sql实例解析与连接方式/image-20230227164603887.png)

不能把group by 子句中没有的列放到select语句中.

### 2.2查找最大值和最小值

空值没有影响.

![image-20230227164620369](img/Sql实例解析与连接方式/image-20230227164620369.png)

### 2.3求和

![image-20230227164639158](img/Sql实例解析与连接方式/image-20230227164639158.png)

### 2.4计算行数

![image-20230227164719491](img/Sql实例解析与连接方式/image-20230227164719491.png)

**count(*)计算了空值.**

**针对某一列时会跳过空值**



### 2.5累计求和 Running Total

![image-20230227164847493](img/Sql实例解析与连接方式/image-20230227164847493.png)

Sum( ) over ()

over 中的 order by 需要具有唯一性.

否则,  WARD 会和 MARTIN一样是5350

即建立**唯一的排他序列得到正确的累加值**.

在以前的mysql不支持窗口函数,所以要使用标量子查询.



### 2.6计算众数

oracle 使用 max + keep

如果max相同,则按照keep中的排序规则保留其最大的.

keep从右向左执行, 先对每一个cnt降序排序,然后执行rank函数,保留rank1的值.

![image-20230227164934043](img/Sql实例解析与连接方式/image-20230227164934043.png)

mysql只能用通用做法.group by + having





思考题:

累计乘法和累计减法





## 3.SQL实例分析 日期处理



### 3.1日期加减法

Oracle中，对天数来说，对天数来说可以直接加减，如果要加减若干月或者年，需要用一个函数，add months.

MySQL日期加减法类似，使用**INTERVAL关键字**指定要加上或者减去时间
的单位，不必使用单引号。
第二种方法: 使用date add函数，一样的作用。

OceanBase的add和mysql一模一样

![image-20230309103225068](img/Sql实例解析与连接方式/image-20230309103225068.png)



### 3.2计算两个日期之间的天数

![image-20230227165217187](img/Sql实例解析与连接方式/image-20230227165217187.png)

mysql 和 OceanBase datediff(较晚的日期,较早的日期)

sql server 是datediff(较早的,较晚的)

### 3.3两个日期的工作日天数

![image-20230227165324649](img/Sql实例解析与连接方式/image-20230227165324649.png)

这样统计天数就变成了计算行数的问题.



![image-20230309103757837](img/Sql实例解析与连接方式/image-20230309103757837.png)

1.计算出开始日期和结束日期之间相隔多少天。 x视图

2.排除掉周末，统计有多少个工作日，计算满足条件的记录。

Oracle 和 mysql的差异是函数使用的不同.



### 3.4判断闰年

判断闰年的最简单方式

检查2月份最后一天，如
果是29号，就是闰年;如
果是28号，就不是闰年;
如果既不是28号，也不是
29号，程序写错。

orcale 有trunc函数找到**当前年份的第一天**

![image-20230309104059402](img/Sql实例解析与连接方式/image-20230309104059402.png)

先算出当前日期是当前年份的第几天, 找到当前年的第一天.

![image-20230227165617940](img/Sql实例解析与连接方式/image-20230227165617940.png)

### 3.5识别重叠的日期区间

![image-20230227165658575](img/Sql实例解析与连接方式/image-20230227165658575.png)

自连接方法, 复制出另一份表,然后找到重叠的项目

窗口比自联结快,但需要限定项目的个数.

![image-20230227165731407](img/Sql实例解析与连接方式/image-20230227165731407.png)



思考题: 当前月份的第一个和最后一个星期一





## 4.常见的SQL连接模式

查询有时候并不只需要等值连接.

4.1叠加行集(Union &Union all)

4.2查找只存在于一张表的数据 (差)

4.3从一个表检索另一个不相关的行(外连接

4.4从多个表中返回缺失值 (全外连接)

4.5连接与聚合函数的使用

### 4.1叠加行集(Union & Union all)

使用连接的情况，就是想返回保存至多个表中的数据
理论上需要将一个结果集叠加到另一个之上，甚至这些表**可以没有相同的键**，有一个前提条件是，它们**列的数据类型必须相同**。

![image-20230227165935617](img/Sql实例解析与连接方式/image-20230227165935617.png)

Union all是将多个表中的行并入结果集. 列的数目和类型必须匹配,名字可以不一样. Union all 会包括重复项, union会去除重复项.

![image-20230227170009502](img/Sql实例解析与连接方式/image-20230227170009502.png)

union的问题 : **有排序操作**以删除重复项,慎用.

排序是非关系操作,大数据量的排序对性能是一个灾难.

### 4.2查找只存在于一张表的数据(差)

使用差函数, 但不同数据库的差函数关键字不一样.

minus限制条件, 列必须相同个数和数据类型,且不返回重复值. 空值不问产生任何问题.

except 对结果进行去重.

![image-20230227170147073](img/Sql实例解析与连接方式/image-20230227170147073.png)

使用not in时用空值的问题,一遍要加上exists 或 not exists

### 4.3从一个表检索另一个不相关的行(外连接)

![image-20230227170229988](img/Sql实例解析与连接方式/image-20230227170229988.png)

outer可写可不写

### 4.4从多个表中返回每个表的缺失值(全外连接)

![image-20230227170250386](img/Sql实例解析与连接方式/image-20230227170250386.png)

### 4.5连接与聚合函数的使用

确保表之间的连接查询不会干扰到聚合操作.

左边是员工奖金表,

![image-20230227170339432](img/Sql实例解析与连接方式/image-20230227170339432.png)

奖金总额正确,但工资总额是错的.

![image-20230309105955183](img/Sql实例解析与连接方式/image-20230309105955183.png)

是因为连接查询导致某行的工资出现两次.

解决方法, 使用distinct.

![image-20230227170437389](img/Sql实例解析与连接方式/image-20230227170437389.png)



如果表中, 部门编号为10的人只有部分人有奖金.此时计算总额会少算.

![image-20230227170454013](img/Sql实例解析与连接方式/image-20230227170454013.png)



提示: 需要选择连接方式.用**外连接把员工全包括**.



