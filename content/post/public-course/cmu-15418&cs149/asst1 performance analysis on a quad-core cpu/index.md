---
title: 'asst1'
date: 2024-03-01
lastmod: 2025-02-06
author: ['Ysyy']
categories: ['']
tags: ['cmu-15418&cs149']
description: ''
weight: None
draft: False
comments: True
showToc: True
TocOpen: True
hidemeta: False
disableShare: False
showbreadcrumbs: True
summary: ''
---
[参考](https://www.cnblogs.com/kalicener/p/16824312.html)

[任务](https://github.com/stanford-cs149/asst1)

## [Program 1: Parallel Fractal Generation Using Threads (20 points)](https://github.com/stanford-cs149/asst1#program-1-parallel-fractal-generation-using-threads-20-points)

提示:
需要先看CMU15-418/CS149的L2再完成Pro1

任务描述:
用多线程画mandelbrot fractal.

代码中给出了串行的实现, 你需要实现多线程的版本.

多线程版本中只需要修改 `workerThreadStart`函数.
不需要手动创建线程, 也不需要手动join线程.
直接调用mandelbrotThread().

### 1.1 & 1.2, 计算在2,3,4,5,6,7,8,16,32个线程下的加速比

#### 编写并观察

workerThreadStart函数的实现:

```C++
345void workerThreadStart(WorkerArgs *const args)
{

    // TODO FOR CS149 STUDENTS: Implement the body of the worker
    // thread here. Each thread should make a call to mandelbrotSerial()
    // to compute a part of the output image.  For example, in a
    // program that uses two threads, thread 0 could compute the top
    // half of the image and thread 1 could compute the bottom half.

    // printf("Hello world from thread %d\n", args->threadId);
    double startTime = CycleTimer::currentSeconds();
    // 每个线程负责的行数(除不尽的部分由最后一个线程负责)
    int height = args->height / args->numThreads;
    int startRow = args->threadId * height;
    int numRows = height;
    if (args->threadId == args->numThreads - 1)
    {
        // 如果是最后一个线程，那么就要把除不尽的部分也算上
        numRows = height + args->height % args->numThreads;
    }
    printf("Thread %d startRow: %d, numRows: %d\n", args->threadId, startRow, numRows);
    mandelbrotSerial(args->x0, args->y0, args->x1, args->y1,
                     args->width, args->height,
                     startRow, numRows,
                     args->maxIterations, args->output);
    double endTime = CycleTimer::currentSeconds();
    printf("Thread %d time: %.3f ms\n", args->threadId, (endTime - startTime) * 1000);
}
```

结果:

| 线程数 | 加速比 |
| ------ | ------ |
| 2      | 1.97   |
| 3      | 1.63   |
| 4      | 2.31   |
| 5      | 2.37   |
| 6      | 3.08   |
| 7      | 3.15   |
| 8      | 3.74   |
| 16     | 5.14   |

可以观察到，加速比和线程数并不是线性相关.

#### 猜测原因

猜测可能的原因有:

- 线程通信的开销
- 每个线程分配的任务不均匀

### 1.3 查看每个线程的执行时间,验证猜想

当线程数为4时, 每个线程的执行时间如下:
Thread 0 time: 63.974 ms
Thread 3 time: 65.563 ms
Thread 2 time: 259.972 ms
Thread 1 time: 260.669 ms

当线程数为8时, 每个线程的执行时间如下:
Thread 0 time: 13.702 ms
Thread 7 time: 16.831 ms
Thread 1 time: 57.324 ms
Thread 6 time: 61.069 ms
Thread 5 time: 113.431 ms
Thread 2 time: 115.753 ms
Thread 4 time: 164.736 ms
Thread 3 time: 166.306 ms

可以看到,中间线程分配的任务更多,执行时间更长.
因此在增加线程数时,加速比并不是线性增加的.

### 1.4

任务描述:

- 解决上面的问题,使得加速比更接近线性.
  - 如: 8线程时的加速比需要在7~8之间.
- 解决方法需要具有适用性, 适用所有的线程数.

tips:
有一个非常简单的静态赋值可以实现这个目标，并且线程之间不需要通信/同步.

#### 解决方案

思路:
根据代码可知, 每行的计算是独立的, 因此可以将每行分配给不同的线程.
但由上面的实验可知,中间行的计算量比较大.

因此我们不应该直接平均切分行, 而是以线程数量为步长,线程交叉依次分配行.
即 第i个线程分配k*n+i行.

```C++
void workerThreadStart(WorkerArgs *const args)
{

    // TODO FOR CS149 STUDENTS: Implement the body of the worker
    // thread here. Each thread should make a call to mandelbrotSerial()
    // to compute a part of the output image.  For example, in a
    // program that uses two threads, thread 0 could compute the top
    // half of the image and thread 1 could compute the bottom half.

    // printf("Hello world from thread %d\n", args->threadId);
    double startTime = CycleTimer::currentSeconds();

    /*
    方案1
    // 每个线程负责的行数(除不尽的部分由最后一个线程负责)
    int baseHeight = args->height / args->numThreads;
    int startRow = args->threadId * baseHeight;
    int numRows = baseHeight;

    int yu = args->height % args->numThreads;
    // 均匀分配剩余行
    if (args->threadId < yu)
    {
        numRows++;
    }
    startRow += std::min(args->threadId, yu);
    printf("Thread %d startRow: %d, numRows: %d\n", args->threadId, startRow, numRows);
    mandelbrotSerial(args->x0, args->y0, args->x1, args->y1,
                     args->width, args->height,
                     startRow, numRows,
                     args->maxIterations, args->output);

    */

    // 方案2, 依次分配行
    int height = args->height;
    for (int i = args->threadId; i < height; i += args->numThreads)
    {
        mandelbrotSerial(args->x0, args->y0, args->x1, args->y1,
                         args->width, args->height,
                         i, 1,
                         args->maxIterations, args->output);
    }

    double endTime = CycleTimer::currentSeconds();
    printf("Thread %d time: %.3f ms\n", args->threadId, (endTime - startTime) * 1000);
}
```

输出结果:

Thread 3 time: 88.842 ms
Thread 1 time: 89.680 ms
Thread 0 time: 89.717 ms
Thread 7 time: 90.280 ms
Thread 5 time: 90.715 ms
Thread 6 time: 90.743 ms
Thread 2 time: 91.049 ms
Thread 4 time: 92.982 ms
[mandelbrot thread]:            [93.318] ms
Wrote image file mandelbrot-thread.ppm
                                (7.10x speedup from 8 threads)

上面的解决方案使得每个线程的执行时间基本相同,因此加速比接近线性.
在8线程时,加速比为7.1.

### 1.5 16线程和8线程的加速比

现在16线程是否明显优于8线程? 给出是或否的原因.
  (6.45x speedup from 16 threads)
16线程并没有明显由于8线程,反而还更慢.
原因:

- 电脑本身是4核, 超线程后是8线程.
- 16线程时线程切换反而导致开销增加.

### 总结

pro1的目的是为了认识到并行计算的overhead, 以及多线程在计算上也应该是依次交替分配的. 不能简单的平均分配.

pro1是通过垂直分割来实现并行计算.
而向量化是通过水平分割来实现并行计算.

## program-2-vectorizing-code-using-simd-intrinsics

前提: L2
任务描述：
使用SIMD指令(CS149intrin.h提供的),来实现clampedExpVector函数.

示例函数:

```C++
void absVector(float* values, float* output, int N) {
  __cs149_vec_float x;
  __cs149_vec_float result;
  __cs149_vec_float zero = _cs149_vset_float(0.f);
  __cs149_mask maskAll, maskIsNegative, maskIsNotNegative;

//  Note: Take a careful look at this loop indexing.  This example
//  code is not guaranteed to work when (N % VECTOR_WIDTH) != 0.
//  Why is that the case?
  for (int i=0; i<N; i+=VECTOR_WIDTH) {

    // All ones
    maskAll = _cs149_init_ones();

    // All zeros
    maskIsNegative = _cs149_init_ones(0);

    // Load vector of values from contiguous memory addresses
    _cs149_vload_float(x, values+i, maskAll);               // x = values[i];

    // Set mask according to predicate
    _cs149_vlt_float(maskIsNegative, x, zero, maskAll);     // if (x < 0) {

    // Execute instruction using mask ("if" clause)
    _cs149_vsub_float(result, zero, x, maskIsNegative);      //   output[i] = -x;

    // Inverse maskIsNegative to generate "else" mask
    maskIsNotNegative = _cs149_mask_not(maskIsNegative);     // } else {

    // Execute instruction ("else" clause)
    _cs149_vload_float(result, values+i, maskIsNotNegative); //   output[i] = x; }

    // Write results back to memory
    _cs149_vstore_float(output+i, result, maskAll);
  }
}
```

示例函数absVector并不能适用于所有情况,原因如下:
当n%VECTOR_WIDTH != 0时, 会越界.

### 1&2 实现clampedExpVector函数

```C++
void clampedExpVector(float *values, int *exponents, float *output, int N)
{

  //
  // CS149 STUDENTS TODO: Implement your vectorized version of
  // clampedExpSerial() here.
  //
  // Your solution should work for any value of
  // N and VECTOR_WIDTH, not just when VECTOR_WIDTH divides N
  //
  __cs149_vec_float one, nine;
  __cs149_vec_int zeroInt, oneInt;

  oneInt = _cs149_vset_int(1);
  zeroInt = _cs149_vset_int(0);
  one = _cs149_vset_float(1.f);
  nine = _cs149_vset_float(9.999999f);
  for (int i = 0; i < N; i += VECTOR_WIDTH)
  {
    __cs149_mask maskAll, maskIsZero, maskIsNotZero;
    __cs149_vec_float x;
    __cs149_vec_int y;
    // All ones
    maskAll = _cs149_init_ones();

    // All zeros
    maskIsZero = _cs149_init_ones(0);

    // 防止在最后一次循环时，i+VECTOR_WIDTH超出N
    if (i + VECTOR_WIDTH > N)
    {
      maskAll = _cs149_init_ones(N - i);
    }
    // float x = values[i];
    _cs149_vload_float(x, values + i, maskAll);

    // int y = exponents[i];
    _cs149_vload_int(y, exponents + i, maskAll);

    // if (y == 0)
    _cs149_veq_int(maskIsZero, y, zeroInt, maskAll);
    // {
    //   output[i] = 1.f;
    // }
    _cs149_vstore_float(output + i, one, maskIsZero);

    // else
    maskIsNotZero = _cs149_mask_not(maskIsZero);
    // 消除最后一次循环时，i+VECTOR_WIDTH超出N的情况
    maskIsNotZero = _cs149_mask_and(maskIsNotZero, maskAll);

    {
      // float result = x;
      __cs149_vec_float result = x;

      // int count = y - 1;
      __cs149_vec_int count;
      _cs149_vsub_int(count, y, oneInt, maskIsNotZero);

      // 哪些count>0
      __cs149_mask countMark;
      _cs149_vgt_int(countMark, count, zeroInt, maskIsNotZero);

      // while (count > 0)
      while (_cs149_cntbits(countMark) > 0)
      {
        // result *= x;
        _cs149_vmult_float(result, result, x, countMark);

        // count--;
        _cs149_vsub_int(count, count, oneInt, countMark);

        // 哪些count>0
        _cs149_vgt_int(countMark, count, zeroInt, countMark);
      }

      // if (result > 9.999999f)
      __cs149_mask gtNineMask;
      _cs149_vgt_float(gtNineMask, result, nine, maskIsNotZero);

      // { reult = 9.999999f;}
      _cs149_vmove_float(result, nine, gtNineMask);

      // output[i] = result;

      _cs149_vstore_float(output + i, result, maskIsNotZero);
    }
  }
}
```

通过init_ones来防止在有n%vectorWith!=0时 越界.

- 在最开始的maskAll时设置
- 在取反码后也要设置一次

count循环:
通过设置一个mask来标记哪些count>0, 从而实现循环.

修改vectorWidth为2, 4, 8, to 16来回答:
Does the vector utilization increase, decrease or stay the same as VECTOR_WIDTH changes? Why?

vectorWidth为2时, 结果如下:
****************** Printing Vector Unit Statistics *******************
Vector Width:              2
Total Vector Instructions: 162728
Vector Utilization:        77.0%
Utilized Vector Lanes:     250653
Total Vector Lanes:        325456

vectorWidth为4时, 结果如下:
****************** Printing Vector Unit Statistics *******************
Vector Width:              3
Total Vector Instructions: 119440
Vector Utilization:        72.2%
Utilized Vector Lanes:     258879
Total Vector Lanes:        358320

vectorWidth为8时, 结果如下:
****************** Printing Vector Unit Statistics *******************
Vector Width:              8
Total Vector Instructions: 51628
Vector Utilization:        66.0%
Utilized Vector Lanes:     272539
Total Vector Lanes:        413024

vectorWidth为16时, 结果如下:
****************** Printing Vector Unit Statistics *******************
Vector Width:              16
Total Vector Instructions: 26968
Vector Utilization:        64.2%
Utilized Vector Lanes:     277188
Total Vector Lanes:        431488

可以发现, 随着vectorWidth的增加, vectorUtilization也在减少.

原因:
有多个条件语句,当vectorWidth增加时, 每次在某个条件中不执行的指令也会增加.

### 3 实现arraySumVector

```C++
float arraySumVector(float *values, int N)
{

  //
  // CS149 STUDENTS TODO: Implement your vectorized version of arraySumSerial here
  //

  __cs149_vec_float sum = _cs149_vset_float(0.f);
  for (int i = 0; i < N; i += VECTOR_WIDTH)
  {
    __cs149_mask maskAll;
    __cs149_vec_float x;
    // All ones
    maskAll = _cs149_init_ones();

    // 防止在最后一次循环时，i+VECTOR_WIDTH超出N
    if (i + VECTOR_WIDTH > N)
    {
      maskAll = _cs149_init_ones(N - i);
    }
    // float x = values[i];
    _cs149_vload_float(x, values + i, maskAll);

    // sum += x;
    _cs149_vadd_float(sum, sum, x, maskAll);
  }
  float result = 0.f;
  // log2(VECTOR_WIDTH)内解决
  for (int i = 0; i < log2(VECTOR_WIDTH); i++)
  {
    // 使用_cs149_hadd_float函数，将sum中的每两个元素相加
    // 再使用_cs149_interleave_float函数，将sum中的每两个元素交叉放置
    // 重复log2(VECTOR_WIDTH)次
    _cs149_hadd_float(sum, sum);
    _cs149_interleave_float(sum, sum);
  }
  // 将sum中的第一个元素赋值给result
  result = sum.value[0];
  return result;
}
```

假设VECTOR_WIDTHs始终是N的因子.

可以实现在O(N/VECTOR_WIDTH + log2(VECTOR_WIDTH))的时间内完成计算.

最后的log2实现方式.
提示中给了两个函数
hadd: 将每两个元素相加
interleave: 将每两个元素交叉放置

因此我们可以类似与归并排序的方式,将sum中的每两个元素相加,再将每两个元素交叉放置.
重复log2(VECTOR_WIDTH)次后,第一个元素就是结果.

## program-3 ISPC

前提: L3

### part1 ISPC basic

任务:学习ISPC基本概念和编写.

ISPC是一种编译器,可以将C代码编译为SIMD指令.

### part2 ISPC task

任务描述:
观察ISPCtask执行的结果

#### 1

启动mandelbrot_ispc --tasks

结果:
[mandelbrot serial]:            [424.881] ms
Wrote image file mandelbrot-serial.ppm
[mandelbrot ispc]:              [97.180] ms
Wrote image file mandelbrot-ispc.ppm
[mandelbrot multicore ispc]:    [48.986] ms
Wrote image file mandelbrot-task-ispc.ppm
                                (4.37x speedup from ISPC)
                                (8.67x speedup from task ISPC)

因为设置了两个task所以大约是两倍的加速比 对于 ISPC

#### 2

修改mandelbrot_ispc_withtasks()中的task数量,
you should be able to achieve performance that exceeds the sequential version of the code by over 32 times!
How did you determine how many tasks to create?
Why does the number you chose work best?

根据机器的最大超线程数量设置
我设置了16个task, 因为我的机器是4核8线程, 16个task可以使得每个线程都有两个task.

#### 3

what happens when you launch 10,000 ISPC tasks? What happens when you launch 10,000 threads?

向量加速

思考题:
Q: Why are there two different mechanisms (foreach and launch) for expressing independent, parallelizable work to the ISPC system?
A:foreach是将一个任务分配给多个线程,而launch是将多个任务分配给多个线程.

Q: Couldn't the system just partition the many iterations of foreach across all cores and also emit the appropriate SIMD code for the cores?
A:

## program-4 Iterative sqrt (15 points)

用sqrt复习ISPC的基本概念

### 1

运行结果:
[sqrt serial]:          [1316.793] ms
[sqrt ispc]:            [301.134] ms
[sqrt task ispc]:       [52.439] ms
                                (4.37x speedup from ISPC)
                                (25.11x speedup from task ISPC)
4.37x speedup due to SIMD
25.11 / 4.37 = 5.74x speedup due to multi-core

### 2

构造数组使得加速比最大.

全部数为2.998.
思路:
因为每个元素相同可以让计算更均匀,2.998可以充分调动cpu
结构:
                                (5.60x speedup from ISPC)
                                (30.39x speedup from task ISPC)

### 3

构造数组使得加速比最小.

全部数为1
思路:
1的sqrt计算迭代最少.

结果:
                                (2.50x speedup from ISPC)
                                (3.08x speedup from task ISPC)

## program-5 BLAS saxpy (10 points)

### 1

运行观察加速比
[saxpy ispc]:           [25.098] ms     [11.874] GB/s   [1.594] GFLOPS
[saxpy task ispc]:      [18.438] ms     [16.164] GB/s   [2.169] GFLOPS
                                (1.36x speedup from use of tasks)

因为需要访问内存所以加速比不高.

### 2

Even though saxpy loads one element from X, one element from Y, and writes one element to result the multiplier by 4 is correct. Why is this the case? (Hint, think about how CPU caches work.)

当程序写入结果的一个元素时，它首先将包含这个元素的缓存行提取到缓存中。这需要一个内存操作。然后，当不需要这个缓存行时，它将从缓存中闪现出来，这需要另一个内存操作。