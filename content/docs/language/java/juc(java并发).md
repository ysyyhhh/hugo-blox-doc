# Java 多线程

## 线程与进程

一个Java程序的运行是一个进程，包括一个main线程和多个其他线程

Java的线程和操作系统的线程的区别
- JDK1.2之前使用的是JVM模拟的用户级线程，JDK1.2之后使用的是操作系统的内核级线程

用户级线程和内核级线程的区别
- 用户线程：由用户空间程序管理和调度的线程，运行在用户空间（专门给应用程序使用）。
- 内核线程：由操作系统内核管理和调度的线程，运行在内核空间（只有内核程序可以访问）。

线程模型是用户线程和内核线程之间的关联方式，常见的线程模型有这三种：
- 一对一（一个用户线程对应一个内核线程）
- 多对一（多个用户线程映射到一个内核线程）
- 多对多（多个用户线程映射到多个内核线程）

Java采用的是一对一的线程模型，即一个用户线程对应一个内核线程。这种线程模型的优点是可以充分利用多核处理器的性能，缺点是创建和销毁线程的开销较大。

JDK21正式引入了虚拟线程


![](img/JUC(Java并发)/Java线程结构.png)


### 为什么程序计数器、虚拟机栈和本地方法栈是线程私有的呢？

程序计数器的功能：
- 记录当前线程执行的字节码指令的地址，从而当线程被切换回来的时候能够知道该线程上次运行到哪儿了。
- 字节码解释器通过改变程序计数器来依次读取指令，从而实现代码的流程控制，如：顺序执行、选择、循环、异常处理。

程序计数器是线程私有的，是为了线程切换时能够正确恢复执行现场。


虚拟机栈
- 每个线程在创建时都会创建一个虚拟机栈，用于存放线程的方法调用栈、局部变量表、操作数栈等信息。（执行的是Java方法）

本地方法栈
- 用于支持本地方法调用，即调用C/C++编写的本地方法。

为了保证**线程的局部变量不被其他线程访问**，虚拟机栈和本地方法栈是线程私有的。

### 为什么堆和方法区是线程共享的呢？

堆：是进程中所有线程共享的内存区域，用于存放对象实例。

方法区：是进程中所有线程共享的内存区域，用于存放类的元数据信息、常量池、静态变量等。

堆和方法区是线程共享的，是为了**方便线程之间共享数据**。

### 并发并行、同步异步

并发：指多个线程交替执行，从宏观上看是同时执行的。

并行：指多个线程同时执行，从微观上看是同时执行的。

同步：指多个线程按照一定的顺序执行。

异步：指多个线程按照不确定的顺序执行。

## 多线程概念

### 为什么要使用多线程？

多线程的主要优点有以下几点：
- 线程间的切换开销小
- 多线程高并发是高并发量的基础
- 现在的CPU都是多核的，多线程可以充分利用CPU的性能

### 多线程带来的问题？

多线程的主要问题有以下几点：
- 线程安全问题
- 死锁问题
- 内存泄漏问题


线程安全：
- 线程安全是指多个线程访问共享资源时不会出现数据不一致的问题。

死锁：
- 死锁是指两个或多个线程互相等待对方释放资源，导致所有线程都无法继续执行的问题。
- 四个条件： 互斥条件、请求与保持条件、不剥夺条件、循环等待条件

内存泄漏：
- 内存泄漏是指程序中的对象无法被垃圾回收器回收，导致内存占用过多的问题。

### 单核上的多线程效率

单核上的多线程效率，取决于线程的类型

- CPU密集型线程：多线程效率不高，因为多个线程会争夺CPU资源，导致线程切换开销大。
- IO密集型线程：多线程效率较高，因为线程在等待IO时会释放CPU资源，不会争夺CPU资源。

### 多线程的实现方式

Java中实现多线程主要有两种方式：

1. 继承Thread类并重写run()方法。
2. 实现Runnable接口并实现run()方法，然后将其作为参数传递给Thread类的构造方法。
3. 实现Callable接口并实现call()方法，然后将其作为参数传递给FutureTask类的构造方法, 最后还是通过Thread来调用

严格来说，这两种都是实现Runnable接口的方式，只不过一种是直接继承Thread类，另一种是将Runnable接口的实现类作为参数传递给Thread类的构造方法。

#### 实现Runnable接口
```java
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("MyRunnable.run()");
    }
}

public class Main {
    public static void main(String[] args) {
        Thread thread = new Thread(new MyRunnable());
        thread.start();
    }
}
```

#### 继承Thread类
```java
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("MyThread.run()");
    }
}

public class Main {
    public static void main(String[] args) {
        MyThread myThread = new MyThread();
        myThread.start();
    }
}
```

#### 实现Callable接口

可以有返回值

```java
public class MyCallable implements Callable<String> {
    @Override
    public String call() throws Exception {
        return "return value";
    }
}

public class Main {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        FutureTask<String> futureTask = new FutureTask<>(new MyCallable());
        Thread thread = new Thread(futureTask);
        thread.start();
        System.out.println(futureTask.get()); //return value
    }
}
```

#### 实现接口 vs 继承类

实现接口的方式更加灵活，因为Java是单继承的，如果继承了Thread类就不能再继承其他类了。

类一般只要求可执行就行, 继承了Thread类, 会有一些额外的方法, 比如start, stop等, 但是一般不会用到.


## 线程的生命周期和状态

线程的生命周期主要包括以下几个状态：
- 新建状态（New）：线程对象被创建后的状态, 还没有调用start()方法。
- 运行状态（Runable）：线程对象调用start()方法后的状态。
- 阻塞状态（Blocking）：需要等待锁被释放
- 无限期等待状态（Waiting）：等待其它线程显式地唤醒
- 超时等待状态 (TIME_WAITING) ：等待一段时间后自动唤醒
- 终止状态（Terminated）：表示该线程已经运行完毕。

![](img/JUC(Java并发)/Java线程状态变化.png)


### 上下文切换

上下文切换是指CPU从一个线程切换到另一个线程时，需要保存当前线程的上下文信息，然后加载另一个线程的上下文信息。

发生上下文切换的原因主要有以下几点：
- 时间片耗尽
- 调用阻塞类型的中断，如请求IO、sleep、wait、join等
- 被终止

上下文切换的开销主要包括以下几个方面：
- 保存和恢复寄存器
- 保存和恢复程序计数器
- 保存和恢复内存映射表

