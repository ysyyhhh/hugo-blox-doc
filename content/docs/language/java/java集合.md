# Java集合体系

Java 集合， 也叫作容器，主要是由两大接口派生而来：一个是 Collection接口，主要用于存放单一元素；另一个是 Map 接口，主要用于存放键值对。对于Collection 接口，下面又有三个主要的子接口：List、Set 和 Queue。

![](img/Java集合/Java集合的结构.png)

List: 有序，可重复
- ArrayList: Object[] 数组, 查询快, 增删慢
- Vector: Object[] 数组, 线程安全(与ArrayList区别)
- LinkedList: 双向链表, 查询慢, 增删快

Set: 元素不可重复
- HashSet: 基于HashMap实现, 无序
- TreeSet: 红黑树(自平衡的二叉查找树), 有序
- LinkedHashSet: 基于LinkedHashMap实现, 是HashSet的子类, 有序

Queue: 有序，可重复, 用于存放队列元素
- PriorityQueue: 优先级队列, Object[] 数组
- DelayQueue: 延迟队列, 用于存放延迟元素
- ArrayDeque: 双端队列, Object[] 数组


Map: 无序，不可重复，键值对
- HashMap: JDK1.8之前是数组+链表, JDK1.8之后是数组+链表/红黑树
- LinkedHashMap: 基于HashMap实现, 有序
- TreeMap: 红黑树(自平衡的二叉查找树), 有序
- HashTable: 数组(主体)+链表(解决哈希冲突), 线程安全

如何选用集合
- 要键值对 - Map
  - 需要排序 - TreeMap
  - 不需要排序 - HashMap
  - 需要线程安全 - HashTable
- 不需要键值对 - Collection
  - 保证元素唯一 - Set
    - 需要排序 - TreeSet
    - 不需要排序 - HashSet
  - 允许重复元素 - List
    - 需要高效的增删 - LinkedList
    - 需要高效的查询 - ArrayList



## List

ArrayList 与 Array比较
- ArrayList是数组的封装，可以动态扩容，而数组是静态的
- ArrayList允许使用泛型

ArrayList 与 Vector比较
- ArrayList是非线程安全的，而Vector是线程安全的
- ArrayList是JDK1.2引入的(主要实现类,新)，而Vector是JDK1.0引入的


ArrayList
- 底层是数组,支持随机访问
- 可以添加null元素
- 插入:
  - 头部插入: O(n)
  - 尾部插入: O(1), 扩容时O(n),每次扩容是原来的1.5倍
  - 指定位置插入: O(n)
- 删除:
  - 只有尾部删除是O(1), 其他都是O(n)


LinkedList
- 底层是双向链表, 不支持随机访问
- 头部和尾部的插入删除都是O(1)
- 一般不使用,作者都不使用



### ArrayList
底层是动态数组

#### 声明arraylist，java语言会做什么操作
A:声明ArrayList时，Java会创建一个长度为0的数组，当第一次添加元素时，会创建一个长度为10的数组，并将元素添加到数组中。当数组长度不够时，会创建一个原数组长度的1.5倍的新数组，并将原数组中的元素复制到新数组中。

#### arraylist什么时候扩容
A:ArrayList在添加元素时，会先判断当前数组的容量是否足够，如果不够则会进行扩容。扩容时，会创建一个原数组长度的1.5倍的新数组，并将原数组中的元素复制到新数组中。

#### arraylist是线程安全的吗
A:ArrayList是非线程安全的，如果需要在多线程环境下使用ArrayList，可以使用Collections.synchronizedList()方法将ArrayList转换为线程安全的List。

#### 线程安全的list有哪些
A:线程安全的List有Vector和Collections.synchronizedList()方法转换的List。Vector是一种线程安全的List实现，而Collections.synchronizedList()方法可以将ArrayList转换为线程安全的List。

### Vector
Vector的底层

为其所有需要保证线程安全的方法都添加了**synchronized关键字**，锁住了整个对象
## Set

对集合进行排序时,需要实现Comparable接口,重写compareTo方法

集合的不可重复性是通过equals方法来判断的, 需要重写equals方法和hashCode方法

#### hashset了解过吗

