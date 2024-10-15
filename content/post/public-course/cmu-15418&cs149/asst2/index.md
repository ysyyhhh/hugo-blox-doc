---
title: 'asst2'
date: 2024-03-01
lastmod: 2024-10-15
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
## C++ Sync

### thread的使用

```C++
#include <thread>
#include <stdio.h>

void my_func(int thread_id, int num_threads) {
 printf("Hello from spawned thread %d of %d\n", thread_id, num_threads);
}

int main(int argc, char** argv) {

  std::thread t0 = std::thread(my_func, 0, 2);
  std::thread t1 = std::thread(my_func, 1, 2);

  printf("The main thread is running concurrently with spawned threads.\n");

  t0.join();
  t1.join();

  printf("Spawned threads have terminated at this point.\n");

  return 0;
}
```

### mutex

```C++
#include <chrono>
#include <iostream>
#include <map>
#include <mutex>
#include <string>
#include <thread>
 
std::map<std::string, std::string> g_pages;
std::mutex g_pages_mutex;
 
void save_page(const std::string& url)
{
    // simulate a long page fetch
    std::this_thread::sleep_for(std::chrono::seconds(2));
    std::string result = "fake content";
 
    std::lock_guard<std::mutex> guard(g_pages_mutex);
    g_pages[url] = result;
}
 
int main() 
{
    std::thread t1(save_page, "http://foo");
    std::thread t2(save_page, "http://bar");
    t1.join();
    t2.join();
 
    // safe to access g_pages without lock now, as the threads are joined
    for (const auto& pair : g_pages)
        std::cout << pair.first << " => " << pair.second << '\n';
}
```

Output

```shell
http://bar => fake content
http://foo => fake content
```

### condition_variable

线程调用 wait (lock)来指示它希望等待来自另一个线程的通知。

注意，互斥对象(包装在 std: : only _ lock 中)被传递给 wait ()调用。当通知线程时，条件变量将获得锁。

这意味着当调用 wait ()返回时，调用线程是锁的当前持有者。锁通常用于保护线程现在需要检查的共享变量，以确保它正在等待的条件为真。

创建 N 个线程。N-1个线程等待来自线程0的通知，然后在接到通知后，自动递增一个受共享互斥锁保护的计数器。

```C++
/*
 * Wrapper class around a counter, a condition variable, and a mutex.
 */
class ThreadState
{
public:
    std::condition_variable *condition_variable_;
    std::mutex *mutex_;
    int counter_;
    int num_waiting_threads_;
    ThreadState(int num_waiting_threads)
    {
        condition_variable_ = new std::condition_variable();
        mutex_ = new std::mutex();
        counter_ = 0;
        num_waiting_threads_ = num_waiting_threads;
    }
    ~ThreadState()
    {
        delete condition_variable_;
        delete mutex_;
    }
};

void signal_fn(ThreadState *thread_state)
{
    // Acquire mutex to make sure the shared counter is read in a
    // consistent state.
    thread_state->mutex_->lock();
    while (thread_state->counter_ < thread_state->num_waiting_threads_)
    {
        thread_state->mutex_->unlock();
        // Release the mutex before calling `notify_all()` to make sure
        // waiting threads have a chance to make progress.
        thread_state->condition_variable_->notify_all();
        // Re-acquire the mutex to read the shared counter again.
        thread_state->mutex_->lock();
    }
    thread_state->mutex_->unlock();
}

void wait_fn(ThreadState *thread_state)
{
    // A lock must be held in order to wait on a condition variable.
    // This lock is atomically released before the thread goes to sleep
    // when `wait()` is called. The lock is atomically re-acquired when
    // the thread is woken up using `notify_all()`.
    std::unique_lock<std::mutex> lk(*thread_state->mutex_);
    thread_state->condition_variable_->wait(lk);
    // Increment the shared counter with the lock re-acquired to inform the
    // signaling thread that this waiting thread has successfully been
    // woken up.
    thread_state->counter_++;
    printf("Lock re-acquired after wait()...\n");
    lk.unlock();
}

/*
 * Signaling thread spins until each waiting thread increments a shared
 * counter after being woken up from the `wait()` method.
 */
void condition_variable_example()
{
    int num_threads = 3;

    printf("==============================================================\n");
    printf("Starting %d threads for signal-and-waiting...\n", num_threads);
    std::thread *threads = new std::thread[num_threads];
    ThreadState *thread_state = new ThreadState(num_threads - 1);
    threads[0] = std::thread(signal_fn, thread_state);
    for (int i = 1; i < num_threads; i++)
    {
        threads[i] = std::thread(wait_fn, thread_state);
    }
    for (int i = 0; i < num_threads; i++)
    {
        threads[i].join();
    }
    printf("==============================================================\n");

    delete thread_state;
    delete[] threads;
}
```

