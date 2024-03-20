# Spring 基础

## Spring 概念

Spring 是重量级企业开发框架 Enterprise JavaBean(EJB)的替代品，Spring 为企业级 Java 开发提供了一种相对简单的方法，通过 依赖注入 和 面向切面编程，用简单的 Java 对象(Plain Old Java Object，PoJ0)实现了 EJB 的功能

缺点:
Spring的组件代码是轻量级,但是Spring的配置文件却是重量级的

Spring 2.5 引入了注解驱动的开发模式，消除了大量的XML配置

Spring 3.0 引入了Java配置的方式，可以完全不使用XML配置

但在使用某些特性时,仍然要配置
如:
- 事务管理
- SpringMVC

### 常见的一些模块


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

## Spring Spring MVC Spring Boot的关系

Spring是一个开源框架
Spring MVC是Spring框架的一个模块
Spring Boot是Spring框架的一个子项目。
- 简化了Spring MVC的配置





### springboot

为了简化spring应用的创建及部署

SpringBoot优点:

Spring Boot通过自动配置功能，降低了复杂性，同时支持基于JVM的多种开源框架，可以缩短开发时间，使开发更加简单和高效。

Spring Boot 遵循“约定优于配置”的原则，提供了一种快速构建Spring应用的方式。(默认配置可以修改)

提供了嵌入式的Tomcat、Jetty、Undertow等容器，可以通过main方法直接运行。

#### Spring Boot Starter

Spring Boot Starter 是 Spring Boot 的一个重要特性，它是一种特殊的依赖，可以简化 Maven 或 Gradle 的配置，使得构建 Spring Boot 应用更加简单。
spring-boot-starter-web：提供对 Web 应用的支持。

### Spring Boot的特性

支持的Servlet容器:
- Tomcat
- Jetty
- Undertow

如何在Spring Boot中使用Jetty
- 在pom.xml中排除Tomcat
- 添加Jetty的依赖

### SpringBootApplication注解

SpringBootApplication注解是Spring Boot的核心注解，它是一个组合注解，包括了@Configuration、@EnableAutoConfiguration、@ComponentScan等注解。

这三个注解的功能:
- @Configuration：表明该类是一个配置类，它会被Spring容器扫描并且用于构建Bean定义，这些Bean定义将被用于构建Spring应用上下文。
- @ComponentScan：自动扫描并加载符合条件的组件或者bean。
- @EnableAutoConfiguration：开启Spring Boot的自动配置功能。

### SpringBoot的自动配置

Spring Boot 的自动配置功能是 Spring Boot 的一个重要特性，它可以根据应用的依赖和配置自动配置 Spring 应用。

Spring Boot 的自动配置功能是通过 @EnableAutoConfiguration 注解实现的，它会根据应用的依赖和配置自动配置 Spring 应用。

自动装配核心功能的实现实际是通过 AutoConfigurationImportSelector类

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@AutoConfigurationPackage //作用：将main包下的所有组件注册到容器中
@Import({AutoConfigurationImportSelector.class}) //加载自动装配类 xxxAutoconfiguration
public @interface EnableAutoConfiguration {
    String ENABLED_OVERRIDE_PROPERTY = "spring.boot.enableautoconfiguration";

    Class<?>[] exclude() default {};

    String[] excludeName() default {};
}
```


AutoConfigurationImportSelector 类实现了 ImportSelector接口，也就实现了这个接口中的 selectImports方法，该方法主要用于获取所有符合条件的类的全限定类名，这些类需要被加载到 IoC 容器中。

```java
private static final String[] NO_IMPORTS = new String[0];

public String[] selectImports(AnnotationMetadata annotationMetadata) {
        // <1>.判断自动装配开关是否打开
        if (!this.isEnabled(annotationMetadata)) {
            return NO_IMPORTS;
        } else {
          //<2>.获取所有需要装配的bean
            AutoConfigurationMetadata autoConfigurationMetadata = AutoConfigurationMetadataLoader.loadMetadata(this.beanClassLoader);
            AutoConfigurationImportSelector.AutoConfigurationEntry autoConfigurationEntry = this.getAutoConfigurationEntry(autoConfigurationMetadata, annotationMetadata);
            return StringUtils.toStringArray(autoConfigurationEntry.getConfigurations());
        }
    }

