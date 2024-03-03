
# docker Usage

## 多阶段构建docker镜像

多阶段构建的修改不会保留到下一阶段，只有COPY和ADD命令会保留到下一阶段

usages：

- 第一阶段：编译/打包程序依赖

多阶段用途：

- 缩小镜像体积
-

## 新系统build时出现`Cannot autolaunch D-Bus without X11 $DISPLAY`

docker 拉取包时需要登录.

问题出在Linux缺少一个密码管理包gnupg，它用于加密，我们在登录时需要这个包将密码加密后才能完成，因此直接安装

```shell
sudo apt install gnupg2 pass
```
