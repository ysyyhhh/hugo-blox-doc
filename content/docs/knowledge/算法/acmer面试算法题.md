# 写在前面

笔试上机题型基本是经典算法题，且难度最多leetcode hard。但面试的题目类型很多，如场景题、NP问题等没有最优解的问题。

以下对求职面试算法题做整理，主要面向ACMer，是对比赛中不常见的算法题的补充。

篇幅有限，仅给出简要思路，正解代码可选择该篇，或者自行搜索。背代码没用，经过思考后自己写一遍，面试时才能写出来。

# 经典算法题

## 链表

```C++
struct node {
    int x_;
    node* nex_ = nullptr; //需要初始化
    node(int x)
    {
        x_ = x;
    }
    node() { }
};
```

### 链表翻转 空间O(1) 时间O(n)
[例题](https://leetcode.cn/problems/reverse-linked-list-ii/)

### 归并排序链表O(n) 时间O(nlogn)
[例题](https://www.luogu.com.cn/problem/P1177)
```C++

node* merge(node* ha, node* hb)
{
    node* head = new node();
    node* now = head;
    node* na = ha->nex_;
    node* nb = hb->nex_;
    while (na != nullptr && nb != nullptr) {
        if (na->x_ < nb->x_) {
            now->nex_ = na;
            na = na->nex_;
        } else {
            now->nex_ = nb;
            nb = nb->nex_;
        }
        now = now->nex_;
    }
    if (na != nullptr) {
        now->nex_ = na;
    }
    if (nb != nullptr) {
        now->nex_ = nb;
    }
    return head;
}
node* sort(node* head)
{

    if (head->nex_ == nullptr || head->nex_->nex_ == nullptr)
        return head;
    // traverse(head);
    //split 交替
    node* ha = head;
    node* hb = new node();

    node* now = head->nex_;
    node* nb = hb;
    node* na = ha;
    bool oe = 0;
    while (now != nullptr) {
        if (oe) {
            nb->nex_ = now;
            nb = now;
        } else {
            na->nex_ = now;
            na = now;
        }
        now = now->nex_;
        oe = !oe;
    }
    na->nex_ = nullptr;
    nb->nex_ = nullptr;

    hb = sort(hb);
    ha = sort(ha);

    // return head;
    return merge(ha, hb);
}

```
## 数据结构(树状数组)

### 单点加,区间和
[树状数组1例题](https://www.luogu.com.cn/problem/P3368)
```C++
#include <cstdio>
#include <iostream>
using namespace std;
typedef long long ll;
const int N = 1e6 + 7;

int n;
int a[N], t[N];

inline int lowbit(int x)
{
    return x & -x;
}
void add(int k, int x)
{
    for (k; k <= n; k += lowbit(k)) {
        t[k] += x;
    }
}
int sum(int r)
{
    int res = 0;
    for (r; r > 0; r -= lowbit(r)) {
        res += t[r];
    }
    return res;
}
int sum(int l, int r)
{
    return sum(r) - sum(l - 1);
}

void build()
{
    //O(n)
    for (int i = 1; i <= n; i++) {
        t[i] += a[i];
        int j = i + lowbit(i);
        if (j <= n) {
            t[j] += t[i];
        }
    }
}

int main()
{
    int m;
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        scanf("%d", &a[i]);
    }
    build();
    for (int i = 1; i <= m; i++) {
        int op;
        scanf("%d", &op);
        if (op == 1) {
            int x, k;
            scanf("%d%d", &x, &k);
            add(x, k);
        } else {
            int l, r;
            scanf("%d%d", &l, &r);
            printf("%d\n", sum(l, r));
        }
    }
    return 0;
}
```

### 区间改,单点查
[树状数组2例题](https://www.luogu.com.cn/problem/P3368)

把原数组不做任何处理.
树状数组维护一个前缀和数组(初始为0).

把区改变成端点处的单改
单查变成区查

```C++
#include <cstdio>
#include <iostream>
using namespace std;
typedef long long ll;
const int N = 1e6 + 7;

int n;
int a[N], t[N];

inline int lowbit(int x)
{
    return x & -x;
}
void add(int k, int x)
{
    for (k; k <= n; k += lowbit(k)) {
        t[k] += x;
    }
}
void add(int l, int r, int x)
{
    //要使得 sum(r) - sum(l-1) 加了x的话，需要在l处+x，同时在r+1处-x
    add(l, x);
    add(r + 1, -x);
}
ll sum(int r)
{
    ll res = 0;
    for (r; r > 0; r -= lowbit(r)) {
        res += t[r];
    }
    return res;
}
int main()
{
    int m;
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        scanf("%d", &a[i]);
    }
    for (int i = 1; i <= m; i++) {
        int op;
        scanf("%d", &op);
        if (op == 1) {
            int x, y, k;
            scanf("%d%d%d", &x, &y, &k);
            add(x, y, k);
        } else {
            int x;
            scanf("%d", &x);
            printf("%lld\n", a[x] + sum(x));
        }
    }
    return 0;
}
```
## 排序

[例题](https://www.luogu.com.cn/problem/P1177)

### 手写快排

### 归并排序(求逆序对)

[求逆序对](https://www.luogu.com.cn/problem/P1908)
```C++
#include <cstdio>
#include <iostream>
using namespace std;
typedef long long ll;
const int N = 5e6 + 7;

ll ans;

int tmp[N], a[N];

void merge(int* a, int l, int r, int mid)
{
    int ti = l;
    int li = l, ri = mid + 1;
    while (li <= mid && ri <= r) {
        int lw = a[li], rw = a[ri];
        if (lw <= rw) {
            tmp[ti++] = a[li++];
        } else {
            tmp[ti++] = a[ri++];
            //按理来说，右边的数组应该在左边所有都放完再放
            //因此，如果提前放了，那么剩下左边有多少个没放的 都 和它组成一个逆序对
            //即 mid-li+1
            ans += mid - li + 1;
        }
    }
    while (li <= mid)
        tmp[ti++] = a[li++];
    while (ri <= r)
        tmp[ti++] = a[ri++];

    for (int i = l; i <= r; i++) {
        a[i] = tmp[i];
    }
}

void sort(int* a, int l, int r)
{
    if (l >= r)
        return;
    // cout << l << " " << r << endl;
    int mid = (l + r) / 2;
    sort(a, l, mid);
    sort(a, mid + 1, r);
    merge(a, l, r, mid);
}
int main()
{
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        scanf("%d", &a[i]);
    }

    sort(a, 1, n);

    cout << ans;

    return 0;
}
```

### 第k大数 O(n)
[例题](https://leetcode.cn/problems/kth-largest-element-in-an-array/)
补充: 第K大数,而不是第K个不同的数.

和求排序后的第k个数本质一致,转换一下即可.

#### 思路

回忆一下二分法和快排:

- 二分法形成一棵二叉树. 每层所有序列长度总和为n, 二叉树高度为h, 时间复杂度为 O(n*h)

- 最优的情况: 每个结点的左儿子和右儿子序列长度相等. h = logn, 时间复杂度为O(n*logn)
- 因此快排最优是O(n*logn)

#### 如何优化到O(n)

显然, 对于求排序后第k个数. 在二分时,每次可以只选择一个儿子继续搜索.

即在最优情况下,每次二分结果为 l,mid,r

- mid == k ,答案就是a[mid]
- mid > k, 只需要继续在 (l,mid-1)中搜
- mid < k, 只需要继续在 (mid+1,r)中搜

因此与快排形成的二叉树不同. 该方法每层的搜索总长度是递减的.

即 n + n/2 + n/4 + n/8 + ... 

易得上述公式的近似为 2*n, 时间复杂度O(n)



## 串

### [字符串全排列](https://leetcode.cn/problems/zi-fu-chuan-de-pai-lie-lcof/)



### 最长回文子串-- O(n)

思路:[马拉车算法](https://blog.csdn.net/qq_51116518/article/details/117370554) 

#### 证明O(n):

即证while内的p[i]++ 执行次数总和为O(n)级别

首先考虑什么情况下才需要进入while循环

- i < mx, 且 i  为 id 所在回文串的右四等分点之后.
  - 此时p[i]是以mx-i 开始增加, 即i + p[i] >= mx
  - 也就是while内的操作每执行一次 mx++
- i > mx, 无法使用之前的预处理.
  - while内的操作没执行一次 mx++

可知while的操作次数等于 mx从0加到n-1的次数, 因此while内操作次数的总和为n

总时间复杂度 O(n)





## 动态规划(非背包)

### 最长公共连续子序列 O(nm)

### 最长上升子序列 O(nlogn)

思路:动态规划+二分



## 背包类

货币面值组成

### [砝码称重](https://www.acwing.com/problem/content/description/3420/) O(n * s)

题意：有天平和 N 个砝码重量是 Wi。可以称出多少种不同的重量？砝码可以放在天平两边。

N<100 ,Σwi < 1e5

思路：

01背包， 称重为i的可以从 abs(i-w) ， i+w 中转移。 不过要注意开个滚动数组防止重复放砝码。



## 数学题

#### 小凯的疑惑





# STL用法


[Vector代替平衡树](https://www.luogu.com.cn/article/ig60mcky)
1.插入一个数 x。
2.删除一个数 x(若有多个相同的数，应只删除一个)
3.查询 x 的排名(定义排名为比当前数小的数的个数+1)
4.查询数据结构中排名为 x 的数。
5.求 x 的前驱(前驱定义为小于x，且最大的数)
6.求 x 的后继(后继定义为大于x，且最小的数)

```C++
scanf("%d%d",&op,&x);
if(op==1)
    s.insert(upper_bound(s.begin(),s.end(),x),x);
if(op==2)
    s.erase(lower_bound(s.begin(),s.end(),x));
if(op==3)
    printf("%d\n",lower_bound(s.begin(),s.end(),x)-s.begin()+1);
if(op==4)
    printf("%d\n",s[x-1]);
if(op==5)
    printf("%d\n",*--(lower_bound(s.begin(),s.end(),x)));
if(op==6)
    printf("%d\n",*(upper_bound(s.begin(),s.end(),x)));
```

vector的查找和插入

```C++
bool cmp(int a1,int a2){
  return a1 > a2;
}
vector<int>a;
int in = lower_bound(a.begin(),a.end(),x,cmp) - a.begin();
```


# 思维题

#### 小球称重问题

8个小球，其中1个偏重，1个天平，要秤几次才能找到重的球？

2次 
- 两边各放3个
  - 如果相同重
    - 剩下两个第二次必测得出
  - 如果其中第一次其中一边重的话
    - 就把那3个挑两个出来
    - 如果一样重剩下那个就是重 否则直接就测出来
### 开关问题

三个开关放在一个房间里面，另一个房间有灯泡。问你：如何在只进出有灯泡的房间一次，就可以判断出三个开关中具体哪一个是控制该灯泡的

A：打开一个开关，等一会儿，然后关闭它。然后打开另一个开关，然后进入房间。如果灯泡亮着，那么是第二个开关。如果灯泡是暗的，摸一下灯泡。如果灯泡是热的，那么是第一个开关。如果灯泡是冷的，那么是第三个开关。

# NP问题

## 集合覆盖问题




# 杂项

### [随机加权采样算法 alias](https://leetcode.cn/problems/random-pick-with-weight/)

https://www.cnblogs.com/Lee-yl/p/12749070.html



# 杂谈后话

写一点求职的经验和所见所闻吧！**不保证时效性和真实性，参考与否自行斟酌**。

**面评记录对求职的影响**：

- 针对人群：想**刷面试经验**，而**不是真正急着找工作的**。
- 请**珍惜每次面试机会**，尤其是面试喜欢的公司时。
- 面试一般都会有记录和面试评价。
- 所见所闻：大佬A大二时投递了理想公司的实习，意图刷该公司的面试经验。结果表现不佳，导致在真正需要找实习的时候，因之前的面评太差，导致没过简历/排序靠后（记不太清了）













