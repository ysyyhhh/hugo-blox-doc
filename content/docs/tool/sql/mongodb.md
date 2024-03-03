# mongoDB

## 常用命令

```bash
# 连接
mongosh ip[:port]/database -u username -p password

# 查看数据库
show dbs

# 切换数据库
use database

# 查看集合
show collections
# file

# 查看集合数据
db.{collection}.find()

# 按条件查看集合数据
## pid=1
db.{collection}.find({pid:1})

## 限制4条
db.{collection}.find().limit(4)

## 只显示其中一个字段
db.{collection}.find({}, {name:1})

## 统计数量
db.{collection}.find().count()

## 全部删除
db.{collection}.remove({})

## 插入或更新数据


```
