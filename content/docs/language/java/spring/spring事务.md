# Spring事务

## 事务的特性

- 原子性(Atomicity): 事务是一个不可分割的工作单位，事务中的操作要么都发生，要么都不发生。
- 一致性(Consistency): 事务必须使数据库从一个一致性状态变换到另一个一致性状态。
- 隔离性(Isolation): 一个事务的执行不能被其他事务干扰。
- 持久性(Durability): 事务一旦提交，它对数据库中数据的改变是永久性的。

保证AID,C才能被满足

## 为什么要有事务

系统中的业务方法可能包括了多个原子性的数据库操作

如:
```java
public void savePerson() {
  personDao.save(person);
  personDetailDao.save(personDetail);
}
```
这些操作需要保证原子性，要么都成功，要么都失败

事务能否生效, 取决于数据库引擎的支持, 需要是innodb引擎


## Spring事务管理

MySQL保证原子性是通过回滚日志(undo log) 实现的.
如果执行遇到异常, 会回滚到事务开始前的状态. 且回滚日志先于数据的持久化.

Spring事务管理的方式有两种：
- 编程式事务管理
- 声明式事务管理

### 编程式事务管理

编程式事务管理是通过编程的方式来管理事务。

在编程式事务管理中，需要在代码中显式的调用事务管理的API来管理事务

会导致业务代码和事务管理代码耦合在一起，不利于事务管理逻辑的重用, 很少用

通过`TransactionTemplate` 或者 `PlatformTransactionManager` 来管理事务

```java
public class AccountService {
    private JdbcTemplate jdbcTemplate;
    private TransactionTemplate transactionTemplate;

    public void setJdbcTemplate(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public void setTransactionTemplate(TransactionTemplate transactionTemplate) {
        this.transactionTemplate = transactionTemplate;
    }

    public void transfer(final String outUser, final String inUser, final Double money) {
        transactionTemplate.execute(new TransactionCallbackWithoutResult() {
            @Override
            protected void doInTransactionWithoutResult(TransactionStatus transactionStatus) {
                jdbcTemplate.update("update account set money = money - ? where username = ?", money, outUser);
                jdbcTemplate.update("update account set money = money + ? where username = ?", money, inUser);
            }
        });
    }
}
```

### 声明式事务管理

声明式事务管理是通过配置的方式来管理事务。

在声明式事务管理中，只需要在配置文件中声明事务管理的相关属性，就可以在业务代码中实现事务管理，而不需要在业务代码中负责事务管理的代码。

实际基于 AOP 实现（基于`@Transactional` 的全注解方式使用最多）

```java
@Service
public class AccountService {
    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Transactional
    public void transfer(String outUser, String inUser, Double money) {
        jdbcTemplate.update("update account set money = money - ? where username = ?", money, outUser);
        jdbcTemplate.update("update account set money = money + ? where username = ?", money, inUser);
    }
}
```

## Spring事务的传播行为

事务的传播行为是指在**多个事务方法相互调用的情况下，事务管理器如何管理事务的传播行为**。

当事务方法A调用事务方法B时，Spring事务管理器会根据**事务方法B的传播行为**来决定事务方法B是否加入事务方法A的事务。

我们在 A 类的aMethod()方法中调用了 B 类的 bMethod() 方法。这个时候就涉及到业务层方法之间互相调用的事务问题。如果我们的 **bMethod()如果发生异常需要回滚**，如何配置事务传播行为才能**让 aMethod()也跟着回滚**呢？



Spring事务的传播行为有以下几种：
### 会发生回滚的四种情况
#### REQUIRED
默认且最常见的传播行为，如果当前没有事务，就新建一个事务，如果当前存在事务，就加入该事务。

- 如果外部方法没有开启事务, REQUIRED修饰的内部方法会开启一个新的事务.
- 如果外部方法开启了事务, REQUIRED修饰的内部方法会加入到外部方法的事务中, 即属于同一个事务.

其中一个方法回滚,就都回滚
```java
@Service
Class A {
    @Autowired
    B b;
    @Transactional(propagation = Propagation.REQUIRED)
    public void aMethod {
        //do something
        b.bMethod();
    }
}
@Service
Class B {
    @Transactional(propagation = Propagation.REQUIRED)
    public void bMethod {
       //do something
    }
}
```


#### REQUIRES_NEW

新建一个事务，如果当前存在事务，就把当前事务挂起。

也就是说**不管外部方法是否开启事务**，Propagation.REQUIRES_NEW修饰的内部方法会**新开启自己的事务**，且开启的**事务相互独立，互不干扰**。


即,一般情况下, ab回滚互不影响.

但如果b方法**抛出了未被捕获的异常**, 且这个异常满足a的回滚规则,a才会跟着回滚.


```java
@Service
Class A {
    @Autowired
    B b;
    @Transactional(propagation = Propagation.REQUIRED)
    public void aMethod {
        //do something
        b.bMethod();
    }
}

@Service
Class B {
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void bMethod {
       //do something
    }
}
```


#### NESTED

如果当前存在事务，则在嵌套事务内执行，如果当前没有事务，则新建一个事务。

- 在外部方法开启事务的情况下，在**内部开启一个新的事务，作为嵌套事务存在**。
- 如果外部方法无事务，则单独开启一个事务，与 PROPAGATION_REQUIRED 类似。

即, 
a回滚, b一定回滚
b回滚,a不会滚

```java
@Service
Class A {
    @Autowired
    B b;
    @Transactional(propagation = Propagation.REQUIRED)
    public void aMethod {
        //do something
        b.bMethod();
    }
}

@Service
Class B {
    @Transactional(propagation = Propagation.NESTED)
    public void bMethod {
       //do something
    }
}
```