```

### 开发RESTful Web的注解有哪些

RESTful是一种软件架构风格，它是一种设计风格而不是标准，它是一种针对网络应用的设计和开发方式，可以降低开发的复杂性，提高系统的可伸缩性。

Spring MVC 提供了一些注解来简化 RESTful Web 的开发，这些注解包括：
- @RestController：用于定义 RESTful Web 服务。
  - 是@Controller和@ResponseBody的组合注解
  - 表示这是个控制器，并且是一个RESTful的控制器
- @Component、@Service、@Repository：用于定义组件。
- @GetMapping、@PostMapping、@PutMapping、@DeleteMapping：用于定义 GET、POST、PUT、DELETE 请求。
- @RequestParam、@PathVariable、@RequestBody：分别在处理方法的参数上使用，用于获取请求参数、路径参数、请求体。


### Spring Boot的配置文件

Spring Boot 的配置文件有两种格式：properties 和 YAML。

Spring Boot 的配置文件有以下几种位置，对应的优先级从高到低：
- 当前目录下的 config 目录
- 当前目录
- classpath 下的 config 目录
- classpath 根目录
- 开发时 resources 目录
- 以上位置的 application-{profile}.properties 或 application-{profile}.yml


读取配置文件

@Value注解
- 用于读取配置文件中的属性值
```java
@Value("${name}")
private String name;
```

@ConfigurationProperties注解
- 读取并绑定配置文件中的属性值
```java
@ConfigurationProperties(prefix = "person")
public class Person {
    private String name;
    private Integer age;
    private String
}
```





## Spring 中的设计模式

- 工厂模式
  - BeanFactory
  - ApplicationContext
- 单例模式
  - Bean的作用域
- 代理模式
  - AOP
- 观察者模式
  - Spring事件驱动模型
- 适配器模式
  - HandlerAdapter
  - HandlerMapping
- 模板方法模式
  - JdbcTemplate


## Spring Data JPA

Spring Data JPA 是 Spring 基于 ORM 框架 JPA 封装的一个子项目，用于简化 JPA 的使用。

Spring Data JPA 提供了一种新的方法来定义仓库接口，通过定义仓库接口来自动生成仓库实现。

Spring Data JPA 通过解析方法名来自动生成 SQL 语句，从而简化了开发。

### 实战

#### 创建实体类

```java
@Entity
@Table(name = "t_user")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String username;
    private String password;
    private String email;
    private String phone;
    private Date created;
    private Date updated;
    // 省略 getter 和 setter
}
```

使某个字段不参与持久化

```java
@Transient
private String code;
```

### JPA的审计功能

JPA提供了审计功能，可以自动记录实体的创建时间和更新时间。

```java
@EntityListeners(AuditingEntityListener.class)
@MappedSuperclass

public class BaseEntity {
    @CreatedDate
    private Date created;
    @LastModifiedDate
    private Date updated;
    // 省略 getter 和 setter
}
```

需要在启动类上添加`@EnableJpaAuditing`注解
```java
@Configuration
@EnableJpaAuditing
public class JpaConfig {
}
```
## Hibernate

Hibernate 是一个开源的对象关系映射框架，它是一个优秀的ORM（Object-Relational Mapping）框架，它对 JDBC 进行了封装，提供了对象关系映射的功能，可以将 Java 对象映射到数据库表中。


## Spring Security

Spring Security 是 Spring 提供的一个安全框架，用于对 Java 应用程序进行安全认证和授权。

hasRole和hasAuthority的区别
- hasRole：会在参数上加上ROLE_前缀(所以数据库中的角色名要加上ROLE_前缀)
- hasAuthority：不会在参数上加上ROLE_前缀
 

加密
- BCryptPasswordEncoder