### 线程死锁
四个条件： 互斥条件、请求与保持条件、不剥夺条件、循环等待条件

#### 预防和避免

预防死锁是破坏死锁的后三个条件。
- 破坏请求与保持条件：一次性申请所有资源。
- 破坏不剥夺条件：如果一个线程申请不到资源，就释放已经占有的资源。
- 破坏循环等待条件：按序申请资源。

避免死锁是通过银行家算法来实现的。
- 银行家算法是一种避免死锁的算法，它通过判断系统是否处于安全状态来避免死锁。
- 银行家算法的核心思想是：当一个进程申请资源时，系统会先判断该进程申请资源后系统是否处于安全状态，如果是则分配资源，否则等待。






## JMM

JMM是Java内存模型的缩写，是一种抽象的概念，用于描述Java程序中的内存访问规则。

定义了一个线程之间如何通过内存进行通信的规范，即线程之间如何访问共享内存。

JMM是Java解决多线程并发问题的核心，它定义了一套规范，用于保证多线程环境下的内存可见性、原子性和有序性。

### JMM概念(CPU缓存模型和指令重排序)

#### CPU缓存

CPU 缓存是为了解决 CPU 处理速度和内存处理速度不对等的问题。

![](img/JUC(Java并发)/CPU缓存模型.png)

CPU Cache 的工作方式：
先复制一份数据到 CPU Cache 中，当 CPU 需要用到的时候就可以**直接从 CPU Cache 中读取数据**，当运算完成后，再将运算得到的数据写回 Main Memory 中。

CPU内部缓存不一致的解决 是通过**缓存一致性协议**来解决的。

但同时操作系统也需要解决缓存不一致的问题.(JMM)

#### 指令重排序

指令重排序是指 CPU 和编译器为了提高程序运行效率而对指令序列进行重新排序的一种手段。

指令重排序可以保证串行语义一致，但是没有义务保证多线程间的语义也一致 ，所以在多线程下，指令重排序可能会导致一些问题。

编译器优化重排：
- 编译器（包括 JVM、JIT 编译器等）在不改变单线程程序语义的前提下，重新安排语句的执行顺序。
- 指令并行重排：现代处理器采用了指令级并行技术(Instruction-Level Parallelism，ILP)来将多条指令重叠执行。如果不存在数据依赖性，处理器可以改变语句对应机器指令的执行顺序。
- 内存系统的重排序：处理器使用缓存和读写缓冲区，这使得加载和存储操作看上去可能是在乱序执行。

![](img/JUC(Java并发)/Java源代码经历的重排序.png)


指令重排序可以保证串行语义一致，但是没有义务保证多线程间的语义也一致 ，所以在多线程下，指令重排序可能会导致一些问题。

编译器和处理器的指令重排序的处理方式不一样。对于编译器，通过禁止特定类型的编译器重排序的方式来禁止重排序。

对于处理器，通过插入内存屏障（Memory Barrier，或有时叫做内存栅栏，Memory Fence）的方式来禁止特定类型的处理器重排序。指令并行重排和内存系统重排都属于是处理器级别的指令重排序。
> 内存屏障（Memory Barrier，或有时叫做内存栅栏，Memory Fence）是一种 CPU 指令，用来禁止处理器指令发生重排序（像屏障一样），从而保障指令执行的有序性。另外，为了达到屏障的效果，它也会使处理器写入、读取值之前，将主内存的值写入高速缓存，清空无效队列，从而保障变量的可见性。

#### JMM

JMM是定义了一套规范，用于保证多线程环境下的内存可见性、原子性和有序性。包括:
- 抽象了线程和主内存之间的关系
- 规定了从 Java 源代码到 CPU 可执行指令的这个转化过程要遵守哪些和并发相关的原则和规范

![](img/JUC(Java并发)/JMM(Java内存模型).png)

Java内存区域的区别
JVM 内存结构和 Java 虚拟机的运行时区域相关，定义了 JVM 在运行时如何分区存储程序数据，就比如说堆主要用于存放对象实例。

![](img/JUC(Java并发)/JMM设计思想.png)


### 并发问题的原因

CPU、内存、I/O 设备的速度是有极大差异的，为了合理利用 CPU 的高性能，平衡这三者的速度差异，计算机体系结构、操作系统、编译程序都做出了贡献，同时导致了并发问题。


- CPU 增加了缓存，以均衡与内存的速度差异.
  - 导致可见性问题
  - 可见性是指当多个线程访问共享变量时，一个线程修改了共享变量的值，其他线程**能够看到修改后的值。**
- 操作系统增加了进程、线程，以分时复用 CPU，进而均衡 CPU 与 I/O 设备的速度差异
  - 导致原子性问题
  - 原子性: 是指一个操作是不可中断的，要么全部执行成功，要么全部不执行。
- 编译程序优化指令执行次序，使得缓存能够得到更加合理地利用。
  - 导致有序性问题
  - 有序性：代码的执行顺序按照代码的先后顺序执行。

#### 可见性问题

可见性问题,就是看不到修改后的值, 由CPU缓存导致.

```java

//线程1执行
int a = 0;//1
a = 10;//2

//线程2执行
int j = a//3
```

假设,有两个CPU, CPU1执行线程1, CPU2执行线程2.
线程1执行语句2时, 会先把a=0这个初始值从主内存中加载到CPU1的高速缓存中, 然后在CPU1的高速缓存中赋值a=10, 并没有立即写入到主存.

线程2 如果在 线程1写入主存之前,执行了语句3, 那么就会读取到a=0这个初始值, 而不是修改后的值10.

#### 原子性问题

原子性问题由分时复用CPU导致.


Java中只有对基本数据类型的**读取和赋值**操作是原子性的，其他的操作都不是原子性的。
下面语句1是原子性的, 其他都不是原子性的.
```java
x = 10;        //语句1: 直接将数值10赋值给x，也就是说线程执行这个语句的会直接将数值10写入到工作内存中
y = x;         //语句2: 包含2个操作，它先要去读取x的值，再将x的值写入工作内存，虽然读取x的值以及 将x的值写入工作内存 这2个操作都是原子性操作，但是合起来就不是原子性操作了。
x++;           //语句3： x++包括3个操作：读取x的值，进行加1操作，写入新的值。
x = x + 1;     //语句4： 同语句3
```

