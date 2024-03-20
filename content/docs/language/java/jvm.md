# JVM

![](img/JVM/系统结构.png)

## TODO: 类字节码

JVM上运行的是字节码，而不是源代码。
字节码是一种中间代码，它是一种介于源代码和机器码之间的代码。字节码是由Java编译器编译生成的，它是一种与平台无关的代码，可以在任何支持Java虚拟机的平台上运行。

JVM不仅支持Java语言，还支持其他语言，如Groovy、Kotlin、Scala等。这些语言都可以编译成字节码，然后在JVM上运行。


### 字节码文件

字节码文件是以.class为扩展名的文件，它包含了Java源代码编译生成的字节码。
字节码文件是一种二进制文件以8位字节为单位存储的，它包含了类的结构信息、字段信息、方法信息、接口信息等。

class文件采用伪结构来存储, 有两种类型: 无符号数和表。

无符号数: 占两个字节, 用于描述数字, 例如: u1, u2, u4, u8

表: 由多个无符号数或其他表构成, 用于描述有层次关系的复合结构, 例如: 字段表, 方法表, 属性表

![](img/JVM/class文件结构.png)

### 字节码增强技术

字节码增强技术是指在编译后的字节码文件中插入新的字节码，从而增强程序的功能。字节码增强技术可以用于实现AOP（Aspect-Oriented Programming）编程、动态代理、代码注入等功能。



## 类加载机制

### 类的生命周期

类的生命周期包括：加载、验证、准备、解析、初始化、使用和卸载。

类加载的过程包括了: 加载、验证、准备、解析、初始化。

其中解析的过程是可选的，可以在初始化阶段之后再进行。
- 为了支持动态绑定

其余阶段按顺序开始,但是不一定按顺序结束.

### 类的加载

类的加载是指将类的字节码文件加载到内存中，并创建一个Class对象，用于表示该类。

在加载阶段,虚拟机需要完成:
- 通过类的全限定名获取类的二进制字节流
- 将字节流代表的静态存储结构转化为方法区的运行时数据结构
- 在内存中生成一个代表这个类的java.lang.Class对象,作为方法区这个类的各种数据的访问入口

![](img/JVM/类的加载.png)

类加载器不需要等到"首次使用"时才加载类,而是在预料到类会被使用时就加载类. 如果在加载类的过程中遇到了错误,类加载器必须抛出异常,通知调用者类加载失败.

加载class文件的方式:
- 从本地系统中直接加载
- 通过网络下载.class文件
- 从zip,jar等归档文件中加载
- 从数据库中读取.class文件
- 将Java源文件动态编译为.class文件

### 连接

连接阶段包括了验证、准备和解析。

#### 验证

验证是确保加载的类符合JVM规范的过程。验证阶段的目的是确保被加载的类是合法、合理的，不会危害虚拟机的安全。

验证阶段主要包括了四个方面的验证：
- 文件格式验证：验证字节码文件是否符合JVM规范。
- 元数据验证：验证字节码文件中的类、字段、方法等信息是否符合JVM规范。
- 字节码验证：验证字节码文件中的字节码是否符合JVM规范。
- 符号引用验证：验证字节码文件中的符号引用是否符合JVM规范。

#### 准备

准备阶段是为类的**静态变量分配内存并设置初始值**的过程。这些变量所使用的内存都将在方法区中进行分配.
- 不包括实例变量,实例变量会在对象实例化时随着对象一起分配在Java堆中
- 初始值是默认的零值,例如: 0, null

#### 解析

解析阶段是将**常量池中的符号引用替换为直接引用**的过程。解析阶段是可选的，可以在初始化阶段之后再进行。

解析针对类或接口,字段,类方法,接口方法,方法类型,方法句柄,方法调用点限定符,动态调用点限定符这几类符号引用进行.

#### 初始化

初始化是为类的静态变量赋予正确的初始值的过程。

对类变量进行初始值设定有两种方式:
- 声明变量时指定初始值
- 使用静态初始化块

JVM初始化步骤
- 如果这个类还没有被加载和连接,则先进行加载和连接
- 如果类的直接父类还没有被初始化,则先初始化其直接父类
- 如果类中有初始化语句,则依次执行这些初始化语句

类的初始化动机: 只有对类的主动使用才会导致类的初始化,主动使用包括:
- 创建类的实例, new
- 访问类的静态变量,或者为静态变量赋值
- 调用类的静态方法
- 反射,例如: Class.forName("com.example.Test")
- 初始化一个类的子类
- Java虚拟机启动时被标明为启动类的类,即main方法所在的类


#### 使用

类访问方法区的数据,执行程序代码,调用方法等.

对象是在堆中分配的,对象的实例变量也在堆中分配,但是对象的引用是在栈中分配的.

#### 卸载

