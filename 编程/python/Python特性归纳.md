## 单例模式

```python

class Singleton(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance

    def __init__(self):
        print("我是Singleton")


if __name__ == "__main__":
    obj1 = Singleton()
    obj2 = Singleton()
    print(id(obj1))
    print(id(obj2))
```

### 运行结果

```python
我是Singleton
我是Singleton
4301512608
4301512608
```

## 装饰器

### 无参装饰器

```py
def log(func):
    print("111")

    def wrapper():
        print("222")
        func()  # 不带返回值的装饰器
        # return func() # 带有返回值的装饰器

    print("333")
    return wrapper


@log
def g():
    print("444")
    return 'ggg'


if __name__ == '__main__':
    print(g())


```

#### 运行结果

```shell
# 不带返回值
111
333
222
444
None

# 带返回值
111
333
222
444
ggg
```

### 有参装饰器

```python
def log(level='INFO'):
    print(111)

    def _log(func):
        print(222)

        def wrapper(num):
            print(333)
            print(level)
            print(num)
            return func(num)

        print(555)
        return wrapper

    print(444)
    return _log


@log("sds")
def g(num):
    print("fff")
    return 'ggg'
```

#### 运行结果

```shell
111
444
222
555
333
sds
sd
fff
ggg
```



