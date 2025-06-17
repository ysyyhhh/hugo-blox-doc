# MySQL

## MySql常用命令

查看所有用户和host

```
select user,host from mysql.user;
```

##### 修改用户

修改密码
```
alter user 'root'@'localhost' identified with mysql_native_password by '123456';

alter user 'digitalmap'@'%' identified with mysql_native_password by 'digitalmap';

```

修改用户host

```sql
update mysql.user set host = '%' where user = 'root
```

##### 刷新权限

```
flush privileges;
```

##### 添加一个远程用户

```
create user 'remote'@'%' identified by 'password'
create user 'digitalmap'@'localhost' identified by 'digitalmap_root'


GRANT all ON *.* TO 'remote'@'%';

GRANT all ON digitalmap.* TO 'digitalmap'@'%';

grant all privileges on *.* to 'remote'@'%' with grant option;

grant all privileges on digitalmap.* to 'digitalmap'@'%' with grant option;

*.*所有数据库下的所有表
```

##### 删除用户

```
drop user 'remote'@'%';
```

##### 创建数据库并设定中文编码

```
CREATE DATABASE `db_name` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
```

##### 登录格式

```
mysql -h #{数据库IP} -P 3306 -u #{用户名} -p -D #{数据库名}
```

##### 自增id 不连续时

```
SET @auto_id = 0;
UPDATE 表名 SET 自增字段名 = (@auto_id := @auto_id + 1);
ALTER TABLE 表名 AUTO_INCREMENT = 1;

```

#### 文件

读取sql
```
source
```

导出为sql
```
mysqldump -u root -p 数据库名 > 文件名.sql
```


#### 数据库

设置数据库的字符集

```sql
alter database 数据库名 character set utf8;
```

#### 表

```sql
# 添加一列
alter table 表名 add column 列名 类型;


```



#### 数据

```sql

# 插入数据
insert into 表名 (字段1,字段2) values (值1,值2);


# 更新数据
update 表名 set 字段1=值1,字段2=值2 where 条件;

# 删除数据
delete from 表名 where 条件;
```
### 时间处理

Date



### 条件语句

CASE

强制转换

CAST


## 常用SQL


### augmenttask表

```
CREATE TABLE `augmenttask` (
  `originSetId` varchar(255) DEFAULT NULL,
  `augSetId` varchar(255) DEFAULT NULL,
  `weatherType` int(11) DEFAULT NULL,
  `weatherIntensity` float DEFAULT NULL,
  `parameter` float DEFAULT NULL,
  `beginTime` datetime DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `taskname` varchar(255) DEFAULT NULL,
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `road` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;

```

```
UPDATE augmenttask
SET taskname = CONCAT(
  SUBSTRING_INDEX(taskname, '_', 1), '_',
  weatherType, '_',
  weatherIntensity, '_',
  parameter, '_',
  FLOOR(RAND() * 10)
);

UPDATE testtask t
JOIN augmenttask a ON t.augTaskId = a.ID
SET t.name = a.taskname;

```

```
SET @start_date = UNIX_TIMESTAMP('2021-01-01 00:00:00');
SET @end_date = UNIX_TIMESTAMP('2025-05-01 23:59:59');

UPDATE augmenttask
SET beginTime = FROM_UNIXTIME(
  FLOOR(@start_date + RAND() * (@end_date - @start_date))
);
```

按照beginTime顺序重新赋值ID

```sql

```

```sql
-- 关闭外键检查，防止约束冲突
SET FOREIGN_KEY_CHECKS=0;

-- 1. 建临时表，结构同原表，去掉AUTO_INCREMENT
DROP TABLE IF EXISTS augmenttask_tmp;

CREATE TABLE augmenttask_tmp LIKE augmenttask;

ALTER TABLE augmenttask_tmp MODIFY COLUMN ID INT NOT NULL;

-- 2. 按beginTime排序，从1开始赋值ID插入临时表
SET @rownum := 0;

INSERT INTO augmenttask_tmp (originSetId, augSetId, weatherType, weatherIntensity, parameter, beginTime, status, taskname, ID, road)
SELECT originSetId, augSetId, weatherType, weatherIntensity, parameter, beginTime, status, taskname, 
       (@rownum := @rownum + 1) AS new_id,
       road
FROM augmenttask
ORDER BY beginTime ASC;

-- 3. 清空原表
TRUNCATE TABLE augmenttask;

-- 4. 导回数据
INSERT INTO augmenttask SELECT * FROM augmenttask_tmp;

-- 5. 开启外键检查
SET FOREIGN_KEY_CHECKS=1;

-- 可选：删除临时表
DROP TABLE IF EXISTS augmenttask_tmp;
```