#### MANDATORY

如果当前存在事务，则加入该事务；如果当前没有事务，则抛出异常。（mandatory：强制性）

- 如果外部方法没有开启事务, MANDATORY修饰的内部方法会抛出异常.
- 如果外部方法开启了事务, MANDATORY修饰的内部方法会加入到外部方法的事务中, 即属于同一个事务.





#### 不会发生回滚的情况
- PROPAGATION_SUPPORTS：支持当前事务，如果当前没有事务，就以非事务方式执行。
- PROPAGATION_NOT_SUPPORTED：以非事务方式执行操作，如果当前存在事务，就把当前事务挂起。
- PROPAGATION_NEVER：以非事务方式执行，如果当前存在事务，则抛出异常。

## Spring事务的隔离级别

事务的隔离级别是指多个事务之间的隔离程度，事务的隔离级别有以下几种：
- DEFAULT：使用数据库默认的隔离级别。
  - MySQL 默认的隔离级别是 REPEATABLE_READ
  - Oracle 默认的隔离级别是 READ_COMMITTED
- READ_UNCOMMITTED：允许脏读、不可重复读和幻读
  - 允许一个事务读取另一个事务未提交的数据
- READ_COMMITTED：禁止脏读，但是允许不可重复读和幻读。
  - 允许一个事务读取另一个事务已提交的数据
- REPEATABLE_READ：禁止脏读和不可重复读，但是允许幻读。
  - 对同一字段的多次读取结果是一致的
- SERIALIZABLE：禁止脏读、不可重复读和幻读。
  - 最高的隔离级别，会导致性能下降


## 事务超时

是指一个事务所允许执行的最长时间，如果超过该时间限制但事务还没有完成，则自动回滚事务.

## 事务只读

对于只有读取数据查询的事务，可以指定事务类型为 readonly，即只读事务。

这是一种声明, 用于优化事务性能, 通常用于查询操作, 但不是必须的.

原因:
给方法加上了Transactional注解的话，这个方法执行的所有sql会被放在一个事务中。如果声明了只读事务的话，数据库就会去优化它的执行.

比如:
- 一次执行单条查询, 数据库没必要使用事务支持, 因为默认支持了.
- 一次执行大量的查询, 数据库会使用事务支持, 保证数据的一致性.


## Spring事务的回滚规则

Spring事务的回滚规则有以下几种：
- 默认情况下，只有遇到运行期异常(RuntimeException 的子类）时才会回滚，Error 也会导致事务回滚，但是，在遇到检查型（Checked）异常时不会回滚。
- 通过`@Transactional`注解的`rollbackFor`属性可以指定哪些异常需要回滚。
- 通过`@Transactional`注解的`noRollbackFor`属性可以指定哪些异常不需要回滚。

```java
@Transactional(rollbackFor = {Exception.class})
public void transfer(String outUser, String inUser, Double money) {
    jdbcTemplate.update("update account set money = money - ? where username = ?", money, outUser);
    jdbcTemplate.update("update account set money = money + ? where username = ?", money, inUser);
}
```

## @Transactional注解使用

### 作用范围

- 方法: 推荐用于方法, 但智能用于public方法, 否则不生效.
- 类: 用于类上, 会应用到所有的public方法上.
- 接口: 不推荐在接口上使用.


### 常用配置参数

```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Inherited
@Documented
public @interface Transactional {

  @AliasFor("transactionManager")
  String value() default "";

  @AliasFor("value")
  String transactionManager() default "";

  Propagation propagation() default Propagation.REQUIRED;

  Isolation isolation() default Isolation.DEFAULT;

  int timeout() default TransactionDefinition.TIMEOUT_DEFAULT;

  boolean readOnly() default false;

  Class<? extends Throwable>[] rollbackFor() default {};

  String[] rollbackForClassName() default {};

  Class<? extends Throwable>[] noRollbackFor() default {};

  String[] noRollbackForClassName() default {};

}
```
五个常用配置参数

| 属性名 | 默认值| 说明 |
| -- | -- | -- |
| propagation | Propagation.REQUIRED | 事务的传播行为 |
| isolation | Isolation.DEFAULT | 事务的隔离级别 |
| timeout | TransactionDefinition.TIMEOUT_DEFAULT(-1) | 事务的超时时间 | 
| readOnly | false | 事务的只读属性 |
| rollbackFor | {} | 导致事务回滚的异常类数组 |


### @Transactional注解的实现原理

`@Transactional`注解的实现原理是基于AOP实现的。

AOP 又是使用动态代理实现的。如果目标对象实现了接口，默认情况下会采用 JDK 的动态代理，如果目标对象没有实现了接口,会使用 CGLIB 动态代理。



## Spring AOP 自调用问题


当一个方法被标记了@Transactional 注解的时候，Spring 事务管理器只会在**被其他类方法调用的时候生效**，而不会在同一个类中方法调用生效。


Spring AOP 工作原理决定的。

因为 Spring AOP 使用动态代理来实现事务的管理，它会在运行的时候为带有 @Transactional 注解的方法生成代理对象，并在方法调用的前后应用事物逻辑。如果该方法被其他类调用我们的代理对象就会拦截方法调用并处理事务。

但是在**一个类中的其他方法内部调用的时候，我们代理对象就无法拦截到这个内部调用**，因此事务也就失效了。


MyService 类中的method1()调用method2()就会导致method2()的事务失效。
```java
@Service
public class MyService {

private void method1() {
     method2();
     //......
}
@Transactional
 public void method2() {
     //......
  }
}
```
解决方法:
- 避免同一个类内部调用
- 使用AspectJ取代Spring AOP(因为AspectJ是编译时织入，Spring AOP是运行时织入)
