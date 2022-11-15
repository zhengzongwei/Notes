# 字符串的相关总结

## 字符串的特点

    1. 不可变
    2. 有序
    3. 可以储存多个字符

## 切片

**切片语法** [起始:结束:步长]

## 字符串操作

### Find Rfind

    find检查字符是否包含在字符串中,如果有 返回开始的索引值,如果没有返回 -1
    
    Rfind 和find类似 从右边开始查找

``` Python
>>> str = 'hello world'
>>> ret = str.find('k')
>>> print(ret)
结果:-1
>>> ret = str.find('l')
>>> ret
结果:2
>>>
```