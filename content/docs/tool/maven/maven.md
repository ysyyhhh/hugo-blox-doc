# maven

## 打包

```shell
mvn clean package -Dmaven.test.skip=true
```

## 常见问题

### 找不到主类

```shell
Error: Could not find or load main class com.xxx.xxx.xxx
Caused by: java.lang.ClassNotFoundException: com.xxx.xxx.xxx
```

解决方法：在pom.xml中添加如下配置

```xml

```
