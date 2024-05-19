# npm

## docker中的npm

[解决npm慢](https://blog.csdn.net/wenxuankeji/article/details/135658361)

```shell
# 设置npm源
npm config set registry https://registry.npmmirror.com

# 原有域名弃用了
## https://npm.taobao.org => https://npmmirror.com
# https://registry.npm.taobao.org => https://registry.npmmirror.com


# npm install 时查看详细信息
npm install --verbose
```


