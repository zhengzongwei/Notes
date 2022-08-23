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



