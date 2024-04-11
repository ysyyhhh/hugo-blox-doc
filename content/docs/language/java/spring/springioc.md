# Spring IOC

什么是IOC
- Inversion of Control 控制反转 
- **控制权由程序员转交给了Spring容器**，**由Spring容器来实例化对象**，而不是由程序员来实例化对象

控制：对象创建（实例化、管理）的控制权
反转：由程序员转交给了外部环境（Spring，IOC容器）

当我们**需要创建一个对象时，只需要配置好配置文件/注解**

## Spring IOC容器

IOC容器是**Map类型的对象**，存储了所有的bean对象，key是bean的id，value是bean对象

两种配置Bean的方式：
- XML配置
- 注解配置

## Spring Bean

Bean是被IoC容器管理的对象，Bean是一个Java对象，由Spring容器实例化、装配、管理

## 声明为Bean的注解

@Component
- 用于标注一个普通的bean
- 不区分是哪个层的

@Repository
- 用于标注一个DAO层的bean
- 但很多时候都不用这种方式
- 一般直接通过MapperScan注解扫描mapper接口（在mybatis中）

@Service
- 用于标注一个Service层的bean

@Controller
- 用于标注一个Controller层的bean


@Component和@Bean的区别
- @Component是用于标注一个普通的bean，作用于**类**；而@Bean是用于标注一个方法，作用于**方法**
- @Component是被Spring扫描到之后（@ComponentScan），**自动注册**到Spring容器中；而@Bean是在配置类中，**手动注册**到Spring容器中
- @Bean自定义性强，比如在引用第三方库的时候，可以使用@Bean注解，将第三方库的对象注册到Spring容器中

```Java
@Configuration
public class AppConfig {
    @Bean
    public TransferService transferService() {
        return new TransferServiceImpl();
    }

}
```

```xml
<bean id="transferService" class="com.example.TransferServiceImpl"/>
```

不能通过@Component实现的例子

```Java
@Configuration
public class AppConfig {
    @Bean
    public TransferService transferService() {
        return new TransferServiceImpl();
    }

    @Bean
    public TransferService transferService2() {
        return new TransferServiceImpl();
    }
}
```
为什么不能使用@Component
- 因为@Component是用于标注一个普通的bean，作用于类；而@Bean是用于标注一个方法，作用于方法

## 注入Bean的注解

Spring内置的@Autowired注解
JDK内置的@Resource注解和@Inject注解

@Autowired和@Resource的区别
- AutoWired的默认是**按照类型注入**
  - 如果有多个类型一样的bean，会变成按照名称注入
- Resource默认是按照名称注入，如果没有指定name属性，会按照类型注入
- 如果存在多个实现类, Autowired需要@Qualifier指定具体的实现类，而Resource需要name指定具体的实现类
- @Autowired 支持在构造函数、方法、字段和参数上使用。
- @Resource 主要用于字段和方法上的注入，**不支持在构造函数或参数上使用**。

SmsService 接口有两个实现类: SmsServiceImpl1和 SmsServiceImpl2，且它们都已经被 Spring 容器所管理

```java
// 报错，byName 和 byType 都无法匹配到 bean
@Autowired
private SmsService smsService;
// 正确注入 SmsServiceImpl1 对象对应的 bean
@Autowired
private SmsService smsServiceImpl1;

// 正确注入  SmsServiceImpl1 对象对应的 bean
// smsServiceImpl1 就是我们上面所说的名称
@Autowired
@Qualifier(value = "smsServiceImpl1")
private SmsService smsService;
```

```Java
// 报错，byName 和 byType 都无法匹配到 bean
@Resource
private SmsService smsService;
// 正确注入 SmsServiceImpl1 对象对应的 bean
@Resource
private SmsService smsServiceImpl1;
// 正确注入 SmsServiceImpl1 对象对应的 bean（比较推荐这种方式）
@Resource(name = "smsServiceImpl1")
private SmsService smsService;
```

## 注入Bean冲突时的问题

当我们从 Spring 容器中“拉”取一个 Bean 回来的时候，可以按照名字去拉取，也可以按照类型去拉取，按照 BeanName 拉取的话，一般来说只要 BeanName 书写没有问题，都是没问题的。但是如果是按照类型去拉取，则可能会因为 Bean 存在多个实例从而导致失败。

使用@Resource

@Qualifier 指定 name

另外还有一种方案，就是在注册 Bean 的时候，告诉 Spring 容器，这个 Bean 在通过 type 进行注入的时候，不作为候选 Bean。

## 怎么动态获取spring容器里面的bean，从哪个类中获取

从ApplicationContext中获取Bean


## Bean的作用域

- singleton：单例模式，一个Spring容器中只有一个bean实例，默认值
- prototype：原型模式，每次从容器中获取bean时，都会创建一个新的实例
- request：每次HTTP请求都会创建一个新的bean，该bean仅在当前HTTP request内有效
- session：每次HTTP请求都会创建一个新的bean，该bean仅在当前HTTP session内有效
- global session：全局session作用域，仅在基于portlet的Web应用中才有意义，Spring5废弃
- application：全局作用域，Spring5废弃
- websocket：全局作用域，Spring5废弃

配置Bean的作用域
```xml
<bean id="user" class="com.example.User" scope="prototype"/>
```

```Java
@Component
@Scope("prototype")
public class User {
}
```



## Bean的线程安全问题

与作用域有关
- singleton：线程不安全, IoC容器中只有一个bean实例，多个线程共享一个bean实例, 如果bean中有状态，会出现线程安全问题
- prototype：线程安全, 每次从容器中获取bean时，都会创建一个新的实例
- 其他的都是线程安全的

解决办法:
- 不要在bean中定义状态
- 使用ThreadLocal(推荐)

## Bean的生命周期

Bean的生命周期包括初始化和销毁两个阶段

Bean的初始化
- 通过构造方法创建bean
- 为bean的属性设置值 set()
- 如果实现了*.Aware接口，调用相应的方法
  - BeanNameAware
  - BeanFactoryAware
- 如果有相应的初始化方法就调用
  - 如果有Spring 容器相关BeanPostProcessor，调用postProcessBeforeInitialization方法
  - 如果有InitializingBean，调用afterPropertiesSet方法
  - 如果有init-method属性，调用init-method方法
- bean初始化完成

Bean的销毁
- 调用bean的销毁方法
  - 如果实现了 DisposableBean 接口，调用destroy方法
  - 如果有destroy-method属性，调用destroy-method方法
- bean销毁完成

![](img/SpringIOC/Bean的声明周期.png)


