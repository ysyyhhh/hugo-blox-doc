# SpringMVC

## 1. SpringMVC简介

MVC是Model-View-Controller的缩写，是一种设计模式，用于开发Web应用程序。SpringMVC是Spring框架的一个模块，用于开发Web应用程序。

Model1时代

这个模式下 JSP 即是控制层（Controller）又是表现层（View）。显而易见，这种模式存在很多问题。比如控制逻辑和表现逻辑混杂在一起，导致代码重用率极低；再比如前端和后端相互依赖，难以进行测试维护并且开发效率极低。
![](img/SpringMVC/Model1.png)

Model2时代

早期MVC
Model:系统涉及的数据，也就是 dao 和 bean。
View：展示模型中的数据，只是用来展示。
Controller：接受用户请求，并将请求发送至 Model，最后返回数据给 JSP 并展示给用户
![](img/SpringMVC/Model2.png)

存在的问题有:
- 代码耦合度高, 代码重用率低

SpringMVC

MVC 是一种设计模式，Spring MVC 是一款很优秀的 MVC 框架。Spring MVC 可以帮助我们进行更简洁的 Web 层的开发，并且它天生与 Spring 框架集成。Spring MVC 下我们一般把后端项目分为 Service 层（处理业务）、Dao 层（数据库操作）、Entity 层（实体类）、Controller 层(控制层，返回数据给前台页面)。


## SpringMVC核心组件

SpringMVC的核心组件有：
- DispatcherServlet: 核心的Servlet，用于接收请求并分发请求
- HandlerMapping: 处理器映射器，用于查找处理器
- HandlerAdapter: 处理器适配器，用于执行处理器
- Handler: 处理器，用于处理请求
- ViewResolver: 视图解析器，用于解析视图



## SpringMVC的工作流程(mvc的dispatcherservlet的分派原理)

![](img/SpringMVC/SpringMVC工作流程.png)

1. 浏览器发送请求, `DispatcherServlet` 拦截请求
2. `DispatcherServlet` 根据请求信息调用 `HandlerMapping`
   1. `HandlerMapping` 根据URL找到对应的 `Handler`,即Controller
3. `DispatcherServlet` 调用 `HandlerAdapter`
   1. `HandlerAdapter` 执行 `Handler`
4. `Handler` 执行完毕返回 `ModelAndView`
5. `DispatcherServlet` 调用 `ViewResolver`
   1. `ViewResolver` 解析 `ModelAndView` 返回 `View`
6. `DispatcherServlet` 把ModelAndView传给View
   1. `View` 渲染数据并返回给 `DispatcherServlet`
7. `DispatcherServlet` 把 `View` 返回给浏览器


![image-20230413193651300](4.13滴滴准备/img/image-20230413193651300.png)

1. 用户发送 请求到 前端控制器（DispatcherServlet）。
2. 前端控制器 请求 **处理器映射器**（HandlerMapping）去 查找 处理器（Handler）。
3. 找到以后 处理器映射器（HandlerMappering）向 前端控制器 返回 执行链（HandlerExecutionChain）。
4. 前端控制器（DispatcherServlet）调用 **处理器适配器**（HandlerAdapter） 去执行 处理器（Handler）。
5. 处理器适配器 去执行 处理器Handler。
6. 处理器 执行完给 处理器适配器 返回ModelAndView。
7. **处理器适配器** 向 前端控制器 返回ModelAndView。
8. 前端控制器 请求 **视图解析器**（ViewResolver）去进行 视图解析。
9. 视图解析器 向 前端控制器返回View。
10. 前端控制器 对 **视图进行渲染**。
11. 前端控制器 向用户**响应结果**。


## restful风格在mvc的分派，如何解析参数（这个我不知道瞎答的）

restful 即 URL表示资源， + GET POST PUT DELETE 表示行为

Restful风格的请求是使用 **url+请求方式** 表示一次请求目的的，并且规范了一些的状态码，使得看到接口就知道请求要干嘛。

RequestMappingURL

PathVariable 获取参数

- `@Controller`声名一个处理请求的控制器

- `@RequestMapping`请求映射地址，它存在几个子注解对于实现`REST`风格来说更加具有语义性

- - `GETMapping` GET请求
  - `PUTMapping` PUT请求
  - `POSTMapping` POST请求
  - `DELETEMapping` DELETE请求`sponseBody` 将响应内容转换为`JSON`格式

- `@RequestBody` 请求内容转换为`JSON`格式

- `@PathVariable("id")`用于绑定一个参数

- `@RESTController` 等同于`@Controller`+`@ResponseBody`在类上写了这个注解，标识这个类的所有方法只返回数据，而不进行视图跳转



## 统一异常处理

SpringMVC提供了`@ControllerAdvice`注解，用于统一处理异常。`@ControllerAdvice`注解可以用于定义一个全局的异常处理类，用于处理所有Controller中抛出的异常。

还会用到`@ExceptionHandler`注解，用于定义一个方法，用于处理指定类型的异常。

```java
@ControllerAdvice
@ResponseBody
public class GlobalExceptionHandler {
    @ExceptionHandler(Exception.class)
    public Result handleException(Exception e) {
        return new Result("500", e.getMessage());
    }
}
```


这种方式可以统一处理异常，避免在每个Controller中都写异常处理代码。

如果需要对不同的异常做不同的处理，可以定义多个`@ExceptionHandler`方法

ExceptionHandlerMethodResolver 中 getMappedMethod 方法，根据异常类型找到对应的方法，然后执行。
```java
@Nullable
  private Method getMappedMethod(Class<? extends Throwable> exceptionType) {
    List<Class<? extends Throwable>> matches = new ArrayList<>();
    //找到可以处理的所有异常信息。mappedMethods 中存放了异常和处理异常的方法的对应关系
    for (Class<? extends Throwable> mappedException : this.mappedMethods.keySet()) {
      if (mappedException.isAssignableFrom(exceptionType)) {
        matches.add(mappedException);
      }
    }
    // 不为空说明有方法处理异常
    if (!matches.isEmpty()) {
      // 按照匹配程度从小到大排序
      matches.sort(new ExceptionDepthComparator(exceptionType));
      // 返回处理异常的方法
      return this.mappedMethods.get(matches.get(0));
    }
    else {
      return null;
    }
  }

```
getMappedMethod() 会首先找到所有可以处理的异常信息，然后按照匹配程度从小到大排序，最后返回处理异常的方法。