HashSet是一种基于哈希表的Set实现，其底层实现与HashMap类似，只不过HashSet中存储的是不重复的元素。HashSet中的元素是无序的，不保证元素的插入顺序和遍历顺序一致。

#### 判断某对象是否在set中存在，需要重写哪些方法

为了判断某个对象是否在Set中存在，需要重写该对象的hashCode()和equals()方法。hashCode()方法用于计算对象的哈希值，equals()方法用于比较两个对象是否相等。在重写这两个方法时，需要保证相等的对象具有相同的哈希值，否则会导致Set中出现重复元素。


## Queue

ArrayDeque 和 LinkedList的区别
- 都实现了Deque接口
- ArrayDeque是数组实现的双端队列, 随机访问快, 队列操作慢；LinkedList是双向链表实现的双端队列, 队列操作快
- ArrayDeque不支持null元素, LinkedList支持
- ArrayDeque存在扩容，但均摊快；LinkedList不存在，每次插入需要申请空间，均摊慢。

### PriorityQueue
JDK1.5 引入的

- 底层是堆, 默认是小顶堆, 可以通过传入Comparator来实现大顶堆
- 是插入删除是O(logn)，查顶推是O(1)
- 是非线程安全的，不支持null元素

典型算法题的应用
- 推排序
- 第k大数（不过这个一般用快排O(n)实现）
- 带权图的遍历

### BlockingQueue 阻塞队列

是一个接口，继承于Queue。

阻塞的原因是，支持当队列没用元素时一直阻塞，直到有元素。
如果队列已满，则等到队列有空间时再插入元素。

常用于生产者消费者模型。

## Map**

### HashMap

HashMap 和 HashTable的区别
- HashMap是非线程安全的，而HashTable是线程安全的
- HashMap允许使用null作为键和值，而HashTable不允许
- 效率：HashMap效率高，HashTable效率低
- 容量大小：HashMap默认大小为16，HashTable默认大小为11
- 扩容：HashMap扩容是原来的2倍，HashTable扩容是原来的2倍+1
- 底层数据结构：HashMap是数组+链表/红黑树，HashTable是数组+链表
  - JDK1.8 HashMap在链表长度超过8时，链表会自动转化为红黑树，优化查询速度

HashMap 和 TreeMap的区别
- HashMap是无序的，而TreeMap是有序的

#### HashMap原理

HashMap是一种基于哈希表的Map实现，其底层实现主要包括数组和链表（或红黑树）两部分。数组用来存储哈希桶，链表（或红黑树）用来解决哈希冲突。

数组+链表+红黑树。

那么在jdk1.8的HashMap中，当链表的**长度超过8**时，链表会自动转化为红黑树，优化查询速度。

jdk1.8之前插入链表是头插法，jdk1.8之后是尾插法。

头插法：效率高、满足时间局部性原理

- 但在扩容后可能会导致链表逆序，影响查询效率。
- 扩容时可能会导致死循环（多线程场景下，跟链表逆序有关）


put原理

同时还有一个区别：发生“hash冲突”时，我们上面的做法是“头插法”，这是jdk1.7的做法，而在jdk1.8中，使用的是“尾插法”。

#### hash冲突解决方案

- 开放定址法
  - 线性探测法
  - 二次探测法
  - 伪随机
- 链地址法
  - 相同的hash值的元素，用链表存储
- 再哈希法
  - 提供多个hash函数
- 建立公共溢出区
  - 将哈希表分为基本表和溢出表两部分，凡是和基本表发生冲突的元素，一律填入溢出表。
  - 在查找的时候，先与哈希表的相应位置比较，如果查找成功，则返回。否则去公共溢出区按顺序一一查找。在冲突数据少时性能好，冲突数据多的时候耗时。

#### hashmap底层实现

HashMap是一种基于哈希表的Map实现，其底层实现主要包括数组和链表（或红黑树）两部分。数组用来存储哈希桶，链表（或红黑树）用来解决哈希冲突。

一般情况下，当元素数量超过阈值时便会触发扩容。每次扩容的容量都是之前容量的2倍。

