# k8s
 
**[kubectl](https://kubernetes.io/zh-cn/docs/reference/kubectl/) 命令行工具**

kubectl [command] [TYPE] [NAME] [flags]

\- `command`：指定要对一个或多个资源执行的操作，例如 `create`、`get`、`describe`、`delete`。

\- `TYPE`：指定[资源类型](https://kubernetes.io/zh-cn/docs/reference/kubectl/#resource-types)。资源类型不区分大小写， 可以指定单数、复数或缩写形式。

\- `NAME`：指定资源的名称。名称区分大小写。 如果省略名称，则显示所有资源的详细信息。例如：

命令大全

```
- kubectl get:列出资源,比如 pod、deployment、service 等
- kubectl describe:显示资源的详细信息
- kubectl create:创建资源,比如 pod、deployment、service 等
- kubectl delete:删除资源
- kubectl apply:对资源进行配置更改
- kubectl rollout:管理资源的发布,比如 deployment 的发布
- kubectl scale:扩缩 pod 副本数
- kubectl expose:暴露资源为 service
- kubectl logs:打印 pod 的日志
- kubectl exec:在 pod 内执行命令
- kubectl cp:在 pod 之间 copy 文件
- kubectl port-forward:将 pod 的端口转发到本地
- kubectl label:给资源加标签
- kubectl annotate:给资源加注释
- kubectl config:管理 kubeconfig 文件
- kubectl cluster-info:显示集群信息
- kubectl version:显示 CLI 版本和服务端版本
- kubectl api-versions:显示所支持的 API 版本
- kubectl api-resources:显示每个API group下的资源列表
```

常用命令

```

kubectl get 资源类型
kubectl get pod
kubectl get pod -o wide
kubectl get deployment
kubectl get deployment -o wide
kubectl get namespace
# 指定查看某个命名空间下的pod
kubectl get pod -n kube-system
# 查看所有命名空间下的pod
kubectl get pod -A -o wide

kubectl describe 资源类型
kubectl describe pod
kubectl describe pod web-nginx-dep2-5f4fbd5bfb-jqw9z
kubectl describe pod -o wide
kubectl describe deployment
kubectl describe deployment -o wide
kubectl describe namespace
# 指定查看某个命名空间下的pod
kubectl describe pod -n kube-system
# 查看所有命名空间下的pod
kubectl describe pod -A -o wide

kubectl logs 显示pod中的容器中运行过程中产生的日志信息
kubectl logs ngx-dep3-64cfcc9ddc-92x9s
kubectl logs injoi-5c9b8f98bd-trm95 | grep "capturing the emotions" -A 100 -B 100 搜索并查看上下文
kubectl run bx --image=busybox
kubectl exec -it nginx-dep1-6dd5d75f8b-mgndd /bin/bash
kubectl exec -it pod对象 /bin/bash



```

<https://kubernetes.io/zh-cn/docs/>

# container

# pod

Pod 类似于共享名字空间并共享文件系统卷的一组容器。

# deployment

## depployment.yaml

① `apiVersion` 是当前配置格式的版本。\
② `kind` 是要创建的资源类型，这里是 `Deployment`。\
③ `metadata` 是该资源的元数据，`name` 是必需的元数据项。\
④ `spec` 部分是该 `Deployment` 的规格说明。\
⑤ `replicas` 指明副本数量，默认为 1。\
⑥ `template` 定义 Pod 的模板，这是配置文件的重要部分。\
⑦ `metadata` 定义 Pod 的元数据，至少要定义一个 label。label 的 key 和 value 可以任意指定。\
⑧ `spec` 描述 Pod 的规格，此部分定义 Pod 中每一个容器的属性，`name` 和 `image` 是必需的。

# secret

Secret 是 Kubernetes 中的一种资源,用于存储敏感信息,比如密码、OAuth 令牌、SSH 密钥等。Secret 的数据是 base64 编码并存储在 etcd 中。Secret 有三种类型:1. Opaque:任意数据,用于存储密码、密钥等;base64 编码后存储。\
2\. [kubernetes.io/service-account-token:服务账号令牌,由](http://kubernetes.io/service-account-token:%E6%9C%8D%E5%8A%A1%E8%B4%A6%E5%8F%B7%E4%BB%A4%E7%89%8C,%E7%94%B1) Kubernetes 自动创建和更新。\
3\. [kubernetes.io/dockercfg:Docker](http://kubernetes.io/dockercfg:Docker) 配置文件,用来存储私有 Docker Registry 的认证信息。主要用途是:- 存储敏感数据,比如密码、密钥、认证信息等\
\- 在 Pod 中设置环境变量\
\- 用于拉取私有镜像仓库的镜像创建 Secret 有三种方式:1. 从文件中创建:

```
bash
kubectl create secret generic <secret-name> --from-file=path/to/file
```

2\. 从字串中创建:

```
bash
kubectl create secret generic <secret-name> --from-literal=<key>=<value> 
```

3\. 编写 YAML 文件创建:

```
yaml
apiVersion: v1
kind: Secret  
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=   # base64 编码后的密码或密钥
  password: MWYyZDFlMmU2N2Rm   # base64 编码后的密码或密钥 
```

在 Pod 中可以以三种方式使用 Secret:1. 设置环境变量的值 `env`\
2\. 以 Volume 文件的形式挂载,然后在 Volume 中访问\
3\. 使用 kubectl 在本地执行工具中设置 Secret总的来说,Secret 用于在 Kubernetes 集群中存储敏感信息,有以下主要用途:- 存储密码、密钥、认证信息等敏感数据\
\- 用于在 Pod 中设置环境变量的值\
\- 用于在 Volume 中创建 config 文件\
\- 拉取私有 Docker Registry 的镜像

# namespace
