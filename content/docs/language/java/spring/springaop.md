# Spring AOP

## 什么是AOP

AOP（Aspect-Oriented Programming）面向切面编程，是一种编程范式，它的主要目的是提高代码的模块化程度，使得代码更加易于维护和扩展。

将那些与业务无关，却为业务模块所共同调用的逻辑或责任（例如事务处理、日志管理、权限控制等）封装起来，便于减少系统的重复代码，降低模块间的耦合度，并有利于未来的可拓展性和可维护性。

Manager层的事务管理、日志管理、权限控制等功能，都是与业务逻辑无关的，但是却是业务逻辑所必须的，这些功能可以通过AOP来实现。

AOP的实现方式有两种：动态代理和CGLIB字节码增强。
- 如果目标对象实现了接口，Spring就会使用JDK的动态代理
- 如果目标对象没有实现接口，Spring就会使用CGLIB字节码增强

![](img/SpringAOP/AOP%20Process.png)

Spring AOP也集成了AspectJ，可以使用AspectJ的注解来实现AOP。

## AOP的核心概念

- Aspect（切面）：横切关注点，即模块化横切关注点的行为。比如日志、事务、权限等 = Advice + Pointcut
- Joinpoint（连接点）：程序执行的某个特定的点，比如方法的调用、异常的处理等
- Pointcut（切入点）：匹配连接点的断言，AOP通过切入点定位到连接点
- Advice（通知）：切面在连接点上执行的动作，分为前置通知、后置通知、环绕通知、异常通知、最终通知
- Introduction（引介）：在不修改类代码的前提下，为类添加新的方法和属性
- Target（目标对象）：被代理的对象
- Weaving（织入）：将切面应用到目标对象并创建新的代理对象的过程
- Proxy（代理）：被AOP框架创建的对象，用来替换原始对象

## Spring AOP 和 AspectJ 

- Spring AOP：基于代理的AOP实现，只支持方法级别的连接点
- AspectJ：基于字节码的AOP实现，支持方法级别和字段级别的连接点
- Spring AOP 属于运行时增强，AspectJ 属于编译时增强

AspectJ的通知类型:
- Before：前置通知
- After：后置通知
- AfterReturning：返回通知, 在方法返回结果后执行
- AfterThrowing：异常通知, 在方法抛出异常后执行
- Around：环绕通知, 在方法执行前后执行

## 多个切面的执行顺序

1. 使用@Order注解, 数值越小优先级越高
```java
@Aspect
@Component
@Order(1)
public class LogAspect {
    // ...
}
```
2. 实现Ordered接口, 重写getOrder()方法
```java
@Aspect
@Component
public class LogAspect implements Ordered {
    @Override
    public int getOrder() {
        return 1;
    }
}
```



## 切面、Filter、Interceptor

- Filter是Servlet规范中的一部分，是基于URL的，只能在Servlet规范中使用
  - 作用是对请求进行过滤，可以在请求到达Servlet之前或者响应到达客户端之前进行一些处理
- Interceptor的作用是在请求到达Controller之前或者响应到达客户端之前进行一些处理
- aspect是AOP的一部分，是基于Java的，可以在任何地方使用
  - 作用是对方法进行增强，比如事务、日志、权限等

执行顺序：过滤器->拦截器->切面
过滤器、拦截器属于请求层面的拦截；切面属于方法层面的拦截

实现原理不同
- Filter是基于函数回调的，依赖于Servlet容器
- Interceptor是基于反射的，依赖于Spring容器
- Aspect是基于代理的，依赖于Spring容器

使用范围不同
- Filter是基于URL的，依赖Tomcat容器
- Interceptor是基于方法的，是Spring组件，不依赖Tomcat容器，

触发时间不同
![](img/SpringAOP/触发时间.png)
请求进入容器后，但在进入servlet之前进行预处理，请求结束是在servlet处理完以后。

拦截器 Interceptor 是在请求进入servlet后，在进入Controller之前进行预处理的，Controller 中渲染了对应的视图之后请求结束。