JVM结束声明周期的情况:
- 执行了System.exit()方法
- 程序正常结束
- 程序异常结束
- 由于操作系统错误导致JVM进程终止

### 类加载器

类加载器是用于加载类的对象，它负责将类的字节码文件加载到内存中，并创建一个Class对象，用于表示该类。

分为三种:
- 启动类加载器: Bootstrap ClassLoader
  - 负责加载JRE/lib下, 或 -Xbootclasspath选项指定的路径中的核心类库
  - 由C++实现,不是Java类
- 扩展类加载器: Extension ClassLoader
  - 负责加载JRE/lib/ext目录下的扩展类库,如javax.*开头的类
  - 由Java实现,是sun.misc.Launcher$ExtClassLoader类
  - 开发者可以直接使用扩展类加载器
- 应用程序类加载器: Application ClassLoader
  - 负责加载用户类路径上的类库
  - 由Java实现,是sun.misc.Launcher$AppClassLoader类
  - 开发者可以直接使用应用程序类加载器

应用程序都是由这三种类加载器互相配合进行加载的，如果有必要，我们还可以加入自定义的类加载器
因为JVM自带的ClassLoader只是懂得从本地文件系统加载标准的java class文件，因此如果编写了自己的ClassLoader，便可以做到如下几点:
- 在执行非置信代码之前，自动验证数字签名。
- 动态地创建符合用户特定需要的定制化构建类。
- 从特定的场所取得java class，例如数据库中和网络中。


#### 寻找类加载器

类加载器的寻找顺序是: 启动类加载器 -> 扩展类加载器 -> 应用程序类加载器

```java
package com.pdai.jvm.classloader;
public class ClassLoaderTest {
     public static void main(String[] args) {
        ClassLoader loader = Thread.currentThread().getContextClassLoader();
        System.out.println(loader);
        System.out.println(loader.getParent());
        System.out.println(loader.getParent().getParent());
    }
}
```

### 类的加载

类的加载有三种方式:
- 命令行启动应用时候由JVM初始化加载
- 通过Class.forName()方法动态加载
- 通过ClassLoader.loadClass()方法动态加载

### JVM类加载机制

JVM类加载机制是指JVM在加载类的过程中所采取的策略和步骤。

全盘负责: 一个类加载器负责加载一个类,如果一个类加载器加载了一个类,那么这个类所依赖的和引用的类也由这个类加载器负责加载.

父类委托: 一个类加载器在加载类时,先委托给其父类加载器加载,如果父类加载器无法加载,则自己加载.

缓存机制: 保证所有加载过的类都会被缓存,当程序中需要使用某个类时,类加载器会先从缓存中搜索这个类,只有当缓存中不存在这个类时,类加载器才会去加载这个类.

### 类加载器的双亲委派模型

双亲委派模型是指类加载器在加载类时，会先委托给其父类加载器加载，只有在父类加载器无法加载时，才会自己加载。

1. 当AppClassLoader加载一个类时,它首先不会自己去尝试加载这个类,而是把类加载请求委派给父类加载器ExtClassLoader去完成
2. 当ExtClassLoader加载一个类时,它首先不会自己去尝试加载这个类,而是把类加载请求委派给BootstrapClassLoader去完成
3. 如果BootstrapClassLoader加载失败(在rt.jar中找不到所需类),会把类加载请求委派给ExtClassLoader
4. 如果ExtClassLoader加载失败(在jre/lib/ext中找不到所需类),会把类加载请求委派给AppClassLoader
5. 如果AppClassLoader加载失败(在用户类路径下找不到所需类),会抛出ClassNotFoundException

```java
public Class<?> loadClass(String name)throws ClassNotFoundException {
            return loadClass(name, false);
    }
    protected synchronized Class<?> loadClass(String name, boolean resolve)throws ClassNotFoundException {
            // 首先判断该类型是否已经被加载
            Class c = findLoadedClass(name);
            if (c == null) {
                //如果没有被加载，就委托给父类加载或者委派给启动类加载器加载
                try {
                    if (parent != null) {
                         //如果存在父类加载器，就委派给父类加载器加载
                        c = parent.loadClass(name, false);
                    } else {
                    //如果不存在父类加载器，就检查是否是由启动类加载器加载的类，通过调用本地方法native Class findBootstrapClass(String name)
                        c = findBootstrapClass0(name);
                    }
                } catch (ClassNotFoundException e) {
                 // 如果父类加载器和启动类加载器都不能完成加载任务，才调用自身的加载功能
                    c = findClass(name);
                }
            }
            if (resolve) {
                resolveClass(c);
            }
            return c;
        }
```

优势:
- 避免类的重复加载, 防止内存中出现多份同样的字节码
- 保护程序安全, 防止核心API被随意篡改

### 自定义类加载器

