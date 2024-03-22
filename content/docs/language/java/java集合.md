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
- Hashtable: 数组(主体)+链表(解决哈希冲突), 线程安全

如何选用集合
- 要键值对 - Map
  - 需要排序 - TreeMap
  - 不需要排序 - HashMap
  - 需要线程安全 - Hashtable
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

是一个接口，继承于Qeueu。

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

put原理

同时还有一个区别：发生“hash冲突”时，我们上面的做法是“头插法”，这是jdk1.7的做法，而在jdk1.8中，使用的是“尾插法”。

#### hashmap底层实现

HashMap是一种基于哈希表的Map实现，其底层实现主要包括数组和链表（或红黑树）两部分。数组用来存储哈希桶，链表（或红黑树）用来解决哈希冲突。

一般情况下，当元素数量超过阈值时便会触发扩容。每次扩容的容量都是之前容量的2倍。

具体来说，HashMap中的每个元素都是一个键值对，其中键和值都可以为null。当向HashMap中添加元素时，首先根据键的哈希值计算出该元素在数组中的位置，如果该位置上已经有元素了，则需要使用链表（或红黑树）来解决哈希冲突。如果链表（或红黑树）中已经存在该键，则更新该键对应的值，否则将该键值对添加到链表（或红黑树）的末尾。

当链表（或红黑树）的长度超过一定阈值时，链表（或红黑树）会被转换为红黑树（或链表），以提高查询效率。当链表（或红黑树）的长度小于等于6时，会使用链表来存储元素，当长度大于6时，会使用红黑树来存储元素。

在HashMap中，数组的长度是2的幂次方，这是为了使哈希值的高位和低位都能够参与到计算中，提高哈希值的均匀性。同时，数组的长度也决定了HashMap中哈希桶的数量，当哈希桶的数量过少时，容易导致哈希冲突，影响查询效率；当哈希桶的数量过多时，会浪费内存空间。因此，在创建HashMap时，需要根据实际情况来选择合适的数组长度。

#### hashmap1.7和1.8区别

HashMap1.7和1.8的主要区别在于底层实现方式的改变。1.7中使用的是数组+链表的方式来解决哈希冲突，而1.8中引入了红黑树来优化链表过长的情况，提高了查询效率。此外，1.8中还引入了一些新的方法和特性，如forEach()方法、Lambda表达式等。

#### hashmap怎么让他线程安全的方法

HashMap本身是非线程安全的，如果需要在多线程环境下使用HashMap，可以使用以下几种方法来保证线程安全：

1. 使用Collections.synchronizedMap()方法将HashMap转换为线程安全的Map。
2. 使用ConcurrentHashMap代替HashMap，ConcurrentHashMap是一种线程安全的Map实现。
3. 使用读写锁来保证HashMap的线程安全性，即使用ReentrantReadWriteLock来控制读写操作的并发访问。


### ConcurrentHashMap

#### ConcurrentHashMap原理

ConcurrentHashMap 已经摒弃了 Segment 的概念，而是直接用 Node 数组+链表+红黑树的数据结构来实现，并发控制使用 synchronized 和 CAS 来操作。


红黑树可用别的数据结构代替吗

跳表与红黑树比较

线程安全的类有哪些，为什么线程安全







