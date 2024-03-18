# Spring 基础


### Spring常见的一些模块


Spring 支持
- IoC（Inversion of Control:控制反转） 
- AOP(Aspect-Oriented Programming:面向切面编程)

Spring模块：
- Spring Core Container：核心容器， 提供IoC容器的基本功能
  - spring-core：Spring 框架基本的核心工具类。
  - spring-beans：提供对 bean 的创建、配置和管理等功能的支持。
  - spring-context：提供对国际化、事件传播、资源加载等功能的支持。
  - spring-expression：提供对表达式语言（Spring Expression Language） SpEL 的支持，只依赖于 core 模块，不依赖于其他模块，可以单独使用。
- Spring AOP：提供面向切面编程的功能
  - spring-aop：提供对 AOP 的支持。
  - spring-aspects：提供对 AspectJ 的支持。
- Spring Data Access/Integration：提供对数据库操作、事务管理、消息处理等功能的支持
  - spring-jdbc：提供对 JDBC 的支持。
  - spring-tx：提供对事务管理的支持。
  - spring-orm：提供对 ORM 工具的支持。
  - spring-oxm：提供对 Object/XML 映射的支持。
  - spring-jms：提供对 JMS 的支持。
  - spring-web：提供对 Web 应用的支持。
  - spring-webmvc：提供对 Web MVC 的支持。
  - spring-websocket：提供对 Web Socket 的支持。
  - spring-webflux：提供对 Web Flux 的支持。
- Spring Web：提供对 Web 应用的支持
  - spring-web：提供对 Web 应用的支持。
  - spring-webmvc：提供对 Web MVC 的支持。
  - spring-websocket：提供对 Web Socket 的支持。
  - spring-webflux：提供对 Web Flux 的支持。
- Spring Test：提供对单元测试和集成测试的支持
  - spring-test：提供对测试的支持。

### Spring Spring MVC Spring Boot的关系

Spring是一个开源框架
Spring MVC是Spring框架的一个模块
Spring Boot是Spring框架的一个子项目。
- 简化了Spring MVC的配置






#### 介绍一下springboot

简化spring应用的创建及部署

Spring Boot通过自动配置功能，降低了复杂性，同时支持基于JVM的多种开源框架，可以缩短开发时间，使开发更加简单和高效。



#### 3.mvc的dispatcherservlet的分派原理

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


#### restful风格在mvc的分派，如何解析参数（这个我不知道瞎答的）

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

