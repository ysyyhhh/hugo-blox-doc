# docker相关技巧

## 记把深度学习项目装入docker

安装时出现选项

```Dockerfile
# RUN apt-get install libglib2.0-dev -y
# 由于安装libglib2.0-dev的时候，bash会有交互操作叫你选择对应的时区，在docker build的时候没有交互的，所以需要加上DEBIAN_FRONTEND="noninteractive"
RUN DEBIAN_FRONTEND="noninteractive" apt -y install libglib2.0-dev

```

## docker清理

在win10下，docker是基于wsl2的，所以docker的镜像和容器都是在wsl2的文件系统中。
所以在清理完docker的镜像和容器后，需要对wsl的盘进行压缩。

```bash
# 停止所有的容器
docker stop $(docker ps -aq)

# 删除所有未使用的容器
docker volume prune

# 删除所有未使用的镜像
docker image prune -a

# 删除缓存
docker builder prune


# 查看当前占用的空间
docker system df


```

对wsl2的盘进行压缩

```bash
wsl --shutdown

# 查看wsl2的盘
wsl --list -v

# 使用diskpart压缩
diskpart
# open window Diskpart
select vdisk file="D:\ubuntu\wsl\docker-desktop-data\ext4.vhdx"
attach vdisk readonly
compact vdisk
detach vdisk
exit
```

## docker中安装conda

```Dockerfile

# 安装conda

RUN apt-get install -y wget

# yhyu13 : donwload anaconda package & install
RUN wget "https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh" 

RUN sh Anaconda3-2023.03-1-Linux-x86_64.sh -b -p /opt/conda

# RUN rm /anaconda.sh 

RUN ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh

RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc

# yhyu13 : add conda to path  
ENV PATH /opt/conda/bin:/opt/conda/condabin:$PATH
```

## docker-compose 使用gpu

```yaml
version: '3.7'
services:
  pytorch:
    build: .
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=all
    volumes:
      - .:/workspace
    ports:
      - "8888:8888"
      - "6006:6006"
    command: bash -c "jupyter notebook --ip
```

## wsl 盘迁移到非系统盘

一般情况下 wsl盘的位置在
`C:\Users\<用户名>\AppData\Local\Docker\wsl`

docker的盘在
`C:\Users\<用户名>\AppData\Local\Docker\wsl\data`

```bash

# 1. 停止wsl
wsl --shutdown

# 2. 查看wsl状态
wsl --list -v
# 可以看到docker有两个wsl，一个是docker-desktop-data，一个是docker-desktop
# 只需要迁移docker-desktop-data即可,另一个很小

# 3. 迁移wsl
wsl --export Ubuntu-20.04 D:\ubuntu\wsl\Ubuntu-20.04.tar

# 4. 删除wsl
wsl --unregister Ubuntu-20.04


# 5. 查看是否删除成功
wsl --list -v

# 6. 导入wsl
wsl --import Ubuntu-20.04 D:\ubuntu\wsl\Ubuntu-20.04 D:\ubuntu\wsl\Ubuntu-20.04.tar --version 2

# 7. 查看是否导入成功
wsl --list -v
```

## docker 中设置特定版本的python

```shell


# 创建一个基础镜像 
FROM ubuntu:20.04

# 重置apt-get
RUN rm -rf /etc/apt/sources.list

# 安装conda
# yhyu13 : install additional packages
# 设置apt的源为tsinghua镜像源
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y curl wget

# 安装conda
RUN curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda \
    && rm Miniconda3-latest-Linux-x86_64.sh

# 创建conda环境并安装python
RUN /opt/conda/bin/conda create -n py38 python=3.8.5
ENV PATH /opt/conda/envs/py38/bin:$PATH

```

## docker中使用display

在启动时需要设置环境变量DISPLAY

### win下的情况

参考[在Docker for Windows中运行GUI程序](https://www.cnblogs.com/larva-zhh/p/10531824.html)


报错：
libGL error: No matching fbConfigs or visuals found

libGL error: failed to load driver: swrast

解决办法：
-  https://bbs.huaweicloud.com/blogs/281862
-  或取消勾选 native opengl

### ubuntu下的情况

安装虚拟显示屏
https://blog.csdn.net/Ber_Bai/article/details/127768374

挂载卷传入 /tmp/.X11-unix
DISPLAY一般是:1.0

在宿主机上
xhost +

## 前后端项目静态资源转发

后端 springboot时：
把静态资源放在static目录下，然后在application中配置

```yaml
spring:
  mvc:
    static-path-pattern: /static/**
  resources:
    static-locations: classpath:/static/
```

如果设置了拦截器，需要在拦截器上加入

```java
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    @Bean
    public CorsInterceptor corsInterceptor() {
        return new CorsInterceptor();
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(corsInterceptor())
                .addPathPatterns("/**");
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/static/**").addResourceLocations("classpath:/static/", "file:static/");
    }

}

```

jar 包和静态路径关系

```md
- .jar
- static
```

前端，需要在nginx上加入转发后访问静态路径后缀。

```nginx
    location /api {
        rewrite ^/api(.*) $1 break;
        proxy_pass $SERVER_URL;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Photo $scheme;

        location ~*.+\.(jpg|jpeg|gif|png|ico|css|js|pdf|txt|swf|xml|woff|woff2|ttf|eot|svg)$ {
            rewrite ^/api(.*) $1 break;
            proxy_pass $SERVER_URL;
            proxy_redirect off;
        }

    }
```
