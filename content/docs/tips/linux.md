# Linux

## 系统资源相关

```shell
# 查看内存
free -h

# 查看cpu
cat /proc/cpuinfo

# 查看cpu使用情况
top

# 查看GPU使用情况
nvidia-smi


# 查看磁盘
df -h

# 查看系统版本
cat /etc/os-release

# 查看系统信息
uname -a


# 列出所有文件夹和文件 显示占用空间
du -sh *

# 查看文件夹大小
du -sh folder_name

# 查看文件大小
du -sh file_name

```

## 用户相关

```shell
# 创建用户
useradd -m -s /bin/bash -d /home/username username
## 解释: -m 创建用户目录, -s 指定shell, -d 指定用户目录

# 设置密码
passwd username

# 删除用户
userdel -r username

# 添加用户的sudo权限
## 编辑sudoers文件
vi /etc/sudoers
## 在root ALL=(ALL) ALL下面添加
username ALL=(ALL) ALL

# 查看用户组
groups username

# 修改用户组
usermod -g groupname username

# 查看所有用户
cat /etc/passwd

```

## 目录挂载

```shell

# 查看挂载
df -h

# 挂载目录
mount /dev/sdb1 /home/username/data

# 卸载目录
umount /home/username/data

# 挂载硬盘
## 查看硬盘
fdisk -l

## 格式化硬盘
fdisk /dev/sdb

## 格式化为ext4
mkfs.ext4 /dev/sdb1

```

挂载目录并立即生效

```shell
# 挂载目录
mount /dev/sdb1 /home/username/data

# 立即生效
mount -a

```

## 文件

```shell

# 带权限复制
cp -rp source dest

# 远程连接复制文件
scp -r username@ip:/home/username/data /home/username/data


# 权限设置
chmod 777 filename
# 参数解释
# 7: 111 读写执行
# 6: 110 读写
# 5: 101 读执行

# 三位数分别代表所有者、所属组、其他用户的权限
# 读、写、执行分别用4、2、1表示
```

## 工具

### 压缩解压缩
```shell
# 压缩
tar -czvf filename.tar.gz foldername

# 解压
tar -xzvf filename.tar.gz
```

```
### 定时脚本
```shell
# 查看定时脚本
crontab -l
```
### curl

```shell
# 下载文件
curl -o filename url

```

## 系统路径/变量

持久化添加/改变系统路径/变量

```shell
# 添加到系统路径
echo 'export PATH=$PATH:/home/username/bin' >> /etc/profile

# 立即生效
source /etc/profile
```

## tool

### ssh
```shell
# 生成密钥
ssh-keygen -t rsa -C "{email}"

# 查看密钥
cat ~/.ssh/id_rsa.pub
```

### apt

```shell
# 设置tsinghua源
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# 更新源
s
```