因此在执行一些常见,但不是原子性的操作时,会导致原子性问题.

```Java
int i = 1;

// 线程1执行
i += 1;

// 线程2执行
i += 1;
```

i += 1需要三条 CPU 指令

1. 将变量 i 从内存读取到 CPU寄存器；
2. 在CPU寄存器中执行 i + 1 操作；
3. 将最后的结果i写入内存（缓存机制导致可能写入的是 CPU 缓存而不是内存）。

如果线程1执行完1后, 轮到线程2执行三条指令, 线程1再执行2,3. 会导致i最后的值是2而不是3.


#### 有序性问题

在执行程序时，为了提高性能，编译器和处理器会对指令进行重排序。
重排序不会影响单线程程序的执行结果，但是会影响多线程程序的执行结果。

```java
int i = 0;              
boolean flag = false;
i = 1;                //语句1  
flag = true;          //语句2
```
比如语句1和语句2顺序可能会被重排.


### 解决并发问题

第一个角度: Java 内存模型规范了 JVM 如何提供按需禁用缓存和编译优化的方法。

- volatile关键字
- synchronized关键字
- final关键字
- Happens-Before规则

第二个角度,通过可见性原子性有序性三个方面来解决并发问题.

- 原子性问题：通过synchronized关键字和原子类来解决。
  - synchronized关键字可以**保证代码块的原子性**。
  - 原子类可以保证对变量的操作是原子性的。
- 可见性问题：通过volatile关键字来解决。
  - 当一个变量被volatile修饰时，表示它是一个共享变量，能保证修改的值立即更新到主存中.
  - synchronized和lock可以通过同步的方式来解决可见性问题。(即同一时刻只有一个线程获取锁,在释放锁之前会将修改的值刷新到主存中)
- 有序性问题
  - 通过volatile关键字来保证**一定的有序性**。
  - 通过synchronized关键字来保证**有序性**。

### vloatile关键字

#### 作用

作用:
- 保证可见性
- 禁止指令重排

保证可见性
一个变量使用 volatile 修饰，这就指示 编译器，这个变量是共享且不稳定的，每次使用它都到主存中进行读取。

禁止指令重排
将变量声明为 volatile ，在对这个变量进行读写操作的时候，会通过**插入特定的内存屏障** 的方式来禁止指令重排序。

#### TODO: vloatile 实现原理

#### 为什么vloatile不能保证原子性

```java
public class VolatileExample {
    private static volatile int count = 0;

    public static void main(String[] args) {
        ExecutorService executorService = Executors.newCachedThreadPool();
        for (int i = 0; i < 1000; i++) {
            executorService.execute(() -> count++);
        }
        executorService.shutdown();
        System.out.println(count);
    }
}
```

```shell
Exception in thread "main" java.util.concurrent.RejectedExecutionException: Task java.util.concurrent.FutureTask@5e2de80c rejected from java.util.concurrent.ThreadPoolExecutor@3b9a45b3[Terminated, pool size = 0, active threads = 0, queued tasks = 0, completed tasks = 1000]
    at java.util.concurrent.ThreadPoolExecutor$AbortPolicy.rejectedExecution(ThreadPoolExecutor.java:2063)
    at java.util.concurrent.ThreadPoolExecutor.reject(ThreadPoolExecutor.java:830)
    at java.util.concurrent.ThreadPoolExecutor.execute(ThreadPoolExecutor.java:1379)
    at VolatileExample.main(VolatileExample.java:13)
```

volatile不能保证原子性, **因为count++不是原子性的操作**, 它包括三个步骤: 读取count的值, 将count的值加1, 写入count的值.


#### 应用场景

单例模式中的双重检查锁

```java
public class Singleton {
    private static volatile Singleton instance;

    private Singleton() {
    }

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```


### synchronized关键字