## part_a

### step 1 实现TaskSystemParallelSpawn

```c++
void TaskSystemParallelSpawn::run(IRunnable *runnable, int num_total_tasks)
{

    //
    // TODO: CS149 students will modify the implementation of this
    // method in Part A.  The implementation provided below runs all
    // tasks sequentially on the calling thread.
    //

    std::atomic<int> taskId(0);
    int num_threads = this->num_threads;

    std::thread threads[num_threads];
    // 交叉分配任务

    for (int i = 0; i < num_threads; i++)
    {
        threads[i] = std::thread([&, i]()
                                 {
                int task_id = taskId.fetch_add(1);
                while (task_id < num_total_tasks)
                {
                    runnable->runTask(task_id, num_total_tasks);
                    task_id = taskId.fetch_add(1);
                } });
    }
    for (int i = 0; i < num_threads; i++)
    {
        threads[i].join();
    }

    // printf("done\n");
}
```

Q:How will you assign tasks to your worker threads? Should you consider static or dynamic assignment of tasks to threads?
A:交叉分配任务，动态分配任务

Q:How will you ensure that all tasks are executed exactly once?
A:使用原子变量taskId

### step 2 实现  TaskSystemParallelThreadPoolSpinning

step1 的overhead主要是创建线程的开销(尤其是计算量低的任务上)，因此使用线程池可以减少开销

要求: 在TestSystem 创建时,或者在run时创建线程池

Q1: 作为一个开始的实现，我们建议您将worker threads设计为连续循环，始终检查它们是否有更多的工作要执行。(进入 while 循环直到条件为真的线程通常称为“spinning”)
那么worker thread 如何确定有work要执行呢？

```c++
TaskSystemParallelThreadPoolSpinning::TaskSystemParallelThreadPoolSpinning(int num_threads) : ITaskSystem(num_threads)
{
    //
    // TODO: CS149 student implementations may decide to perform setup
    // operations (such as thread pool construction) here.
    // Implementations are free to add new class member variables
    // (requiring changes to tasksys.h).
    //
    exit_flag_ = false;
    for (int i = 0; i < num_threads; i++)
    {
        threads.emplace_back(&TaskSystemParallelThreadPoolSpinning::func, this);
    }
}

TaskSystemParallelThreadPoolSpinning::~TaskSystemParallelThreadPoolSpinning()
{
    exit_flag_ = true;
    for (auto &thread : threads)
    {
        thread.join();
    }
}

void TaskSystemParallelThreadPoolSpinning::run(IRunnable *runnable, int num_total_tasks)
{

    //
    // TODO: CS149 students will modify the implementation of this
    // method in Part A.  The implementation provided below runs all
    // tasks sequentially on the calling thread.
    //
    // printf("run\n");
    runnable_ = runnable;
    num_tasks_ = num_total_tasks;
    num_tasks_done_ = num_total_tasks;
    for (int i = 0; i < num_total_tasks; i++)
    {
        tasks_mutex_.lock();
        tasks_.push(i);
        tasks_mutex_.unlock();
    }
    while (num_tasks_done_ < num_total_tasks)
    {
        std::this_thread::yield();
    };
    // Q:为什么要使用yield
    // A:因为如果不使用yield，那么线程会一直占用CPU，导致其他线程无法运行
    // Q:那我直接死循环呢
    // A:死循环会导致CPU占用率100%，导致其他线程无法运行
}
```

Q2:确保 run ()实现所需的同步行为是非常重要的。如何更改 run ()的实现以确定批量任务启动中的所有任务都已完成？
A:使用原子变量num_tasks_done_，每个任务完成时，num_tasks_done_加一，当num_tasks_done_等于num_total_tasks时，所有任务完成

### step 3 实现 TaskSystemParallelThreadPoolSleeping

Step2的缺点：
当线程“spin”等待某些操作时，它们会利用 CPU 核心的执行资源。

- 例如，工作线程可能会循环等待新任务到达。
- 另一个例子是，主线程可能会循环等待辅助线程完成所有任务，这样它就可以从 run ()调用返回。

这可能会影响性能，因为即使这些线程没有做有用的工作，也会使用 CPU 资源来运行这些线程。

