# 1. 初识C语言

## 1.1 C语言的起源

C语言是在B语言的基础上设计而来。

C语言的设计初衷是将其作为程序员使用的一种编程工具，因此，其主要目标是成为又用的语言。

## 1.2 C语言的特性

- 设计特性

  C语言融合了计算机科学理论和实践的控制特性，C语言的设计理念让用户能轻松的完成自顶向下的规划、结构化编程和模块化设计

- 高效性

- 可移植性

- 缺点

  C语言使用指针，而涉及指针的编程错误往往难以察觉

## 1.3 C语言的应用范围



## 1.4 使用C语言的7个步骤

- 定义程序的目标
- 设计程序
- 编写代码
- 编译
- 运行程序
- 测试和调试程序
- 维护和修改代码

# 2.C语言概述

## 2.1 简单C语言示例

### 2.1.1 提高函数可读性的技巧

- 定义有意义的函数名
- 写注释
- 在函数中用空行分隔概念上的多个部分
- 每条语句占一行

```
 #include <stdio.h>
 int main(int argc, char const *argv[]) // 函数头
   
 {
     int num;
     num =1;
     printf("Hello world");
     return 0;
 }   // 函数体
```

### 2.1.2 多条变量声明

```
 int feet,fathoms ==> int feet; int fathoms;
```

### 2.1.3 关键字和保留标识符

```
 auto  break  case  char  const  continue  default  do  double  else  enum  extern  float  for  goto  if    int  long  register  return  short  signed  sizeof  static    struct  switch  ypedef  union  unsigned  void   volatile   while
 1999年12月16日，ISO推出了C99标准，该标准新增了5个C语言关键字：
 inline   restrict   _Bool     _Complex     _Imaginary
 2011年12月8日，ISO发布C语言的新标准C11，该标准新增了7个C语言关键字：
 _Alignas   _Alignof    _Atomic    _Static   _assert     _Noreturn     _Thread    _local    _Generic
   auto ：声明自动变量
 break：跳出当前循环
 case：开关语句分支
 char ：声明字符型变量或函数返回值类型
 const ：声明只读变量
 continue：结束当前循环，开始下一轮循环
 default：开关语句中的“默认”分支
 do ：循环语句的循环体
 double ：声明双精度浮点型变量或函数返回值类型
 else ：条件语句否定分支（与 if 连用）
 enum ：声明枚举类型
 extern：声明变量或函数是在其它文件或本文件的其他位置定义
 float：声明浮点型变量或函数返回值类型
 for：一种循环语句
 goto：无条件跳转语句
 if:条件语句
 int： 声明整型变量或函数
 long ：声明长整型变量或函数返回值类型
 register：声明寄存器变量
 return ：子程序返回语句（可以带参数，也可不带参数）
 short ：声明短整型变量或函数
 signed：声明有符号类型变量或函数
 sizeof：计算数据类型或变量长度（即所占字节数）
 static ：声明静态变量
 struct：声明结构体类型
 switch :用于开关语句
 typedef：用以给数据类型取别名
 unsigned：声明无符号类型变量或函数
 union：声明共用体类型
 void ：声明函数无返回值或无参数，声明无类型指针
 volatile：说明变量在程序执行中可被隐含地改变
 while ：循环语句的循环条件
```

# 3. 数据和C

## 3.1 示例程序

```c
#include <stdio.h>

int main(void){
    float weight; // 体重
    float value;  // 相等重量得到白金价值
    printf("请输入\n ");
    scanf("%f",&weight);
    /*
    假设白金价格为 $1700 
    14.5833用于把英镑常恒盎司转化为金衡盎司
    */
    value =  1700 * 14.5833 * weight;
    printf("%2.f",value);
    return 0;
}
```

## 3.2 变量与常量数据

- **常量** ：在程序运行前已经定义好，在整个程序的运行中没发生变化
- **变量**：在程序运行中可能会被改变或赋值

## 3.3 数据：数据类型关键字