具体来说，HashMap中的每个元素都是一个键值对，其中键和值都可以为null。当向HashMap中添加元素时，首先根据键的哈希值计算出该元素在数组中的位置，如果该位置上已经有元素了，则需要使用链表（或红黑树）来解决哈希冲突。如果链表（或红黑树）中已经存在该键，则更新该键对应的值，否则将该键值对添加到链表（或红黑树）的末尾。

当链表（或红黑树）的长度超过一定阈值时，链表（或红黑树）会被转换为红黑树（或链表），以提高查询效率。当链表（或红黑树）的长度小于等于6时，会使用链表来存储元素，当长度大于6时，会使用红黑树来存储元素。

在HashMap中，数组的长度是2的幂次方，这是为了使哈希值的高位和低位都能够参与到计算中，提高哈希值的均匀性。同时，数组的长度也决定了HashMap中哈希桶的数量，当哈希桶的数量过少时，容易导致哈希冲突，影响查询效率；当哈希桶的数量过多时，会浪费内存空间。因此，在创建HashMap时，需要根据实际情况来选择合适的数组长度。

#### hashmap1.7和1.8区别

HashMap1.7和1.8的主要区别在于底层实现方式的改变。1.7中使用的是数组+链表的方式来解决哈希冲突，而1.8中引入了红黑树来优化链表过长的情况，提高了查询效率。此外，1.8中还引入了一些新的方法和特性，如forEach()方法、Lambda表达式等。

#### hashmap怎么让他线程安全的方法

线程安全的map有哪些

HashMap本身是非线程安全的，如果需要在多线程环境下使用HashMap，可以使用以下几种方法来保证线程安全：

1. 使用Collections.synchronizedMap()方法将HashMap转换为线程安全的Map。
2. 使用ConcurrentHashMap代替HashMap，ConcurrentHashMap是一种线程安全的Map实现。
3. 使用读写锁来保证HashMap的线程安全性，即使用ReentrantReadWriteLock来控制读写操作的并发访问。

### HashTable

Hashtable与Vector类似，都是为每个方法添加了synchronized关键字，来实现的线程安全，锁住了整个对象。Hashtable是一个线程安全的集合,是单线程集合，它给几乎所有public方法都加上了synchronized关键字。

### ConcurrentHashMap

#### ConcurrentHashMap原理**

在 JDK 1.7 中它使用的是数组加链表的形式实现的，而数组又分为：大数组 Segment 和小数组 HashEntry
Segment 本身是基于 ReentrantLock 实现的加锁和释放锁的操作，这样就能保证多个线程同时访问 ConcurrentHashMap 时，同一时间只有一个线程能操作相应的节点，这样就保证了 ConcurrentHashMap 的线程安全了。

分段锁的缺点是：在高并发的情况下，会出现大量线程阻塞，导致性能下降。

JDK1.7之后
使用的是 CAS + volatile 或 synchronized 的方式来保证线程安全的
ConcurrentHashMap 已经摒弃了 Segment 的概念，而是直接用 Node 数组+链表+红黑树的数据结构来实现，并发控制使用 synchronized 和 CAS 来操作。

在 JDK 1.8 中，添加元素时首先会判断
- **容器是否为空，如果为空则使用 volatile 加 CAS 来初始化**。
- 如果容器不为空则根据存储的元素计算该位置是否为空
  - 如果为空则利用 CAS 设置该节点；
  - **如果不为空则使用 synchronize 加锁**，遍历桶中的数据，替换或新增节点到桶中，最后再判断是否需要转为红黑树，这样就能保证并发访问时的线程安全了。

我们把上述流程简化一下，我们可以简单的认为在 JDK 1.8 中，ConcurrentHashMap 是在头节点加锁来保证线程安全的，锁的粒度相比 Segment 来说更小了，发生冲突和加锁的频率降低了，并发操作的性能就提高了。而且 JDK 1.8 使用的是红黑树优化了之前的固定链表，那么当数据量比较大的时候，查询性能也得到了很大的提升，从之前的 O(n) 优化到了 O(logn) 的时间复杂


13、concurrenthashmap最耗时的操作是什么
A: ConcurrentHashMap最耗时的操作是put操作，因为put操作需要保证线程安全，需要进行加锁操作，而加锁操作会影响并发性能。

12、hashtable和concurrenthashmap的区别


线程安全的类有哪些，为什么线程安全




