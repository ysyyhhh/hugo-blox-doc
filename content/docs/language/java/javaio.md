# Java IO

## Java IO流介绍

Java IO流主要分为字节流和字符流，字节流主要用于处理二进制文件，字符流主要用于处理文本文件。

四个抽象类：
- InputStream：字节输入流
- OutputStream：字节输出流
- Reader：字符输入流
- Writer：字符输出流

### 字节流

字节流主要用于处理二进制文件，如图片、视频、音频等。

FileInputStream和FileOutputStream是两个基本的字节流，用于读写文件。

```java
public class FileInputStreamTest {
    public static void main(String[] args) {
        try (FileInputStream fis = new FileInputStream("test.txt")) {
            int data;
            while ((data = fis.read()) != -1) {
                System.out.print((char) data);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```


```java
public class FileOutputStreamTest {
    public static void main(String[] args) {
        try (FileOutputStream fos = new FileOutputStream("test.txt")) {
            String str = "Hello, World!";
            byte[] bytes = str.getBytes();
            fos.write(bytes);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

```

### 字符流

字符流主要用于处理文本文件，如txt文件。

为什么会有字符流
- 字节流是以字节为单位读写数据，而字符流是以字符为单位读写数据
- 字节流读取中文字符时可能会出现乱码，而字符流不会出现乱码

字符流默认采用unicode编码，可以指定编码格式。

常用字符编码所占字节数

| 编码格式 |中文字符所占字节数 | 英文字符所占字节数 |
| --- | --- | --- |
| GBK | 2 | 1 |
| UTF-8 | 3 | 1 |
| UTF-16 | 2 | 2 |
| unicode | 2 | 2 |

FileReader和FileWriter是两个基本的字符流，用于读写文件。

```java
public class FileReaderTest {
    public static void main(String[] args) {
        try (FileReader fr = new FileReader("test.txt")) {
            int data;
            while ((data = fr.read()) != -1) {
                System.out.print((char) data);
            }
        } catch (IOException e) {
            e.printStackTrace();

        }
    }
}
```

```java
public class FileWriterTest {
    public static void main(String[] args) {
        try (FileWriter fw = new FileWriter("test.txt")) {
            String str = "Hello, World!";
            fw.write(str);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

### 字节缓冲流

字节缓冲流主要用于提高读写文件的效率。

BufferedInputStream和BufferedOutputStream是两个基本的字节缓冲流，用于读写文件。

BufferedInputStream 内部维护了一个缓冲区，这个缓冲区实际就是一个字节数组，通过阅读 BufferedInputStream 源码即可得到这个结论.
缓冲器默认大小为 8192 字节，也就是 8KB，这个大小是可以通过构造函数来指定的。
```java
public
class BufferedInputStream extends FilterInputStream {
    // 内部缓冲区数组
    protected volatile byte buf[];
    // 缓冲区的默认大小
    private static int DEFAULT_BUFFER_SIZE = 8192;
    // 使用默认的缓冲区大小
    public BufferedInputStream(InputStream in) {
        this(in, DEFAULT_BUFFER_SIZE);
    }
    // 自定义缓冲区大小
    public BufferedInputStream(InputStream in, int size) {
        super(in);
        if (size <= 0) {
            throw new IllegalArgumentException("Buffer size <= 0");
        }
        buf = new byte[size];
    }
}
```


### 字符缓冲流

字符缓冲流主要用于提高读写文件的效率。

### 打印流

PrintStream和PrintWriter是两个基本的打印流，用于打印数据。

System.out实际是获取了一个PrintStream对象，System.out.println()实际是调用了PrintStream对象的println()方法。

### 随机访问流

RandomAccessFile是一个基本的随机访问流，用于读写文件, 支持随机访问文件。
RandomAccessFile 的构造方法如下
```java
public RandomAccessFile(String name, String mode) throws FileNotFoundException {
    this(name != null ? new File(name) : null, mode);
}
```
mode 参数指定了 RandomAccessFile 的访问模式，有 "r"、"rw"、"rws"、"rwd" 四种模式，分别表示：
- "r"：以只读方式打开
- "rw"：以读写方式打开
- "rws"：以读写方式打开，对文件的内容或元数据的每个更新都同步写入到底层存储设备
- "rwd"：以读写方式打开，对文件内容的每个更新都同步写入到底层存储设备

```java
public class RandomAccessFileTest {
    public static void main(String[] args) {
        try (RandomAccessFile raf = new RandomAccessFile("test.txt", "rw")) {
            raf.write("Hello, World!".getBytes());
            raf.seek(0);
            byte[] bytes = new byte[1024];
            int len;
            while ((len = raf.read(bytes)) != -1) {
                System.out.println(new String(bytes, 0, len));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

## IO中的设计模式

### 装饰器模式

装饰器模式是一种结构型设计模式，允许你通过将对象放入包含行为的特殊封装对象中来为原对象绑定新的行为。

装饰器模式的主要优点有：
- 可以在不修改现有对象的情况下，动态地给一个对象增加一些额外的功能
- 可以使用多个装饰器包装一个对象，得到功能更加强大的对象

字节流和字符流的装饰器模式
FilterInputStream和FilterOutputStream是两个基本的装饰器，用于装饰字节流。


### 适配器模式

适配器模式是一种结构型设计模式，它能使接口不兼容的对象能够相互合作。

InputStreamReader和OutputStreamWriter是两个基本的适配器，用于适配字节流和字符流。

InputStreamReader是字节流到字符流的适配器，OutputStreamWriter是字符流到字节流的适配器。


### 观察者模式

观察者模式是一种行为型设计模式，它定义了一种一对多的依赖关系，让多个观察者对象同时监听某一个主题对象。

NIO中的文件监听器就是观察者模式的一种应用。

NIO中的文件监听器基于WatchService接口和Watchable接口.

### 工厂模式

Files类的newInputStream()和newOutputStream()方法就是工厂模式的一种应用。

## IO模型

IO操作的本质是数据的输入和输出，而IO模型是操作系统对IO操作的抽象。
平时接触最多的是磁盘IO和网络IO。

UNIX系统下, IO模型有五种：
- 同步阻塞IO
- 同步非阻塞IO
- IO复用
- 信号驱动IO
- 异步IO

### Java中的三种常见IO

- BIO（Blocking IO）：同步阻塞IO
- NIO（Non-blocking IO）：同步非阻塞IO
- AIO（Asynchronous IO）：异步IO


BIO（Blocking IO）：同步阻塞IO
- 一个线程只能处理一个连接
- 适用于连接数较少的场景

当有大量的连接时，BIO的效率会很低，因为每个连接都需要一个线程来处理。

IO多路复用（IO Multiplexing）：IO复用
线程首先发起IO请求，然后阻塞在IO复用器上，当IO复用器检测到有IO事件时，线程才会被唤醒。

NIO（Non-blocking IO）：同步非阻塞IO

NIO是一种同步非阻塞IO模型，适用于连接数较多的场景。
NIO的核心是Selector，Selector可以同时监控多个通道的IO事件。

AIO（Asynchronous IO）：异步IO
AIO是一种异步IO模型，适用于连接数较多且数据量较大的场景。

## JavaNIO

NIO的核心组件
- Channel: 通道, 用于读写数据
- Buffer: 缓冲区, 用于存储数据
- Selector: 多路复用器, 用于监控多个通道的IO事件


### NIO零拷贝

零拷贝是指数据在内存和磁盘之间传输时，不需要在中间进行数据拷贝。