| 最初 K&R 给出的关键字 | C90 标准添加的关键字 | C99 标准添加的关键字 |
| --------------------- | -------------------- | -------------------- |
| int                   | signed               | _Bool                |
| long                  | void                 | _Complex             |
| short                 |                      | _Imaginary           |
| unsigned              |                      |                      |
| char                  |                      |                      |
| float                 |                      |                      |
| double                |                      |                      |

通过这些关键字创建的类型，按计算机的存储方式可分为两大基本类型：**整数类型和浮点数类型**

> 位、字节、字
>
> 最小的存储单元是位（bit）
>
> 字节（byte）是常用的计算机存储单位
>
> 字（word）是设计计算机时给定的自然存储单位

### 3.3.1 整数与浮点数

#### 3.3.1.1 整数

整数是没有小数点部分的数，计算机以二进制数字存储整数。

#### 3.3.1.2 浮点数

浮点数与整数的存储方案不同，计算机把浮点数分为小数部分和指数部分来表示，其中 10^7=10000000 7被称为10的指数

### 整数与浮点数区别

- 整数没有小数部分，浮点数有小数部分
- 浮点数可以表示的范围比整数大
- 对于一些算术运算，浮点数损失的精度更多

## 3.4 C语言的数据类型

### 3.4.1 int 类型

> int 类型是有符号的整形，即int类型的值必须我为整数，取值范围因计算机系统而异。一般而言，存储一个int要占用一个机器字长。因此早起的16位IBM PC 兼容机使用一个16位来存储一个int值，取值范围为 -32768-32767，目前个人计算机一般是32位，所以使用32位来存储一个int 值
>
> ISO 规定int 类型的取值范围为 -32768-32767

#### 3.4.1.1 声明int变量

```c
int erns; // 单个声明
int hogs,cows,goats; // 多个声明
```

#### 3.4.1.2 初始化变量

> 初始化变量就是为一个变量赋一个初始值。

```c
// 初始化变量
int hogs =21；
int cows = 32；goats = 14；
int dogs，cats = 94 // 不推荐  
```

### 3.4.1.3 基本数据类型

> 基本数据类型由11个关键字组成：int,long,short,unsigned,char,float,double,singed,_Bool,_Complex,_Imaginary

#### 有符号类型

> 有符号整型可用于表示正整数和负整数

- int ：系统化给定的基本类型,C语言规定`int`类型不小于16位
- short或short int ：最大的`short类型整数`小于最大的`int类型整数`,C语言规定`short类型`不小于16位
- long 或long int：该类型可表示的整数大于或等于最大的`int类型整数`,C语言规定`long类型`至少占32位
- long long或long long int：该类型可表示的整数大于或等于最大的`long类型整数`,C语言规定`long long类型`至少占64位

#### 无符号整型

> 无符号类型只能用于表示零和正整数，在整数类型加上关键字 `unsigned`表明该类型为无符号类型

#### 字符类型

> 可打印出来的符号都是字符，根据定义，char类型表示一个字符占用1字节内存。出于历史原因，1字节通常表示8位，但是如果表示基本字符集，也可以是16位或者更大。

- char ：字符类型关键字，有些编译器使用有符号的char，有些使用无符号的char，在需要时，可加上关键字 signed 或unsigned 来表明具体使用哪一类型。

#### 布尔类型

> 布尔值表示 true 或false。C语言用1表示true，0表示false

- _Bool：布尔类型的关键字。

#### 实浮点类型

> 实浮点类型可表示正浮点数和负浮点数

- float：系统的基本浮点类型，可精确表示6位有效数字
- double：存储浮点数的范围更大，能表示比float类型更多的有效数字和更大的指数

- long double：存储浮点数比double的范围更大

#### 复数和虚数浮点数

> 虚数类型是可选的类型，复数的实部和虚部类型都基于实浮点类型来构成

- float _Complex
-  double _Complex

- long double _Complex
- float _Imaginary
-  double _Imaginary
- long double _Imaginary