在任务的这一部分中，我们希望您通过让线程处于休眠状态来提高任务系统的效率，直到它们所等待的条件得到满足。

您的实现可以选择使用条件变量来实现此行为。条件变量是一个同步原语，它允许线程在等待条件存在时休眠(不占用 CPU 处理资源)。其他线程向等待唤醒的线程发出“信号”，以查看它们所等待的条件是否已经满足。例如，如果没有工作要做，您的工作线程可能会处于休眠状态(这样它们就不会从尝试执行有用工作的线程那里占用 CPU 资源)。另一个例子是，调用 run ()的主应用程序线程可能希望在等待批量任务启动中的所有任务由工作线程完成时休眠。(否则，一个旋转的主线程将从工作线程那里夺走 CPU 资源!)有关 C + + 中条件变量的更多信息，请参见我们的 C + + 同步教程。

您在这部分作业中的实现可能需要考虑棘手的race conditions 。您需要考虑许多可能的线程行为交错

您可能需要考虑编写额外的测试用例来测试您的系统。赋值入门代码包括评分脚本用于评分代码性能的工作负载，但是我们也将使用一组更广泛的工作负载来测试您的实现的正确性，而我们在入门代码中并没有提供这些工作负载！

The assignment starter code includes the workloads that the grading script will use to grade the performance of your code, but we will also test the correctness of your implementation using a wider set of workloads that we are not providing in the starter code!

tasksys.h

```C++
/*
 * TaskSystemParallelThreadPoolSleeping: This class is the student's
 * optimized implementation of a parallel task execution engine that uses
 * a thread pool. See definition of ITaskSystem in
 * itasksys.h for documentation of the ITaskSystem interface.
 */
class TaskSystemParallelThreadPoolSleeping : public ITaskSystem
{
public:
    TaskSystemParallelThreadPoolSleeping(int num_threads);
    ~TaskSystemParallelThreadPoolSleeping();
    const char *name();
    void run(IRunnable *runnable, int num_total_tasks);
    TaskID runAsyncWithDeps(IRunnable *runnable, int num_total_tasks,
                            const std::vector<TaskID> &deps);
    void sync();

private:
    std::vector<std::thread> threads;
    int num_tasks_;
    bool exit_flag_;
    std::atomic<int> num_tasks_done_;
    std::queue<int> tasks_;
    std::mutex tasks_mutex_;
    IRunnable *runnable_{};
    void func();
    std::condition_variable *queue_condition_ = new std::condition_variable();
    std::condition_variable *all_done_condition_ = new std::condition_variable();
    int num_waiting_threads_;
    std::atomic<int> num_tasks_remaining_;
    std::mutex all_done_mutex_;
};
```

tasksys.cpp

```C++
/*
 * ================================================================
 * Parallel Thread Pool Sleeping Task System Implementation
 * ================================================================
 */

const char *TaskSystemParallelThreadPoolSleeping::name()
{
    return "Parallel + Thread Pool + Sleep";
}

void TaskSystemParallelThreadPoolSleeping::func()
{
    int task_id;

    while (!exit_flag_)
    {
        task_id = -1;
        while (task_id == -1)
        {
            std::unique_lock<std::mutex> lk(tasks_mutex_);
            // 等待任务
            queue_condition_->wait(lk, []
                                   { return 1; });
            if (exit_flag_)
            {
                return;
            }
            if (!tasks_.empty())
            {
                task_id = tasks_.front();
                tasks_.pop();
            }
        }
        runnable_->runTask(task_id, num_tasks_);
        num_tasks_remaining_--;

        if (!num_tasks_remaining_)
        {
            // 通知主线程
            // printf("notify_all_done\n");
            all_done_condition_->notify_one();
        }
        else
        {
            // 通知其他线程
            // printf("notify_all\n");
            queue_condition_->notify_one();
        }
    }
}
TaskSystemParallelThreadPoolSleeping::TaskSystemParallelThreadPoolSleeping(int num_threads) : ITaskSystem(num_threads)
{
    //
    // TODO: CS149 student implementations may decide to perform setup
    // operations (such as thread pool construction) here.
    // Implementations are free to add new class member variables
    // (requiring changes to tasksys.h).
    //
    exit_flag_ = false;

    for (int i = 0; i < num_threads; i++)
    {
        threads.emplace_back(&TaskSystemParallelThreadPoolSleeping::func, this);
    }
}

TaskSystemParallelThreadPoolSleeping::~TaskSystemParallelThreadPoolSleeping()
{
    //
    // TODO: CS149 student implementations may decide to perform cleanup
    // operations (such as thread pool shutdown construction) here.
    // Implementations are free to add new class member variables
    // (requiring changes to tasksys.h).
    //
    exit_flag_ = true;
    queue_condition_->notify_all();
    for (auto &thread : threads)
    {
        thread.join();
    }
}

void TaskSystemParallelThreadPoolSleeping::run(IRunnable *runnable, int num_total_tasks)
{
    //
    // TODO: CS149 students will modify the implementation of this
    // method in Parts A and B.  The implementation provided below runs all
    // tasks sequentially on the calling thread.
    //

    runnable_ = runnable;
    num_tasks_ = num_total_tasks;

    num_tasks_remaining_ = num_total_tasks;

    tasks_mutex_.lock();
    for (int i = 0; i < num_total_tasks; i++)
    {
        tasks_.push(i);
    }
    tasks_mutex_.unlock();
    // 通知其他线程
    queue_condition_->notify_all();

    // printf("run\n");

    while (num_tasks_remaining_)
    {

        std::unique_lock<std::mutex> lk2(all_done_mutex_);
        all_done_condition_->wait(lk2, []
                                  { return 1; });
    }
    // printf("all done\n");
    // printf("all done\n");
}
```

