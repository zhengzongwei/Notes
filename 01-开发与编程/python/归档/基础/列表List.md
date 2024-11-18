# 列表 的相关操作(CRUD)

## 列表的特点

1.有序的

2.可变的

``` Python
# 定义一个列表
# 方法一
my_list = list()
# 方法二
my_list = []
```

### 1. 增加元素

- insert

    Insert(要添加的索引,要添加的元素)

- append

    Append() 会把元素添加在列表的末端

- extend

    会把元素迭代(遍历)添加到列表中

### 2. 查找元素

- in not in 返回布尔值
- index

    index(元素,start,stop) 返回 该元素的索引

- count

### 3. 删除元素

- Del()

    Del() 根据下标索引删除

    Del 列表名[索引]

- Pop()

    Pop()有两种用法

    1. Pop()直接删除列表最后的值
    2. Pop(列表索引)

- Remove()

    Remove()根据列表的值进行删除

- Clear()

    Clear()清空元素,返回一个空列表

### 4. 排序

- sort

``` python
my = [ 2, 3, 5, 7, 2, 0]
# 升序
my.sort()
print(my)

# 降序
my.sort(reverse=True)
print(my)

# 列表的数据逆置
ret = reversed(my)
print(list(ret))
my = [ 2, 3, 5, 7, 2, 0]
ret1 = reversed(my)
print(list(ret1))
# 结果: [0, 2, 7, 5, 3, 2]
```

### 列表的嵌套应用

``` Python

# 一个学校，有3个办公室，现在有8位老师等待工位的分配，请编写程序，完成随机的分配

# 方法一
import random
teacher = 'ABCDEFGH'
box = [[], [],[]]
for name in teacher:
    index = random.randint(0,2)
    box[index].append(name)
print(box)

# 方法二
import random

# 定义一个列表用来保存3个办公室
offices = [[],[],[]]

# 定义一个列表用来存储8位老师的名字
names = ['A','B','C','D','E','F','G','H']

i = 0
for name in names:
    index = random.randint(0,2)
    offices[index].append(name)

i = 1
for tempNames in offices:
    print('办公室%d的人数为:%d'%(i,len(tempNames)))
    i+=1
    for name in tempNames:
        print("%s"%name,end='')
    print("\n")
    print("-"*20)

# 随机放球问题
# 有10个球分别3红、3蓝、4白，现需要将这10个球放入这3个盒子，要求每个盒子至少有一个白球，请用程序实现
#提示：
# 使用嵌套列表模拟三个盒子
# 先向每个盒子放入一个白球，然后再遍历剩余的球随机放入一个盒子里

# 方法一
import random
balls='hhhlllbbbb'
box = [[], [], []]
for ball in balls:
    if ball =='b':
        if 'b' not in box[0]:
            box[0].append(ball)
        elif 'b' not in box[1]:
            box[1].append(ball)
        elif'b' not in box[2]:
            box[2].append(ball)
        else:
             box[index].append(ball)
    else:
        index = random.randint(0,2)
        box[index].append(ball)
else:
    print(box)
# 方法二

import random
# 定义一个列表用来保存3个盒子
boxs = [[],[],[]]
# 定义一个列表用来存放10个球
balls = ['w','w','w','w','r','r','r','b','b','b']

# 判断条件,把球添加到盒子里面
i = 0
for ball in balls:
    if ball == "w" and i < 3:
        if i == 0:
            boxs[0].append(ball)
        if i == 1:
            boxs[1].append(ball)
        if i == 2:
            boxs[2].append(ball)
        i += 1
    else:
        index = random.randint(0,2)
        boxs[index].append(ball)
print(boxs)

```
