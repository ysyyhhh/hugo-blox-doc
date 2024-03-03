##### Service层的返回值

service 做校验，如果非法，直接抛异常 + 全局异常处理

controller 正常就是组合 service ，返回前端需要的数据。

java异常效率低下是因为抛出异常会遍历所有涉及堆栈，具体代码在基类Throwable的fillInStackTrace()方法里。但其实可以通过在自定义异常中重写fillInStackTrace()来大幅度提高异常效率。

<https://segmentfault.com/q/1010000020840854>

<https://blog.csdn.net/qq_41107231/article/details/115874974>