结果分析:

sleep对spin的提升效果不明显，可能是因为任务太少，线程切换的开销比较大.

运行结果:

```shell
================================================================================
Running task system grading harness... (11 total tests)
  - Detected CPU with 16 execution contexts
  - Task system configured to use at most 8 threads
================================================================================
================================================================================
Executing test: super_super_light...
Reference binary: ./runtasks_ref_linux
Results for: super_super_light
                                        STUDENT   REFERENCE   PERF?
[Serial]                                5.281     5.788       0.91  (OK)
[Parallel + Always Spawn]               95.221    92.995      1.02  (OK)
[Parallel + Thread Pool + Spin]         10.877    10.446      1.04  (OK)
[Parallel + Thread Pool + Sleep]        6.943     42.705      0.16  (OK)
================================================================================
Executing test: super_light...
Reference binary: ./runtasks_ref_linux
Results for: super_light
                                        STUDENT   REFERENCE   PERF?
[Serial]                                37.497    37.844      0.99  (OK)
[Parallel + Always Spawn]               108.136   108.805     0.99  (OK)
[Parallel + Thread Pool + Spin]         10.777    13.615      0.79  (OK)
[Parallel + Thread Pool + Sleep]        10.274    44.686      0.23  (OK)
================================================================================
Executing test: ping_pong_equal...
Reference binary: ./runtasks_ref_linux
Results for: ping_pong_equal
                                        STUDENT   REFERENCE   PERF?
[Serial]                                603.419   606.739     0.99  (OK)
[Parallel + Always Spawn]               167.412   178.638     0.94  (OK)
[Parallel + Thread Pool + Spin]         105.983   123.525     0.86  (OK)
[Parallel + Thread Pool + Sleep]        108.243   148.316     0.73  (OK)
================================================================================
Executing test: ping_pong_unequal...
Reference binary: ./runtasks_ref_linux
Results for: ping_pong_unequal
                                        STUDENT   REFERENCE   PERF?
[Serial]                                1126.19   1109.329    1.02  (OK)
[Parallel + Always Spawn]               259.271   260.822     0.99  (OK)
[Parallel + Thread Pool + Spin]         199.088   198.013     1.01  (OK)
[Parallel + Thread Pool + Sleep]        198.777   214.293     0.93  (OK)
================================================================================
Executing test: recursive_fibonacci...
Reference binary: ./runtasks_ref_linux
Results for: recursive_fibonacci
                                        STUDENT   REFERENCE   PERF?
[Serial]                                1052.273  1128.069    0.93  (OK)
[Parallel + Always Spawn]               156.014   172.113     0.91  (OK)
[Parallel + Thread Pool + Spin]         156.31    171.337     0.91  (OK)
[Parallel + Thread Pool + Sleep]        156.462   166.476     0.94  (OK)
================================================================================
Executing test: math_operations_in_tight_for_loop...
Reference binary: ./runtasks_ref_linux
Results for: math_operations_in_tight_for_loop
                                        STUDENT   REFERENCE   PERF?
[Serial]                                411.426   423.96      0.97  (OK)
[Parallel + Always Spawn]               537.747   532.353     1.01  (OK)
[Parallel + Thread Pool + Spin]         99.286    104.844     0.95  (OK)
[Parallel + Thread Pool + Sleep]        95.817    239.76      0.40  (OK)
================================================================================
Executing test: math_operations_in_tight_for_loop_fewer_tasks...
Reference binary: ./runtasks_ref_linux
Results for: math_operations_in_tight_for_loop_fewer_tasks
                                        STUDENT   REFERENCE   PERF?
[Serial]                                413.681   415.961     0.99  (OK)
[Parallel + Always Spawn]               514.021   505.234     1.02  (OK)
[Parallel + Thread Pool + Spin]         108.644   117.702     0.92  (OK)
[Parallel + Thread Pool + Sleep]        106.84    260.724     0.41  (OK)
================================================================================
Executing test: math_operations_in_tight_for_loop_fan_in...
Reference binary: ./runtasks_ref_linux
Results for: math_operations_in_tight_for_loop_fan_in
                                        STUDENT   REFERENCE   PERF?
[Serial]                                212.534   211.52      1.00  (OK)
[Parallel + Always Spawn]               76.402    76.09       1.00  (OK)
[Parallel + Thread Pool + Spin]         37.203    39.662      0.94  (OK)
[Parallel + Thread Pool + Sleep]        36.523    57.039      0.64  (OK)
================================================================================
Executing test: math_operations_in_tight_for_loop_reduction_tree...
Reference binary: ./runtasks_ref_linux
Results for: math_operations_in_tight_for_loop_reduction_tree
                                        STUDENT   REFERENCE   PERF?
[Serial]                                208.076   207.488     1.00  (OK)
[Parallel + Always Spawn]               45.054    45.227      1.00  (OK)
[Parallel + Thread Pool + Spin]         33.079    33.9        0.98  (OK)
[Parallel + Thread Pool + Sleep]        34.502    38.389      0.90  (OK)
================================================================================
Executing test: spin_between_run_calls...
Reference binary: ./runtasks_ref_linux
Results for: spin_between_run_calls
                                        STUDENT   REFERENCE   PERF?
[Serial]                                353.553   382.373     0.92  (OK)
[Parallel + Always Spawn]               180.401   197.119     0.92  (OK)
[Parallel + Thread Pool + Spin]         205.374   222.315     0.92  (OK)
[Parallel + Thread Pool + Sleep]        214.819   197.579     1.09  (OK)
================================================================================
Executing test: mandelbrot_chunked...
Reference binary: ./runtasks_ref_linux
Results for: mandelbrot_chunked
                                        STUDENT   REFERENCE   PERF?
[Serial]                                257.289   256.815     1.00  (OK)
[Parallel + Always Spawn]               34.395    34.058      1.01  (OK)
[Parallel + Thread Pool + Spin]         34.241    34.922      0.98  (OK)
[Parallel + Thread Pool + Sleep]        35.191    35.273      1.00  (OK)
================================================================================
Overall performance results
[Serial]                                : All passed Perf
[Parallel + Always Spawn]               : All passed Perf
[Parallel + Thread Pool + Spin]         : All passed Perf
[Parallel + Thread Pool + Sleep]        : All passed Perf
```