见 [synchronized关键字](####synchronized)

### final关键字
所有的final修饰的字段都是编译期常量吗?

如何理解private所修饰的方法是隐式的final?

说说final类型的类如何拓展? 

比如String是final类型，我们想写个MyString复用所有String中方法，同时增加一个新的toMyString()的方法，应该如何做?

final方法可以被重载吗? 

可以父类的final方法能不能够被子类重写? 

不可以说说final域重排序规则?

说说final的原理?

使用 final 的限制条件和局限性?

#### final的基础用法

修饰类
- final类不能有子类
- final类的所有方法都隐式的是final的

修饰方法
- private方法隐式的是final的
- final方法不能被重写
- final方法可以被重载

修饰参数
- final参数不能被修改
- 用于向匿名内部类传递参数

修饰变量
- final修饰的字段**不都是编译期常量**
- 但是final修饰的字段**只能被赋值一次**
```java
public class Test {
    //编译期常量
    final int i = 1;
    final static int J = 1;
    final int[] a = {1,2,3,4};
    //非编译期常量
    Random r = new Random();
    final int k = r.nextInt();

    public static void main(String[] args) {

    }
}
```
如果是 static final 修饰的字段, 就必须是在声明的时候就赋值, 不能在构造方法中赋值, 一定是编译期常量.

blank final
- final修饰的字段, 在声明的时候不赋值, **在构造方法中赋值**, 但是只能赋值一次.

```java
public class Test {
    final int i;
    public Test() {
        i = 1;
    }
}
```

#### TODO: final域重排序


### Happens-Before规则

Happens-Before规则是Java内存模型中的一组规则，用于描述多线程环境下的内存可见性、原子性和有序性。

Happens-Before规则主要包括以下几个规则：

单一线程原则: 一个线程内部, 代码的执行顺序是按照代码的先后顺序执行的.

管程锁定规则: 对同一个锁unlock操作必须先于在lock操作.

volatile变量规则: 对一个volatile变量的写操作必须先于对该变量的读操作

线程启动规则: start()方法调用先于线程的每一个动作.

线程加入(join)规则: Thread对象的终止操作先于join()方法返回.

线程中断规则: 对线程interrupt()方法的调用先于被中断线程的代码检测到中断事件的发生. 即, 可以用interrupt()方法来检测线程是否被中断.

对象终结规则: 对象的构造函数执行结束先于finalize()方法的开始.

传递性: A先于B, B先于C, 那么A先于C.

## 理解线程安全

一个类在可以被多个线程安全调用时就是线程安全的。

线程安全不是一个非真即假的命题，可以将共享数据按照安全程度的强弱顺序分成以下五类: 不可变、绝对线程安全、相对线程安全、线程兼容和线程对立。

### 不可变

不可变(Immutable)的对象一定是线程安全的，不需要再采取任何的线程安全保障措施。
只要一个不可变的对象被正确地构建出来，永远也不会看到它在多个线程之中处于不一致的状态。

多线程环境下，应当尽量使对象成为不可变，来满足线程安全。

不可变的类型:
- final 关键字修饰的基本数据类型
- String
- 枚举类型
- Number 部分子类，如 Long 和 Double 等数值包装类型，BigInteger 和 BigDecimal 等大数据类型。
  - 但同为 Number 的原子类 AtomicInteger 和 AtomicLong 则是可变的

对于集合类型，可以使用 Collections.unmodifiableXXX() 方法来获取一个不可变的集合。

Collections.unmodifiableXXX() 先对原始的集合进行拷贝，需要对集合进行修改的方法都直接抛出异常。

```java
public class ImmutableExample {
    public static void main(String[] args) {
        Map<String, Integer> map = new HashMap<>();
        Map<String, Integer> unmodifiableMap = Collections.unmodifiableMap(map);
        unmodifiableMap.put("a", 1);//抛出异常
    }
}
```

```shell
Exception in thread "main" java.lang.UnsupportedOperationException
    at java.util.Collections$UnmodifiableMap.put(Collections.java:1457)
    at ImmutableExample.main(ImmutableExample.java:9)
```
因为put被直接抛出异常, 所以unmodifiableMap是不可变的.

### 绝对线程安全

不管运行时环境如何，调用者都不需要任何额外的同步措施。

### 相对线程安全

保证对这个对象单独的操作是线程安全的，在调用的时候不需要做额外的保障措施.

但是对于特定复合操作，调用者需要额外的同步措施。

Java的大部分**线程安全类**, 都是这样.

但如在Vector中, 两个线程都在遍历Vector, 一个线程删除了一个元素, 另一个线程可能会访问到一个不存在的元素.
```Java
public class VectorUnsafeExample {
    private static Vector<Integer> vector = new Vector<>();

    public static void main(String[] args) {
        while (true) {
            for (int i = 0; i < 100; i++) {
                vector.add(i);
            }
            ExecutorService executorService = Executors.newCachedThreadPool();
            executorService.execute(() -> {
                for (int i = 0; i < vector.size(); i++) {
                    vector.remove(i);
                }
            });
            executorService.execute(() -> {
                for (int i = 0; i < vector.size(); i++) {
                    vector.get(i);
                }
            });
            executorService.shutdown();
        }
    }
}
```

需要对删除和获取元素操作进行同步.

```Java
executorService.execute(() -> {
    synchronized (vector) {
        for (int i = 0; i < vector.size(); i++) {
            vector.remove(i);
        }
    }
});

executorService.execute(() -> {
    synchronized (vector) {
        for (int i = 0; i < vector.size(); i++) {
            vector.get(i);
        }
    }
});
```


### 线程兼容

线程兼容是指对象本身并不是线程安全的，但是可以通过在调用端使用加锁的方式来保证线程安全。

如ArrayList, HashMap等.

### 线程对立

线程对立是指对象本身并不是线程安全的，而且在调用端使用加锁的方式也无法保证线程安全。

## 线程安全的实现方式

### 互斥同步 synchronized 和 ReentrantLock

互斥同步是指在同一时刻只允许一个线程访问共享资源。

Java中提供了两种互斥同步的方式：synchronized和ReentrantLock。

#### synchronized

synchronized是Java中的关键字，可以用来修饰方法或代码块。

synchronized修饰方法时，表示整个方法是同步的，即同一时刻只允许一个线程访问该方法。

synchronized修饰代码块时，需要**指定一个对象**作为参数，表示对该对象进行同步，即同一时刻只允许一个线程访问该对象。

```java
public class SynchronizedExample {
    public synchronized void method() {
        // 代码
    }
}
```

```java
public class SynchronizedExample {
    public void method() {
        synchronized (this) {
            // 代码
        }
    }
}
```

还可以同步一个类, 两个线程调用同一个类的不同对象上的这种同步语句，也会进行同步。

```java
public class SynchronizedExample {
    public void method() {
        synchronized (SynchronizedExample.class) {
            // 代码
        }
    }
}

public static void main(String[] args) {
    SynchronizedExample e1 = new SynchronizedExample();
    SynchronizedExample e2 = new SynchronizedExample();
    ExecutorService executorService = Executors.newCachedThreadPool();
    executorService.execute(() -> e1.func2());
    executorService.execute(() -> e2.func2());
}
```

同步静态方法, 也是同步类的.

```java
public class SynchronizedExample {
    public static synchronized void method() {
        // 代码
    }
}
```

#### ReentrantLock

ReentrantLock是JUC包中的类，是一种可重入的互斥锁。

ReentrantLock可以替代synchronized进行同步，ReentrantLock可以提供更多的同步操作，如中断、超时、多个条件等。

```java
public class ReentrantLockExample {
    private ReentrantLock lock = new ReentrantLock();

    public void method() {
        lock.lock();
        try {
            // 代码
        } finally {
            lock.unlock();
        }
    }
}

public static void main(String[] args) {
    ReentrantLockExample example = new ReentrantLockExample();
    ExecutorService executorService = Executors.newCachedThreadPool();
    executorService.execute(() -> example.method());
    executorService.execute(() -> example.method());
}
```

#### synchronized 和 ReentrantLock 的区别

- 锁的实现: synchronized是Java的关键字, 是JVM层面的锁, 是隐式的, 不需要用户去手动释放锁; ReentrantLock是JUC包中的类, 是API层面的锁, 是显式的, 需要用户去手动释放锁.
- 性能: synchronized的性能在JDK6之后得到了很大的提升, 但是在并发量很高的情况下, ReentrantLock的性能要优于synchronized.(优化后大致相同)
- 等待可中断: 使用synchronized时, 如果获取不到锁, 线程会一直等待, 不能够中断; 使用ReentrantLock时, 可以设置超时时间, 可以中断.
- 公平锁: ReentrantLock**可以设置为公平锁**, synchronized是非公平锁.
  - 公平锁: 多个线程按照申请锁的顺序来获取锁.
- 锁绑定多个条件: ReentrantLock可以同时绑定多个Condition对象.

如何选择:
除非要使用ReentrantLock的高级功能, 否则优先使用synchronized. 
- 这是因为synchronized是JVM层面的锁, 在JDK6之后进行了很多优化, 所以性能和ReentrantLock差不多, 且更加简洁.
- 并且不用担心忘记释放锁, 也不用担心死锁问题.

### 非阻塞同步

互斥同步的主要问题是阻塞，当一个线程获取锁后，其他线程只能等待。

互斥同步属于一种悲观的并发策略，总是认为只要不去做正确的同步措施，那就肯定会出现问题。无论共享数据是否真的会出现竞争，它都要进行加锁(实际上虚拟机会优化掉一些不必要的加锁操作)。

#### CAS (Compare And Swap)

CAS是一种乐观的并发策略，它总是认为不会出现竞争，只有在真的出现竞争的时候，才通过自旋重试来解决竞争问题。

CAS是基于冲突检测的乐观并发策略.
先进行操作, 如果检测到没有冲突, 则操作成功, 否则不断重试.

CAS的条件是 操作和检查是原子性的. 互斥同步是无法保证的, 只能依靠硬件完成.

CAS指令有三个操作数，分别是内存位置V、旧的预期值A和新值B。CAS指令执行时，当且仅当V的值等于A时，将V的值更新为B，否则不做任何操作。

CAS的实现是C++中的一个原子操作, 但是Java中的CAS是通过JNI来调用C++的CAS指令实现的.


CAS的应用: AtomicInteger 

JUC包中的原子类, 其中的compareAndSet方法和getAndIncrement方法都是基于CAS实现的。

```java
//incrementAndGet方法
public final int incrementAndGet() {
  return unsafe.getAndAddInt(this, valueOffset, 1) + 1;
}

//getAndAddInt方法
public final int getAndAddInt(Object var1, long var2, int var4) {
    int var5;
    do {
        var5 = this.getIntVolatile(var1, var2);
    } while(!this.compareAndSwapInt(var1, var2, var5, var5 + var4));

    return var5;
}
```

#### ABA (CAS的问题)

CAS存在一个问题，即ABA问题。

ABA问题是指一个值原来是A，后来被改成了B，然后又被改回为A，那么CAS检查时会认为它没有被改过，但实际上已经发生了变化。

大部分情况下ABA问题并不会影响并发的正确性.

如果需要解决ABA问题, 用传统的互斥同步会更好.

JUC包中提供了一个带有标记的原子引用类AtomicStampedReference来解决ABA问题。

它可以通过控制变量的版本来保证CAS的正确性。


### 无同步方案

无同步方案是指在多线程环境下，不做任何的同步措施，也不会出现线程安全问题。

核心是: **不共享数据**.

通过将共享数据的访问限制在单线程内部，就可以保证线程安全。

实现方法有: 栈封闭、线程本地存储(Thread Local Storage, TLS)

#### 栈封闭

多个线程访问同一个方法中的局部变量不会出现线程安全问题。

局部变量存在虚拟机栈中，属于线程私有的.

#### 线程本地存储(Thread Local Storage)

当数据必须被多个线程共享时，看看能否将共享数据的代码封装到一个线程内部，这样就可以保证线程安全。

例子: 
- 生产者消费者模式中, 每个线程都有自己的队列, 不会出现线程安全问题.
- Web服务器中, 每个请求都会创建一个线程, 也不会出现线程安全问题.

Java通过ThreadLocal类提供了线程本地存储的支持。


ThreadLocal类可以让每个线程都有自己的共享变量，从而避免了线程安全问题。

```java
public class ThreadLocalExample1 {
    public static void main(String[] args) {
        ThreadLocal threadLocal1 = new ThreadLocal();
        ThreadLocal threadLocal2 = new ThreadLocal();
        Thread thread1 = new Thread(() -> {
            threadLocal1.set(1);
            threadLocal2.set(1);
        });
        Thread thread2 = new Thread(() -> {
            threadLocal1.set(2);
            threadLocal2.set(2);
        });
        thread1.start();
        thread2.start();
    }
}
```
![](img/JUC(Java并发)/ThreadLocalExample1底层结构.png)

每个Thread都有一个ThreadLocalMap对象, 用于存储线程本地变量.

Thread类中定义了ThreadLocal.ThreadLocalMap 成员。
`ThreadLocal.ThreadLocalMap threadLocals = null;`

当调用get set时,先获取当前线程的ThreadLocalMap, 然后将ThreadLocal对象作为key, value作为value存入.

```java
public void set(T value) {
    Thread t = Thread.currentThread();
    ThreadLocalMap map = getMap(t);
    if (map != null)
        map.set(this, value);
    else
        createMap(t, value);
}
```

##### ThreadLocal的问题 -- 内存泄漏

ThreadLocalMap中的Entry的key是弱引用, value是强引用, 如果key被回收了, value不会被回收, 会导致内存泄漏.

解决方法:
在使用完ThreadLocal后, 调用remove方法, 将Entry的key置为null, 这样就可以被回收了.



#### 可重入代码(Reentrant Code)

也叫纯代码, 在代码执行的任何时刻, 都可以被中断, 转而执行另一段代码, 然后再回到原来的代码.

特征: 不依赖于任何共享的变量, 用到的状态变量都有方法的参数传递进来, 不会调用非可重入的方法.

## 线程机制

### 线程基本机制

#### Executor框架

Executor 管理多个异步任务的执行，而无需程序员显式地管理线程的生命周期。这里的异步是指多个任务的执行互不干扰，不需要进行同步操作。



三种Executor:
- CachedThreadPool：一个任务创建一个线程
- FixedThreadPool：所有任务只能使用固定大小的线程
- SingleThreadExecutor：相当于大小为1的FixedThreadPool

```java
public class Main {
    public static void main(String[] args) {
        ExecutorService executorService = Executors.newCachedThreadPool();
        executorService.execute(() -> System.out.println("CachedThreadPool"));
        executorService.shutdown();
    }
}
```

#### Daemon线程(守护线程)

守护线程是一种特殊的线程, 不属于程序中不可或缺的部分，当所有的非守护线程结束时，程序也就终止了，同时会杀死进程中的所有守护线程。

main不是守护线程.

使用setDaemon()方法将线程设置为守护线程。

```java
public class Main {
    public static void main(String[] args) {
        Thread thread = new Thread(() -> {
            while (true) {
                System.out.println("守护线程");
            }
        });
        thread.setDaemon(true);
        thread.start();
    }
}
```

#### sleep()方法

sleep()方法是Thread类的静态方法，可以让当前线程休眠一段时间。 以毫秒为单位。

sleep可能会抛出InterruptedException异常，并且无法跨线程返回给main, 必须在当前线程中处理.

```java
public class Main {
    public static void main(String[] args) {
        Thread thread = new Thread(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("sleep");
        });
        thread.start();
    }
}
```

#### yield()方法

yield()方法是Thread类的静态方法.
表示该线程已经执行完了重要的部分, 可以让当前线程让出CPU，但是不代表当前线程不执行了，只是让出CPU，让CPU重新调度。

是对线程调度器的一种建议，而不是命令。

```java
public class Main {
    public static void main(String[] args) {
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 100; i++) {
                System.out.println("thread1");
                Thread.yield();
            }
        });
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 100; i++) {
                System.out.println("thread2");
                Thread.yield();
            }
        });
        thread1.start();
        thread2.start();
    }
}
```

### 线程中断

#### Interrupt()方法

InterruptedException是一个检查异常

当一个线程调用一个阻塞方法时，比如sleep()、wait()、join()等，

如果其他线程调用了该线程的interrupt()方法，那么该线程会抛出InterruptedException异常。

```java

public class Main {
    public static void main(String[] args) {
        Thread thread = new Thread(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        thread.start();
        thread.interrupt();
    }
}
```

如果一个线程的 run() 方法执行一个无限循环，并且没有执行 sleep() 等会抛出 InterruptedException 的操作，那么调用线程的 interrupt() 方法就无法使线程提前结束

但调用线程的 interrupt() 方法会设置线程的中断标志，可以通过 Thread.interrupted() 方法来判断线程是否被中断。

```java
public class Main {
    public static void main(String[] args) {
        Thread thread = new Thread(() -> {
            while (!Thread.interrupted()) {
                System.out.println("running");
            }
        });
        thread.start();
        thread.interrupt();
    }
}
```

#### Executor框架中的中断

Executor框架中的线程池提供了shutdown()和shutdownNow()方法来关闭线程池。

shutdown()会等待所有线程执行完毕后再关闭，而shutdownNow()会立即关闭所有线程(相当于调用每个线程的interrupt()方法)。
```java
public class Main {
    public static void main(String[] args) {
        ExecutorService executorService = Executors.newCachedThreadPool();
        executorService.execute(() -> {
            while (true) {
                System.out.println("running");
            }
        });
        executorService.shutdownNow();
    }
}
```

如果只是想中断一个线程，可以使用submit()方法提交一个Callable任务，然后调用返回的Future对象的cancel()方法来中断线程。

```java
public class Main {
    public static void main(String[] args) {
        ExecutorService executorService = Executors.newCachedThreadPool();
        Future<?> future = executorService.submit(() -> {
            while (true) {
                System.out.println("running");
            }
        });
        future.cancel(true);
    }
}
```

### 线程之间的协作


#### Join方法

join()方法是Thread类的一个实例方法，用于等待调用join()方法的线程执行完毕。

```java
public class Main {
    public static void main(String[] args) {
        Thread thread = new Thread(() -> {
            System.out.println("thread");
        });
        thread.start();
        try {
            thread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("main");
    }
}
```


#### 查看线程的执行结果，怎么拿到

可以通过线程的join()方法来等待线程执行完毕，并获取线程的执行结果。join()方法会阻塞当前线程，直到被调用的线程执行完毕。

另外，可以通过线程的返回值来获取线程的执行结果。如果线程需要返回结果，可以在run()方法中返回一个值，然后在调用线程的地方通过Thread对象的get()方法获取返回值。


#### wait()和notify()方法

wait()和notify()方法是Object类的实例方法，用于线程之间的协作。

wait()方法会使当前线程等待，直到其他线程调用对象的notify()或notifyAll()方法来唤醒该线程。

只能在同步方法或同步块中调用wait()和notify()方法。

wait会释放锁

```java
public class Main {
    public static void main(String[] args) {
        Object object = new Object();
        Thread thread1 = new Thread(() -> {
            synchronized (object) {
                try {
                    object.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("thread1");
            }
        });
        Thread thread2 = new Thread(() -> {
            synchronized (object) {
                object.notify();
                System.out.println("thread2");
            }
        });
        thread1.start();
        thread2.start();
    }
}
```

#### sleep()方法和wait()方法

- sleep()方法
  - Thread类的静态方法，可以让当前线程休眠一段时间
  - **不会释放锁**。
  - 用于暂停执行
- wait()方法
  - Object类的方法，可以让当前线程等待
  - 会释放锁。
  - wait()调用后, 线程不会自动唤醒, 需要调用notify()或notifyAll()方法唤醒。
    - 或者使用wait(long timeout)方法，指定等待时间后自动唤醒。
  - 用于线程间的通信


##### 为什么wait()不定义在Thread类中呢？

wait()方法是Object类的方法，是让获得对象锁的线程实现等待，会自动释放当前线程占有的对象锁。

每个Object都有对象锁，因此定义在Object类中。

##### 为什么sleep()不定义在Object类中呢？

sleep()方法是Thread类的静态方法，是让当前线程暂停执行，不涉及到对象类，也不需要获得对象锁。

#### await()和signal()方法 (Condition)

JUC包中的Condition接口提供了Condition对象来实现线程之间的协作。

在Condition上调用await()方法会使当前线程等待，直到其他线程调用Condition的signal()方法 或 signalAll()方法来唤醒该线程。


相比于wait() , await可以指定等待的条件. 

使用Lock对象的newCondition()方法来获取Condition对象。

```java
public class AwaitSignalExample {
    private Lock lock = new ReentrantLock();
    private Condition condition = lock.newCondition();

    public void before() {
        lock.lock();
        try {
            System.out.println("before");
            condition.signalAll();
        } finally {
            lock.unlock();
        }
    }

    public void after() {
        lock.lock();
        try {
            condition.await();
            System.out.println("after");
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }
}
```

### 可以直接调用run()方法吗？

可以直接调用run()方法，但是这样会导致run()方法在当前线程（main线程）中执行，不会创建新的线程。

正常情况是调用start()方法，然后由JVM来创建新的线程并执行run()方法。

调用 start() 方法方可启动线程并使线程进入就绪状态，直接执行 run() 方法的话不会以多线程的方式执行。


## 锁

![](img/JUC(Java并发)/Java主流锁.png)

### 乐观锁与悲观锁

对于同一个数据的并发操作:
- 悲观锁认为对于同一个数据的并发操作，一定是会发生冲突的，因此在数据被操作时会加锁。
  - synchronized lock
- 乐观锁认为对于同一个数据的并发操作，是不会发生冲突的，所以不会加锁，只是在更新数据时会判断在此期间数据有没有被其他线程更新。 
  - CAS

![](img/JUC(Java并发)/乐观锁和悲观锁.png)

悲观锁适用于写操作多的场景，乐观锁适用于读操作多的场景。


### 自旋锁与自适应自旋

自旋锁出现的原因:
阻塞或唤醒一个线程都需要从用户态转换到内核态，这个转换过程需要耗费时间, 可能比线程自旋的时间还要长.

而在很多场景中, 同步资源的锁定时间都是非常短的, 如果线程被阻塞的时间比同步资源的锁定时间还要长, 那么线程就会白白浪费CPU资源.

所以可以让当前线程"忙等", 不停地循环等待, 直到获取到锁.

缺点:
- 不能代替阻塞,会消耗CPU资源

因此当自旋时间过长时, 可以将线程挂起, 等待一段时间后再自旋.


自适应自旋:
- 自旋的时间不再是固定的, 而是由前一次在同一个锁上的自旋时间及锁的拥有者的状态来决定的.
- 如果前一次自旋成功, 说明锁的拥有者很快就会释放锁, 那么这一次自旋的时间会更长.
- 如果前一次自旋不成功, 说明锁的拥有者不会很快释放锁, 那么这一次自旋的时间会更短.



### 无锁 vs 偏向锁 vs 轻量级锁 vs 重量级锁


- 偏向锁通过对比Mark Word解决加锁问题，避免执行CAS操作。
- 轻量级锁是通过用CAS操作和自旋来解决加锁问题，避免线程阻塞和唤醒而影响性能。
- 重量级锁是将除了拥有锁的线程以外的线程都阻塞。

### 公平锁和非公平锁

公平锁是指多个线程按照申请锁的顺序来获取锁。

非公平锁是指多个线程获取锁的顺序并不是按照申请锁的顺序，有可能后申请锁的线程比先申请锁的线程优先获取锁。

公平锁的实现成本较高，性能相对非公平锁要低，因为需要先判断队列中是否有其他线程等待，而非公平锁只需要判断锁是否被占用。

![](img/JUC(Java并发)/公平锁和非公平锁.png)


### 可重入锁 vs 非可重入锁

可重入锁是指同一个线程在外层方法获取锁的时候，内层方法可以直接获取该锁。又叫递归锁。

非可重入锁是指锁不可以延续使用，不可以重复获取。

可重入锁可以避免死锁

Java中的synchronized和ReentrantLock都是可重入锁。

```java
public class ReentrantLockExample {
    private ReentrantLock lock = new ReentrantLock();

    public void func() {
        lock.lock();
        try {
            for (int i = 0; i < 3; i++) {
                System.out.println(i);
                if (i == 1) {
                    func();
                }
            }
        } finally {
            lock.unlock();
        }
    }
}
```

![](img/JUC(Java并发)/可重入锁.png)

![](img/JUC(Java并发)/不可重入锁.png)

![](img/JUC(Java并发)/可重入锁和不可重入锁原理.png)

### 共享锁和排他锁

共享锁是读锁，排他锁是写锁。

![](img/JUC(Java并发)/ReentrantReadWriteLock.png)



## 线程池

### 线程池概念

线程池提供了一种限制和管理资源（包括执行一个任务）的方式。 每个线程池还维护一些基本统计信息，例如已完成任务的数量。

好处:
- 降低资源消耗: 通过重复利用已创建的线程降低线程创建和销毁造成的消耗。
- 提高响应速度: 当任务到达时，任务可以不需要等到线程创建就能立即执行。
- 提高线程的可管理性: 线程是稀缺资源，如果无限制地创建，不仅会消耗系统资源，还会降低系统的稳定性，使用线程池可以进行统一分配、调优和监控。



### 创建线程池
1. 通过ThreadPoolExecutor构造函数创建
2. 通过Executors工厂方法创建


### 为什么不推荐使用内置线程池

《阿里巴巴 Java 开发手册》中

- 线程资源必须通过线程池提供，不允许在应用中自行显式创建线程。
- 强制线程池不允许使用 Executors 去创建，而是通过 ThreadPoolExecutor 构造函数的方式，这样的处理方式让写的同学更加明确线程池的运行规则，规避资源耗尽的风险

#### 有哪些实现好的线程池，既然他们不推荐，为什么Java官方还要给你

Java中提供了多种线程池实现，包括ThreadPoolExecutor、ScheduledThreadPoolExecutor、ForkJoinPool等。这些线程池实现都是经过优化和测试的，可以满足大部分场景的需求。

虽然Java官方不推荐直接使用这些线程池实现，但是它们提供了一种可靠、高效的线程池实现，可以作为开发者自己实现线程池的参考。


### Executors工厂方法创建线程池

#### FixedThreadPool

该方法返回一个固定数量的线程池，该线程池中的线程数量始终不变。

当有一个新的任务提交时，线程池中若有空闲线程，则立即执行。若没有，则新的任务会被暂存在一个任务队列中，待有线程空闲时，便处理在任务队列中的任务。

弊端：
使用的是无界的LinkedBlockingQueue，可能会堆积大量的请求，从而导致OOM。

#### SingleThreadExecutor

该方法返回一个只有一个线程的线程池，若多余一个任务被提交到该线程池，任务会被保存在一个任务队列中，待线程空闲，按先入先出的顺序执行队列中的任务。

弊端同FixedThreadPool

#### CachedThreadPool

该方法返回一个可根据实际情况调整线程数量的线程池。线程池的线程数量不确定，但若有空闲线程可以复用，则会优先使用可复用的线程。

弊端：
使用的是SynchronousQueue，允许创建的线程数量为Integer.MAX_VALUE，可能会创建大量的线程，从而导致OOM。

#### ScheduledThreadPool

该方法返回一个固定数量的线程池，而且该线程池可以延迟或定时的执行任务。

弊端：
使用的是无界的DelayedWorkQueue，队列最大长度为Integer.MAX_VALUE，可能会堆积大量的请求，从而导致OOM。



1个10G大小文件，如何得前100个最大数字
\


### 线程池饱和策略

AbortPolicy：直接抛出RejectedExecutionException异常。
CallerRunsPolicy：将任务交给调用线程来执行。
DiscardPolicy：直接丢弃任务，不做任何处理。


### 线程池参数

最重要的三个
- corePoolSize：核心线程数，即线程池中保留的线程数。
- maximumPoolSize：最大线程数，即线程池中允许的最大线程数。
- workQueue：任务队列，用于存储等待执行的任务。

- keepAliveTime：线程空闲时间，即当线程池中的线程空闲时间超过该值时，多余的线程会被销毁。
- unit：时间单位，用于指定keepAliveTime的时间单位。
- threadFactory：线程工厂，用于创建新的线程。
- handler：拒绝策略，用于处理无法处理的任务。


### 线程池常用的阻塞队列

新任务到来时，如果线程数量达到了corePoolSize，就将任务加入workQueue中.

不同的阻塞队列对线程池的运行状态有不同的影响。

- ArrayBlockingQueue：基于数组的有界阻塞队列，按FIFO排序任务。
- LinkedBlockingQueue：基于链表的有界阻塞队列，按FIFO排序任务。
- SynchronousQueue：不存储元素的阻塞队列，每个插入操作必须等到另一个线程调用移除操作，否则插入操作一直处于阻塞状态。
- DelayQueue：基于优先级的延迟阻塞队列，按元素的延迟时间排序。

### 线程池的工作流程

![](img/JUC(Java并发)/线程池实现原理.png)

新任务来了
1. 如果线程池中的线程数量小于corePoolSize，就创建新的线程来执行任务。
2. 如果线程池中的线程数量等于或大于corePoolSize，且小于maximumPoolSize，就将任务加入workQueue中。
3. 如果workQueue已满，且线程数量小于maximumPoolSize，就创建新的线程来执行任务。
4. 如果workQueue已满，且线程数量等于或大于maximumPoolSize，就执行拒绝策略。

### 如何动态修改线程池参数

对 corePoolSize、maximumPoolSize、keepAliveTime 进行修改，可以通过 ThreadPoolExecutor 的 setCorePoolSize、setMaximumPoolSize、setKeepAliveTime 方法进行修改。

因为这三个参数基本决定了线程池的基本行为，修改这三个参数后，线程池会重新调整线程数量。

### 如何设计根据任务优先级执行的线程池

可以使用 PriorityBlockingQueue 来存储任务，然后自定义任务类实现 Comparable 接口，根据优先级来排序。


### 如何解决OOM

OOM：OutOfMemoryError
在使用线程池时，可能会因为线程池中的线程数量过多，导致内存溢出。

解决方法：
- 通过调整线程池的参数，如 corePoolSize、maximumPoolSize、keepAliveTime 等。
- 通过使用有界的阻塞队列，如 ArrayBlockingQueue、LinkedBlockingQueue 等。
- 通过使用拒绝策略，如 AbortPolicy、CallerRunsPolicy、DiscardPolicy、DiscardOldestPolicy 等。
- 重写入队方法，实现自定义的拒绝策略。



## Future

Future接口是Java5中引入的，它用来表示异步计算的结果。

是异步思想的体现，主要用于在一些耗时的操作中，先提交任务，然后去做其他的事情，等到任务完成后再来获取结果。

Future模式看作是一种特殊的设计模式，思想是异步调用。

Java中Future类是一个接口，它的实现类是FutureTask。

```java
// V 代表了Future执行的任务返回值的类型
public interface Future<V> {
    // 取消任务执行
    // 成功取消返回 true，否则返回 false
    boolean cancel(boolean mayInterruptIfRunning);
    // 判断任务是否被取消
    boolean isCancelled();
    // 判断任务是否已经执行完成
    boolean isDone();
    // 获取任务执行结果
    V get() throws InterruptedException, ExecutionException;
    // 指定时间内没有返回计算结果就抛出 TimeOutException 异常
    V get(long timeout, TimeUnit unit)

        throws InterruptedException, ExecutionException, TimeoutException;
}
```

### FutureTask

FutureTask是Future的一个实现类，它实现了Runnable接口，所以它可以被线程执行。

FutureTask可以用来包装Callable或Runnable对象。

```java
public class FutureTask<V> implements RunnableFuture<V> {
    
    // 有两个构造函数

    // 1. 传入Callable对象
    public FutureTask(Callable<V> callable) {
        if (callable == null)
            throw new NullPointerException();
        this.callable = callable;
        this.state = NEW;       // ensure visibility of callable
    }

    // 2. 传入Runnable对象和返回值
    public FutureTask(Runnable runnable, V result) {
        this.callable = Executors.callable(runnable, result);
        this.state = NEW;       // ensure visibility of callable
    }

}
```


CompletableFuture是Java8中引入的一个类，它实现了Future和CompletionStage接口，可以用来表示一个异步计算的结果。

解决了Future的局限性: 不支持组合、不支持异常处理、不支持回调机制。

```java
public class CompletableFuture<T> implements Future<T>, CompletionStage<T> {
}
```


## TODO: AQS

AQS是AbstractQueuedSynchronizer的缩写，它是一个用来构建锁和同步器的框架。

AQS是JUC包中的一个重要类，它是用来构建锁和同步器的框架。

### AQS的设计思想

AQS的设计思想是
- 如果被请求的资源空闲，那么就将当前请求资源的线程设置为有效的工作线程，并且将共享资源设置为锁定状态。
- 如果被请求的资源被占用，那么就需要一套线程阻塞等待以及被唤醒时锁分配的机制，这个机制AQS是用CLH队列锁实现的，即将暂时获取不到锁的线程加入到队列中。

CLH队列是一个虚拟的双向队列（虚拟的双向队列即不存在队列实例，仅存在结点之间的关联关系），它将所有申请同步状态的线程封装成一个队列。

![](img/JUC(Java并发)/CLH队列结构.png)


### AQS的实现原理




## JUC工具类

