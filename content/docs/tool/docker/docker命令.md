# Docker命令

## 安装docker

```shell
sudo apt -y update

sudo apt -y upgrade

sudo apt -y full-upgrade

# 安装依赖
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release

# 添加官方GPG密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

#添加仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 更新apt
sudo apt -y update

# 安装docker
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 安装docker-compose

sudo apt install -y docker-compose


```

centos 6.9 下安装docker

https://medium.com/@zihansyu/centos-6-x-%E5%AE%89%E8%A3%9Ddocker-9e61354fd2ae

https://blog.csdn.net/kinginblue/article/details/73527832

## 1.镜像相关

```shell
# 构建镜像
docker build [选项] <上下文路径/URL/->
# 选项: -f, --file=""  # 指定要使用的Dockerfile路径（默认为./Dockerfile）
#       --force-rm=false  # 在构建过程中删除中间容器
#       --no-cache=false  # 始终使用缓存
#       --pull=false  # 在构建过程中尝试去更新镜像的新版本
#       --quiet=false  # 安静模式，成功后只输出镜像ID
#       --rm=true  # 在构建成功后删除临时容器
#       -t, --tag=[]  # 镜像名称（默认值：<上下文路径>的基本名称）
#       --ulimit=[]  # Ulimit配置

# 拉取镜像
docker pull [选项] [Docker Registry 地址[:端口号]/]仓库名[:标签]

# 查看镜像
docker images [选项] [仓库名]

# 删除镜像
docker rmi [选项] <镜像1> [<镜像2> ...]

# 查看镜像历史
docker history [选项] <镜像名>

# 查看镜像详细信息
docker inspect [选项] <镜像名>
```

## 2.容器相关

```shell
# 创建容器
docker run [选项] <镜像名> [命令]
#eg: docker run -d -p 8080:8080 --name tomcat tomcat:8.5.51
#选项
# -d 后台运行容器，并返回容器ID
# -i 以交互模式运行容器，通常与 -t 同时使用
# -t 为容器重新分配一个伪输入终端，通常与 -i 同时使用
# -P 随机端口映射
# -p 指定端口映射，格式为：主机(宿主)端口:容器端口
# --name 指定容器名字
# --link 连接到其它容器
# --rm 容器退出后自动删除容器文件
# --volumes-from 从其它容器或数据卷挂载一些配置或其它文件
# --volume 挂载宿主机目录或文件，格式为：主机目录:容器目录
# --privileged=true 给容器内的root用户赋予最高权限，容器内的root用户就拥有了真正的root权限
# --restart
#   no 容器退出时不重启
#   on-failure[:max-retries] 容器故障退出（返回值非零）时重启，最多重启max-retries次
#   always 容器退出时总是重启
#   unless-stopped 容器退出时总是重启，但是不考虑在Docker守护进程启动时就已经停止了的容器
# --env-file 从指定文件读入环境变量

# eg:
# docker run -d -p 8080:8080 --name tomcat tomcat:8.5.51 --env-file ./env.list


# 查看容器
docker ps [选项]

# 删除容器
docker rm [选项] <容器名>

# 启动容器
# 启动和创建容器的区别在于，启动容器是针对已经创建好的容器进行启动，而创建容器则是针对镜像进行的操作
docker start [选项] <容器名>

# 停止容器
docker stop [选项] <容器名>

# 查看容器日志
docker logs [选项] <容器名>

# 查看容器内进程
docker top [选项] <容器名>

# 查看容器详细信息
docker inspect [选项] <容器名>

# 进入容器
docker exec [选项] <容器名> [命令]

# 导出容器
docker export [选项] <容器名>

# 导入容器
docker import [选项] <容器名>

# 重命名容器
docker rename [选项] <容器名> <新容器名>

# 查看容器使用的资源
docker stats [选项] <容器名>

# 查看容器端口映射
docker port [选项] <容器名>


# 导出容器中的文件
docker cp [选项] <容器名>:<容器内路径> <宿主机路径>
# 选项: -a, --archive=false  # 归档模式(默认)
#       -L, --follow-link=false  # 总是解析符号链接
#       -d, --device=false  # 复制字符和块设备
#       -r, --recursive=false  # 递归复制整个目录
#       -p, --pause=true  # 暂停容器中的所有进程


```

### docker 检查与排错

```shell
docker logs [选项] <容器名>
# 选项: -f, --follow=false  # 跟踪日志输出
#       --since=""  # 显示自某个timestamp之后的日志，或相对时间，如42m（即42分钟）
#       --tail="all"  # 从日志末尾显示多少行日志， 默认是all
#       -t, --timestamps=false  # 显示时间戳
#       --until=""  # 显示自某个timestamp之前的日志，或相对时间，如42m（即42分钟）

# 查看容器占用
docker stats [选项] <容器名>
# 选项: --all=false  # 显示所有容器（默认显示运行中的容器）
#       --format=""  # 使用Go模板显示
#      --no-stream=false  # 不显示实时流容器的统计信息
#      --no-trunc=false  # 不截断输出


# 停止所有容器
docker stop $(docker ps -a -q)


# 移除所有容器
docker rm $(docker ps -a -q)

# 移除所有镜像
docker image rmi $(docker images -q)


# 清空docker中所有的东西
docker system prune -a

# 清空缓存
docker system prune -f

# 清空未使用的镜像
docker image prune -a

# 清空未使用的容器
docker container prune

# 清空未使用的卷
docker volume prune

# 清空未使用的网络
docker network prune

# 清空未使用的构建缓存
docker builder prune

# 清空未使用的数据
docker system prune -a --volumes

# 清空所有未使用的数据
docker system prune -a --volumes --force




```

## 3.容器日志

```shell
# 查看容器日志
docker logs [选项] <容器名>
# 选项: -f, --follow=false  # 跟踪日志输出
#       --since=""  # 显示自某个timestamp之后的日志，或相对时间，如42m（即42分钟）
#       --tail="all"  # 从日志末尾显示多少行日志， 默认是all
#       -t, --timestamps=false  # 显示时间戳
#       --until=""  # 显示自某个timestamp之前的日志，或相对时间，如42m（即42分钟）



```

## docker submodule

```shell
# 获取子模块
git submodule update --init --recursive


```

## docker-compose

```shell
# 启动命令
docker-compose up [选项] [服务名]

# 选项
# -d 后台运行
# --build 构建镜像

# 删除容器
docker-compose rm [选项] [服务名]

# 删除镜像
docker-compose down [选项] [服务名]

```



## docker私服的相关命令

```shell
# 登录
docker login 

# 上传
docker push <镜像名>