## part_b

在任务的 B 部分中，您将扩展您的 A 部分任务系统实现，以支持可能依赖于以前任务的任务的异步启动。这些任务间依赖关系创建了任务执行库必须遵守的调度约束。

ITaskSystem 接口还有一个方法:

```C++
virtual TaskID runAsyncWithDeps(IRunnable* runnable, int num_total_tasks,
                                const std::vector<TaskID>& deps) = 0;
```

RunAsyncWithDeps ()类似于 run () ，因为它也用于执行 num _total_ asks 任务的批量启动。但是，它与 run ()在许多方面有所不同...

### Asynchronous Task Launch

首先，使用 runAsyncWithDeps ()创建的任务由任务系统与调用线程异步执行。

这意味着 runAsyncWithDeps ()应该立即返回给调用方，即使任务尚未完成执行。

该方法返回与此批量任务启动关联的唯一标识符。

调用线程可以通过调用 sync ()来确定大容量任务启动的实际完成时间。

`virtual void sync() = 0;`

只有当与之前所有批量任务启动关联的任务完成时，sync ()才返回给调用方。例如，考虑以下代码:

```C++
// assume taskA and taskB are valid instances of IRunnable...

std::vector<TaskID> noDeps;  // empty vector

ITaskSystem *t = new TaskSystem(num_threads);

// bulk launch of 4 tasks
TaskID launchA = t->runAsyncWithDeps(taskA, 4, noDeps);

// bulk launch of 8 tasks
TaskID launchB = t->runAsyncWithDeps(taskB, 8, noDeps);

// at this point tasks associated with launchA and launchB
// may still be running

t->sync();

// at this point all 12 tasks associated with launchA and launchB
// are guaranteed to have terminated
```

