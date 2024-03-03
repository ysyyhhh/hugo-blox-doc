
# 利于部署的开发规范手册

本规范用于在开发过程中，使得项目能够更好的部署，更好的维护。

使用时间: 当项目开始开发时，就应该遵守本规范。

核心要点:

- 管理依赖库
- 使用docker
- 端口、ip地址等使用环境变量
- 路径不能写死！尤其是绝对路径和根目录等，需要放在环境变量中！！

## 后端

### python项目

python常见的依赖库管理有:

- poetry
- requirements.txt
- pipenv

#### poetry

初始化

```bash
poetry init
```

安装依赖

```bash
poetry install
```

使用poetry运行项目

```bash
poetry run python main.py
```

添加依赖

```bash
poetry add <package>
```

dockerfile示例

```dockerfile
FROM python:3.8.5-slim-buster
WORKDIR /app

# 拷贝依赖文件
COPY pyproject.toml poetry.lock ./

# 设置国内源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装poetry
RUN pip install poetry

# 安装依赖
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# tips: 先只拷贝依赖文件，再安装依赖，可以利用docker的缓存机制，加快构建速度. 
# (防止只是项目文件改变，而依赖文件没有改变，导致重新安装依赖)

# 拷贝项目文件
COPY . .

# 运行项目
CMD ["poetry", "run", "python", "main.py"]
```

#### requirements.txt

导出依赖

```bash
pip freeze > requirements.txt
```

安装依赖

```bash
pip install -r requirements.txt
```

dockerfile示例

```dockerfile
FROM python:3.8.5-slim-buster
WORKDIR /app

# 拷贝依赖文件
COPY requirements.txt ./

# 设置国内源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装依赖
RUN pip install -r requirements.txt

# 拷贝项目文件
COPY . .

# 运行项目
CMD ["python", "main.py"]
```

#### pipenv

初始化

```bash
pipenv --python 3.8
```

安装依赖

```bash
pipenv install
```

使用pipenv运行项目

```bash
pipenv run python main.py
```

添加依赖

```bash
pipenv install <package>
```

dockerfile示例

```dockerfile
FROM python:3.8.5-slim-buster
WORKDIR /app

# 设置国内源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 拷贝依赖文件
COPY Pipfile Pipfile.lock ./

# 安装依赖
RUN pip install pipenv \
    && pipenv install --system --deploy --ignore-pipfile

# 拷贝项目文件
COPY . .

# 运行项目
CMD ["pipenv", "run", "python", "main.py"]
```

### SpringBoot项目

