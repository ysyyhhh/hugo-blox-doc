## Spring事务

### 事务的特性

- 原子性(Atomicity): 事务是一个不可分割的工作单位，事务中的操作要么都发生，要么都不发生。
- 一致性(Consistency): 事务必须使数据库从一个一致性状态变换到另一个一致性状态。
- 隔离性(Isolation): 一个事务的执行不能被其他事务干扰。
- 持久性(Durability): 事务一旦提交，它对数据库中数据的改变是永久性的。

保证AID,C才能被满足

### Spring事务管理

Spring事务管理的方式有两种：
- 编程式事务管理
- 声明式事务管理

#### 编程式事务管理

编程式事务管理是通过编程的方式来管理事务。在编程式事务管理中，需要在代码中显式的调用事务管理的API来管理事务，这种方式将导致业务代码和事务管理代码耦合在一起，不利于事务管理逻辑的重用。

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

#### 声明式事务管理

声明式事务管理是通过配置的方式来管理事务。在声明式事务管理中，只需要在配置文件中声明事务管理的相关属性，就可以在业务代码中实现事务管理，而不需要在业务代码中负责事务管理的代码。

通过AOP来管理事务, 通过`@Transactional`注解来声明事务

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

### Spring事务的传播行为

事务的传播行为是指在多个事务方法相互调用的情况下，事务管理器如何管理事务的传播行为。

当事务方法A调用事务方法B时，Spring事务管理器会根据**事务方法B的传播行为**来决定事务方法B是否加入事务方法A的事务。


Spring事务的传播行为有以下几种：
- PROPAGATION_REQUIRED：最常见的传播行为，如果当前没有事务，就新建一个事务，如果当前存在事务，就加入该事务。
- PROPAGATION_REQUIRES_NEW：新建一个事务，如果当前存在事务，就把当前事务挂起。
- PROPAGATION_NESTED：如果当前存在事务，则在嵌套事务内执行，如果当前没有事务，则新建一个事务。
- PROPAGATION_MANDATORY：强制要求当前方法必须在事务中执行，如果当前没有事务，则抛出异常。

不会发生回滚的情况：
- PROPAGATION_SUPPORTS：支持当前事务，如果当前没有事务，就以非事务方式执行。
- PROPAGATION_NOT_SUPPORTED：以非事务方式执行操作，如果当前存在事务，就把当前事务挂起。
- PROPAGATION_NEVER：以非事务方式执行，如果当前存在事务，则抛出异常。

### Spring事务的隔离级别

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

### Spring事务的回滚规则

Spring事务的回滚规则有以下几种：
- 默认情况下，Spring只会对RuntimeException进行回滚，对于其他异常不会进行回滚。
- 通过`@Transactional`注解的`rollbackFor`属性可以指定哪些异常需要回滚。
- 通过`@Transactional`注解的`noRollbackFor`属性可以指定哪些异常不需要回滚。

```java
@Transactional(rollbackFor = {Exception.class})
public void transfer(String outUser, String inUser, Double money) {
    jdbcTemplate.update("update account set money = money - ? where username = ?", money, outUser);
    jdbcTemplate.update("update account set money = money + ? where username = ?", money, inUser);
}
```