如上面的注释中所述，在线程调用sync() runAsyncWithDeps() ) 的任务已完成。 准确地说， runAsyncWithDeps()告诉您的任务系统执行新的批量任务启动，但您的实现可以灵活地在下次调用sync()之前随时执行这些任务。 请注意，此规范意味着无法保证您的实现在从 launchB 启动任务之前先执行 launchA 中的任务！

### Support for Explicit Dependencies

runAsyncWithDeps()的第二个关键细节是它的第三个参数：TaskID 标识符向量，必须引用之前使用runAsyncWithDeps()启动的批量任务。 该向量指定当前批量任务启动中的任务所依赖的先前任务。 因此，在依赖向量中给出的启动中的所有任务完成之前，您的任务运行时无法开始执行当前批量任务启动中的任何任务！ 例如，考虑以下示例：

```C++
std::vector<TaskID> noDeps;  // empty vector
std::vector<TaskID> depOnA;   
std::vector<TaskID> depOnBC;   

ITaskSystem *t = new TaskSystem(num_threads);

TaskID launchA = t->runAsyncWithDeps(taskA, 128, noDeps);    
depOnA.push_back(launchA);

TaskID launchB = t->runAsyncWithDeps(taskB, 2, depOnA);
TaskID launchC = t->runAsyncWithDeps(taskC, 6, depOnA);
depOnBC.push_back(launchB);
depOnBC.push_back(launchC);

TaskID launchD = t->runAsyncWithDeps(taskD, 32, depOnBC);            
t->sync();
```

上面的代码有四个批量任务启动（taskA：128 个任务，taskB：2 个任务，taskC：6 个任务，taskD：32 个任务）。 请注意，任务 B 和任务 C 的启动取决于任务 A。 taskD 的批量启动 ( launchD ) 取决于launchB和launchC的结果。 因此，虽然您的任务运行时可以按任意顺序（包括并行）处理与launchB和launchC关联的任务，但这些启动中的所有任务必须在launchA的任务完成后开始执行，并且它们必须在运行时开始之前完成从launchD执行任何任务。

我们可以通过任务图直观地说明这些依赖关系。 任务图是有向无环图 (DAG)，其中图中的节点对应于批量任务启动，从节点 X 到节点 Y 的边表示 Y 对 X 输出的依赖关系。上述代码的任务图是：
![Alt text](https://github.com/jeremyephron/asst2/raw/master/figs/task_graph.png)

请注意，如果您在具有八个执行上下文的 Myth 计算机上运行上面的示例，则并行调度launchB和launchC中的任务的能力可能非常有用，因为单独的批量任务启动都不足以使用所有执行机器的资源。

### Task

您必须从 A 部分扩展任务系统实现，才能正确实现TaskSystem::runAsyncWithDeps()和TaskSystem::sync() 。 与 A 部分一样，我们为您提供以下入门提示：

- It may be helpful to think about the behavior of runAsyncWithDeps() as pushing a record corresponding to the bulk task launch, or perhaps records corresponding to each of the tasks in the bulk task launch onto a "work queue". Once the record to work to do is in the queue, runAsyncWithDeps() can return to the caller.
- The trick in this part of the assignment is performing the appropriate bookkeeping to track dependencies. What must be done when all the tasks in a bulk task launch complete? (This is the point when new tasks may become available to run.)
- It can be helpful to have two data structures in your implementation: (1) a structure representing tasks that have been added to the system via a call to runAsyncWithDeps(), but are not yet ready to execute because they depend on tasks that are still running (these tasks are "waiting" for others to finish) and (2) a "ready queue" of tasks that are not waiting on any prior tasks to finish and can safely be run as soon as a worker thread is available to process them.
- You need not worry about integer wrap around when generating unique task launch ids. We will not hit your task system with over 2^31 bulk task launches.
- You can assume all programs will either call only run() or only runAsyncWithDeps(); that is, you do not need to handle the case where a run() call needs to wait for all proceeding calls to runAsyncWithDeps() to finish.

在part_b/子目录中实现B部分实现，以与正确的参考实现（ part_b/runtasks_ref_* ）进行比较。