[参考](https://developer.aliyun.com/article/65274)
这里都以maven作为依赖管理工具。

主要保留pom.xml文件

dockerfile示例

```dockerfile
# 第一阶段: 构建jar包
FROM maven:3.6.3-jdk-8-slim AS build

WORKDIR /app

COPY pom.xml ./

# 设置国内源
RUN mvn -B -e -C -T 1C org.apache.maven.plugins:maven-dependency-plugin:3.1.2:go-offline

# 拷贝项目文件
COPY . .

# 构建jar包
RUN mvn clean install -DskipTests


# 第二阶段: 运行jar包
FROM openjdk:8-jdk-alpine

WORKDIR /app

# 拷贝第一阶段构建的jar包
COPY --from=build /app/target/demo-0.0.1-SNAPSHOT.jar ./

# 运行项目
CMD ["java", "-jar", "target/demo-0.0.1-SNAPSHOT.jar"]
```

### 数据库

通常后端要连接数据库，这里只是简单的示例，实际项目中应该使用[docker-compose](#封装整个项目)来管理多个容器。

dockerfile示例

```dockerfile
FROM mysql:8.0.22

# 设置时区
ENV TZ=Asia/Shanghai

# 设置root密码
ENV MYSQL_ROOT_PASSWORD=123456

# 设置数据库名
ENV MYSQL_DATABASE=test

# 设置用户名
ENV MYSQL_USER=test

# 设置密码
ENV MYSQL_PASSWORD=123456

# 设置端口
EXPOSE 3306
```

单独运行mysql

```bash
docker run -d -p 3306:3306 --name mysql -v /path/to/mysql/data:/var/lib/mysql mysql:8.0.22
```

## 前端

前端使用npm作为依赖管理工具, 使用nginx作为web服务器。

必要的文件:

- package.json # 依赖文件
- package-lock.json # 锁定依赖版本
- nginx.conf # nginx配置文件
- dockerfile

### npm

npm初始化

```bash
npm init
```

安装依赖

```bash
npm install
```

添加依赖(默认添加到dependencies, 添加到devDependencies需要加上--save-dev参数(或者-D)

```bash
npm install <package>
```

### nginx

nginx.conf示例

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html index.htm;
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### docker

docker [使用多阶段构建](https://cloud.tencent.com/developer/article/2246201)

dockerfile示例

```dockerfile

# 第一阶段: 构建项目
FROM node:lts-alpine as build

WORKDIR /app

# 拷贝依赖文件
COPY package.json package-lock.json ./

# 安装依赖
RUN npm install

# 拷贝项目文件
COPY . .

# 构建项目
RUN npm run build

# 第一段构建完成, 获得/app/build文件夹

# 使用nginx作为web服务器
FROM nginx:1.19.4-alpine

# 拷贝nginx配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 拷贝第一阶段构建的项目文件
COPY --from=build /app/build /usr/share/nginx/html

# 运行nginx
CMD ["nginx", "-g", "daemon off;"]
```

## 项目部署 TODO

### 封装整个项目(单个项目时)

经过上面的步骤已经将前后端 数据库封装到docker中了,但每次启动项目都需要手动启动三个容器, 这里使用docker-compose来管理多个容器。

docker-compose.yml示例

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0.22
    environment:
      TZ: Asia/Shanghai
      MYSQL_ROOT_PASSWORD: 123456
      MYSQL_DATABASE: test
      MYSQL_USER: test
      MYSQL_PASSWORD: 123456
    ports:
      - 3306:3306
    volumes:
      - ./mysql/data:/var/lib/mysql

  backend:
    build: ./backend
    ports:
      - 8080:8080
    depends_on:
      - mysql

  frontend:
    build: ./frontend
    ports:
      - 80:80
    depends_on:
      - backend
```

### 整个项目作为k8s的一个服务(多个项目时)

上面是使用docker-compose来管理 一个项目的多个容器.

但如果有多个项目, 每个项目都有多个容器, 这时候就需要使用k8s来管理了.

我们把一个项目(多个容器)作为一个k8s的一个服务.

k8s的配置文件示例

```yaml
apiVersion: v1
kind: Service
metadata:
  name: test
  labels:
    app: test
spec:
    ports:
        - port: 80
        targetPort: 80
        protocol: TCP
    selector:
        app: test
    type: NodePort
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test
  labels:
    app: test
spec:
    replicas: 1
    selector:
        matchLabels:
        app: test
    template:
        metadata:
        labels:
            app: test
        spec:
        containers:
            - name: mysql
            image: mysql:8.0.22
            env:
                - name: TZ
                value: Asia/Shanghai
                - name: MYSQL_ROOT_PASSWORD
                value: 123456
                - name: MYSQL_DATABASE
                value: test
                - name: MYSQL_USER
                value: test
                - name: MYSQL_PASSWORD
                value: 123456
            ports:
                - containerPort: 3306
            volumeMounts:
                - name: mysql-data
                mountPath: /var/lib/mysql
            - name: backend
            image: backend:latest
            ports:
                - containerPort: 8080
            env:
                - name: MYSQL_HOST
                value: mysql
                - name: MYSQL_PORT
                value: "3306"
                - name: MYSQL_DATABASE
                value: test
                - name: MYSQL_USER
                value: test
                - name: MYSQL_PASSWORD
                value: 123456
            - name: frontend
            image: frontend:latest
            ports:
                - containerPort: 80
        volumes:
            - name: mysql-data
            hostPath:
                path: /path/to/mysql/data
```
