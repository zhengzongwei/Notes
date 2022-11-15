# RESTframework

## Web应用模式

### 前后端不分离

![前后端不分离](REST.images/%E5%89%8D%E5%90%8E%E7%AB%AF%E4%B8%8D%E5%88%86%E7%A6%BB.png)
过程: 浏览器请求动态页面 --> 后端服务器响应(查询数据库,渲染模板)

前端页面看到的效果都是由后端控制,后端渲染页面或重定向

后端控制前端的展示,前端后端的耦合性很高.

这种应用模式只适用于纯网页应用,当后端对接APP时,App可能不需要后端网页,而只是需要数据,所有不适用,需要重新开发接口.

### 前后端分离

![前后端分离](REST.images/%E5%89%8D%E5%90%8E%E7%AB%AF%E5%88%86%E7%A6%BB.png)

在前后端分离的应用模式中,后端仅返回前端所需的数据，不再渲染HTML页面，不再控制前端的效果.

在前后端分离的应用模式中,前端与后端的耦合度相对较低.

在前后端分离的应用模式中，我们通常将后端开发的每个视图都称为一个接口，或者API，前端通过访问接口来对数据进行增删改查.

## RESTful

### RESTful 特点

get 查询

post 增加

put 修改

delete 删除

- 每个URL代表一种资源
- 客户端和服务器之前,传递这种资源的耨中表现层
- 客户端同坐HTTP动词,对服务器端资源进行操作,实现'表现层状态转化'

## REST接口开发的核心任务

- 将请求的数据(JSON格式)转化为模型对象
- 操作数据库
- 将模型对象转化为响应的数据(JSON)

序列化: 将Python类型转化为JSON数据

反序列化: 将JSON数据转化为Python数据

### 总结

开发REST API ,视图操作

- 将数据库序列化为前端所需要的格式,并返回
- 将前端的数据反序列化为模型类对象,并保存到数据库中

## REST framework

特点:

- 提供了定义序列化器Serializer的方法，可以快速根据 Django ORM 或者其它库自动序列化/反序列化；
- 提供丰富的类视图,Mixin扩展类,简化视图的编写
- 丰富的定制层级:函数视图,类视图,视图集合到自动生成API,满足各种需要
- 多种身份认证和权限认证的支持
- 内置限流系统
- 直观的API web 界面
- 可扩展性,插件丰富

### 创建 REST framework 工程

1. 安装DRF

    pip install djangorestframework
2. 添加rest_framework应用

    setting.py

        ``` python
            INSTALLED_APPS = [
            ...
            'rest_framework',
        ]
        ```

### 序列化器

功能:

    序列化操作: 将Python类型(模型类对象,模型类对象的列表)转换成字典
    反序列化操作: 将json转换成字典

定义序列化器: 继承自rest_framework.serializers.Serializer类

``` python
模型类

class BookInfo(models.Model):
    btitle = models.CharField(max_length=20, verbose_name='名称')
    bpub_date = models.DateField(verbose_name='发布日期', null=True)
    bread = models.IntegerField(default=0, verbose_name='阅读量')
    bcomment = models.IntegerField(default=0, verbose_name='评论量')
    image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True

序列化器

class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    btitle = serializers.CharField(label='名称', max_length=20)
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)

视图中使用
from django.http import HttpResponse
from books.models import BookInfo,HeroInfo
from .serializers import BookInfoSerializers,HeroInfoSerializers


def books(request):
    # # 单一对象的序列化
    # book = BookInfo.objects.get(pk=1)
    # book_serializers = BookInfoSerializers(book)
    # book_dict = book_serializers.data
    # print(book_dict)

    # 多对象的序列化
    # book_dict= BookInfoSerializers(BookInfo.objects.all(),many=True).data
    # print(book_dict)

    hero_dict = HeroInfoSerializers(HeroInfo.objects.all(),many=True).data
    print(hero_dict)


    return HttpResponse('OK')
```

注意：serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义。serializer是独立于数据库之外的存在。

#### 序列化操作

1. 基本使用
    1) 查询一个图书对象
    2) 构造序列化器对象
    3) 获取序列化数据,如果获取的是多条数据,添加many=True 参数补充说明

    ``` python
    def books(request):
        # # 单一对象的序列化
        book = BookInfo.objects.get(pk=1)
        book_serializers = BookInfoSerializers(book)
        book_dict = book_serializers.data
        print(book_dict)
    
        # 多对象的序列化
        book_dict= BookInfoSerializers(BookInfo.objects.all(),many=True).data
        print(book_dict)
    ```

2. 关联对象嵌套序列化

    ``` Python
    # 关联对象嵌套序列化
    
    # 1.主键形式输出
    # {'name': '乔峰', 'gender': True, 'comment': '降龙十八掌', 'book_id': 2, 'book': 2}
    # book = serializers.PrimaryKeyRelatedField(label='图书',read_only=True)
    
    # 2.字符串形式输出
    # {'name': '乔峰', 'gender': True, 'comment': '降龙十八掌', 'book_id': 2, 'book': '天龙八部'}
    # book = serializers.StringRelatedField(label='图书',read_only=True)
    
    # 3. 以超链接形式输出
    # {'name': '乔峰', 'gender': True, 'comment': '降龙十八掌', 'book_id': 2, 'book': 'http://127.0.0.1:8000/hero/2'}
    视图中得序列化器添加 # hero_serializer = HeroInfoSerializers(hero,context={'request': request})
    # book = serializers.HyperlinkedRelatedField(label='图书',read_only=True,view_name='books:hero')
    
    # 4.指定对象的某个属性输出
    # {'name': '乔峰', 'gender': True, 'comment': '降龙十八掌', 'book_id': 2, 'book': datetime.date(1995, 12, 16)}
    # book = serializers.SlugRelatedField(label='图书',read_only=True,slug_field='pub_date')
    
    # 5.使用关联对象的序列化器
    # {'name': '乔峰', 'gender': True, 'comment': '降龙十八掌', 'book_id': 2,'book': OrderedDict([('id', 2), ('title', '天龙八部'), ('pub_date', '1995-12-16')])}
    # book = BookInfoSerializers()
    
    # 6. 自定义输出方案
    class BookRelateField(serializers.RelatedField):
    '''自定义处理图书的字段'''
    
    def to_representation(self, value):
        return 'Book: %d-%s' % (value.id, value.title)
    # {'name': '乔峰', 'gender': True, 'comment': '降龙十八掌', 'book_id': 2, 'book': 'Book: 2-天龙八部'}
    # book = BookRelateField(read_only=True)
    
    ```

#### 反序列化操作

1. 验证

    - 字段的类型
    - 必填验证
    - 定义方法
    - 多属性验证
    - 定义类型