```java
package com.pdai.jvm.classloader;
import java.io.*;

public class MyClassLoader extends ClassLoader {

    private String root;

    protected Class<?> findClass(String name) throws ClassNotFoundException {
        byte[] classData = loadClassData(name);
        if (classData == null) {
            throw new ClassNotFoundException();
        } else {
            return defineClass(name, classData, 0, classData.length);
        }
    }

    private byte[] loadClassData(String className) {
        String fileName = root + File.separatorChar
                + className.replace('.', File.separatorChar) + ".class";
        try {
            InputStream ins = new FileInputStream(fileName);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            int bufferSize = 1024;
            byte[] buffer = new byte[bufferSize];
            int length = 0;
            while ((length = ins.read(buffer)) != -1) {
                baos.write(buffer, 0, length);
            }
            return baos.toByteArray();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public String getRoot() {
        return root;
    }

    public void setRoot(String root) {
        this.root = root;
    }

    public static void main(String[] args)  {

        MyClassLoader classLoader = new MyClassLoader();
        classLoader.setRoot("D:\\temp");

        Class<?> testClass = null;
        try {
            testClass = classLoader.loadClass("com.pdai.jvm.classloader.Test2");
            Object object = testClass.newInstance();
            System.out.println(object.getClass().getClassLoader());
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
    }
}
```

自定义类加载器的核心在于对字节码文件的获取，如果是加密的字节码则需要在该类中对文件进行解密。由于这里只是演示，我并未对class文件进行加密，因此没有解密的过程。

这里有几点需要注意 :
1、这里传递的文件名需要是类的全限定性名称，即com.pdai.jvm.classloader.Test2格式的，因为 defineClass 方法是按这种格式进行处理的。
2、最好不要重写loadClass方法，因为这样容易破坏双亲委托模式。
3、这类Test 类本身可以被 AppClassLoader 类加载，因此我们不能把com/pdai/jvm/classloader/Test2.class 放在类路径下。否则，由于双亲委托机制的存在，会直接导致该类由 AppClassLoader 加载，而不会通过我们自定义类加载器来加载。


## Java 内存区域

线程私有的：
- 程序计数器
- 虚拟机栈
- 本地方法栈
线程共享的：
- 堆
- 方法区
- 直接内存 (非运行时数据区的一部分)

Java 虚拟机规范对于运行时数据区域的规定是相当宽松的。以堆为例：堆可以是连续空间，也可以不连续。堆的大小可以固定，也可以在运行时按需扩展 。虚拟机实现者可以使用任何垃圾回收算法管理堆，甚至完全不进行垃圾收集也是可以的。

程序计数器的功能是记录当前线程执行的字节码指令的地址，从而实现线程切换和恢复。

程序计数器是线程私有的，是为了线程切换时能够正确恢复执行现场。

虚拟机栈：每个线程在创建时都会创建一个虚拟机栈，用于存放线程的方法调用栈、局部变量表、操作数栈等信息。（执行的是Java方法）

本地方法栈：用于支持本地方法调用，即调用C/C++编写的本地方法。

为了保证线程的局部变量不被其他线程访问，虚拟机栈和本地方法栈是线程私有的。





## JVM垃圾回收机制




## jvm的内存模型



### 什么叫零拷贝

零拷贝（Zero Copy）是一种数据传输技术，它可以在不需要将数据从一个缓冲区复制到另一个缓冲区的情况下，将数据从一个地方传输到另一个地方。在零拷贝技术中，数据可以直接从磁盘、网络或其他设备中读取，然后通过DMA（Direct Memory Access）技术直接写入内存中，从而避免了数据的多次复制，提高了数据传输的效率。

在Java中，零拷贝技术可以通过NIO（New I/O）来实现。NIO提供了一种基于通道（Channel）和缓冲区（Buffer）的I/O模型，可以直接将数据从通道中读取到缓冲区中，或者将缓冲区中的数据直接写入通道中，从而避免了数据的多次复制。

### 为什么用常量池，有哪些常量池

https://blog.csdn.net/qq_41376740/article/details/80338158

常量池是Java中的一种特殊的内存区域，用于存储常量和符号引用。在Java中，常量池主要有以下几种：

1. 字面量常量池：用于存储字符串、数字等字面量常量。
2. 符号引用常量池：用于存储类、方法、字段等符号引用。
3. 运行时常量池：用于存储在类加载时解析的常量池信息，包括字面量常量池和符号引用常量池中的内容。

使用常量池的主要目的是为了提高程序的性能和减少内存的占用。由于常量池中的常量是唯一的，因此可以避免重复创建相同的常量对象，从而减少内存的占用。同时，由于常量池中的常量是在编译期间就确定的，因此可以在运行时直接使用，避免了重复计算和创建对象的开销，提高了程序的性能。

