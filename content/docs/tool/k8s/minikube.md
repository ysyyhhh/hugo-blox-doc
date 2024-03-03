# minikube

使用

进入pods的容器

```bash
kubectl exec -it <pod-name> -c <container-name> -- /bin/bash

# 查看对应容器的日志

kubectl logs -f <pod-name> -c <container-name>
```

## 错误和解决方案

### minikube 挂载 本地目录进minikube时,作为mysql的数据目录,但是mysql无法启动

挂载方式:
在minikube正常启动后, 使用

```shell
minikube mount <本地目录>:<minikube目录>

```

进行挂载

检查问题

```bash

# 进入pod 的 db容器内查看日志 
kubectl logs -f <pod-name> -c <container-name>

```

输出为

```shell
find: File system loop detected; '/var/lib/mysql/test' is part of the same file system loop as '/var/lib/mysql/'.
```

原因是挂载时发现循环

解决方案:

1. 关闭并**删除**minikube

```shell
minikube stop
minikube delete
```

2. 在minikube启动时就挂载

```shell
minikube start --mount --mount-string="<本地目录>:<minikube目录>"
```

问题解决

### minikube 中 设置ingress未转发的问题

参考[Could not access Kubernetes Ingress in Browser on Windows Home with Minikube?](https://stackoverflow.com/questions/66275458/could-not-access-kubernetes-ingress-in-browser-on-windows-home-with-minikube)

问题1：
当使用minikube时，设置ingress后，minikube ssh 内部可以通过ingress转发的服务端口访问。
但127.0.0.1 或 minikube ip 在主机上无法访问。

解决方法：

```md
Set custom domain IP to 127.0.01 in %WINDIR%\System32\drivers\etc\hosts file, i.e. by adding line 127.0.0.1 my-k8s.com
Get ingress pod name: kubectl get pods -n ingress-nginx
Start port forwarding: kubectl -n ingress-nginx port-forward pod/ingress-nginx-controller-5d88495688-dxxgw --address 0.0.0.0 80:80 443:443, where you should replace ingress-nginx-controller-5d88495688-dxxgw with your ingress pod name.
Enjoy using ingress on custom domain in any browser (but only when port forwarding is active)
```

问题2:
ingress中使用prefix的转发规则时,无法获取路径中的query

解决方法:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/use-regex: "true" # 需要添加这个
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  defaultBackend:
    service:
      name: default-http-backend
      port:
        number: 80
  rules:
    - host: fuzzs-scene-sim-test.localhost
      http:
        paths:
          - path: /FuzzsSceneSimTest(/|$)(.*) # 后缀加上(/|$)(.*) 用于获取query
            pathType: ImplementationSpecific 
            backend:
              service:
                name: fuzzs-scene-sim-test
                port:
                  number: 8089
```