### testtask表

同步 testtask.name 和 augmenttask.taskname

```sql
UPDATE testtask t
JOIN augmenttask a ON t.augTaskId = a.ID
SET t.name = a.taskname;
```


同步 testtask.createTime 为 augmenttask.beginTime + 随机0~3分钟（3分钟以内）
```sql
UPDATE testtask t
JOIN augmenttask a ON t.augTaskId = a.ID
SET t.createTime = DATE_ADD(a.beginTime, INTERVAL FLOOR(RAND() * 180) SECOND);
```

按 createTime 升序，重新给 testtask.ID 赋顺序号（MySQL 5.7 变量法）
```sql
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS testtask_tmp;
CREATE TABLE testtask_tmp LIKE testtask;
ALTER TABLE testtask_tmp MODIFY COLUMN ID INT NOT NULL;

SET @rownum := 0;
INSERT INTO testtask_tmp (ID, testSetId, errorSetId, augTaskId, createTime, status, name)
SELECT (@rownum := @rownum + 1) AS new_id, testSetId, errorSetId, augTaskId, createTime, status, name
FROM testtask
ORDER BY createTime ASC;

TRUNCATE TABLE testtask;

INSERT INTO testtask SELECT * FROM testtask_tmp;

SELECT MAX(ID) + 1 INTO @next_id FROM testtask;
SET @sql = CONCAT('ALTER TABLE testtask AUTO_INCREMENT = ', @next_id);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

DROP TABLE testtask_tmp;

SET FOREIGN_KEY_CHECKS=1;
```

### report表

保持 report.name 和 testtask.name 一致
```sql
UPDATE report r
JOIN testtask t ON r.testId = t.ID
SET r.name = t.name;
```



```sql
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS report_tmp;
CREATE TABLE report_tmp LIKE report;
ALTER TABLE report_tmp MODIFY COLUMN ID INT NOT NULL;

INSERT INTO report_tmp (ID, name, image, alarm, miss, yaw, bev, augId, testId, testInfo)
SELECT t.ID, t.name, r.image, r.alarm, r.miss, r.yaw, r.bev, r.augId, r.testId, r.testInfo
FROM report r
JOIN testtask t ON r.testId = t.ID
ORDER BY t.ID ASC;

TRUNCATE TABLE report;

INSERT INTO report SELECT * FROM report_tmp;

SELECT MAX(ID) + 1 INTO @next_id FROM report;
SET @sql = CONCAT('ALTER TABLE report AUTO_INCREMENT = ', @next_id);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

DROP TABLE report_tmp;

SET FOREIGN_KEY_CHECKS=1;
```




```sql
-- 1. 备用表（建议做好数据备用）
-- mysqldump -u 用户名 -p 数据库名 model > modelbackup.sql
use test;
-- 2. 新建一张表，结构完全与model表一致，但是id从1开始自动增长
CREATE TABLE `model_new` LIKE `model`;

-- 3. 依序插入数据到新表中（按现有id从小到大）
-- 这样插入时id会自动从1开始依次增加
INSERT INTO `model_new` (`name`, `file_name`, `size`, `create_date`, `type`, `desc`) 
SELECT `name`, `file_name`, `size`, `create_date`, `type`, `desc`
FROM `model`
ORDER BY `id`;

-- 4. 检查无误后：
-- 你可以用以下语句进行替换：
RENAME TABLE `model` TO `model_old`, `model_new` TO `model`;

-- 若无需要，你可以删除备用表：
-- DROP TABLE `model_old`;

```
