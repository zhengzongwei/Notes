# Django项目

## 准备

1. 创建虚拟环境
2. 安装Django包 pip install django==1.11
3. 创建项目 django-admin startproject 项目名称 或直接在pycharm里面创建
4. 运行项目 python manage.py runserver 8000

## 配置

1. 本地化处理

    LANGUAGE_CODE = 'zh-hans'#'en-us'

    TIME_ZONE = 'Asia/Shanghai'#'UTC'

2. 静态文件处理

    STATIC_URL = '/static/'

    STATICFILES_DIRS=[
        os.path.join(BASE_DIR,'static')
    ]

## 静态文件匹配

``` python
http://127.0.0.1:8000/static/images/1.jpg
```

> 如果是以指定字符串开头,则进行静态文件处理
> 如果不是以指定字符串/static/开头,则进行路由匹配

STATIC_URL ='/static/'  ----> /static/images/1.jpg

> 将匹配的字符串去掉,当前为 images/1.jpg

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]

> 将两个字符串进行路径拼接,到磁盘查找这个文件,并返回.

### 问题1：django如何确定请求的是静态文件

    将请求路径与STATIC_URL进行匹配

### 问题2：django如何在磁盘上找到静态文件

    将STATICFILES_DIRS指定的目录与请求文件路径进行拼接

## 创建应用

``` Python
    1. 进入项目目录
    2. python manage.py startapp 应用名称
    3. 在setting.py中安装应用
        INSTALL_APPS = [
            'users.apps.UsersConfig',
        ]
    4. 在应用中创建urls.py 用于配置应用中的路由
        from django.conf.urls import url
        from . import views
        #列表名称的单词是固定的，不能改
        urlpatterns =[
# url('正则表达式',views.视图函数名)
    url(r'index',views.index,name='index')
]

    5. 将应用的路由包含在根路由中
        from django.conf.urls import url,include
        urlpatterns = [
            。。。
            url('^users/',include('users.urls')),
        ]
```

## 定义视图

``` Python
1. 在应用的views.py 中定义函数
    # 必须接受参数request
    def index(request):
    return HttpResponse('hello world')

2. 在urls.py 中定义路由
urlpatterns = [
    # url('正则表达式',views.视图函数名)
    url(r'^index$',views.index),
]
3. 访问 http://127.0.0.1:8000/user/index
```

### 了解路由匹配过程

1. 在根级urls.py 中为namespace 参数指定数值
2. 在应用urls.py 中为url指定name参数
3. 使用reverse('namespace'参数值:'name'参数值) -->生成url字符串

    应用场景: 重定向,超链接

## 从url中获取参数

``` python
1. 在路由规则中提取参数

    # show/10/120
    #url(r'^show/(\d+)/(\d+)$',views.show),#第一个参数赋给a，第二个参数赋给b
    url(r'^show/(?P<b>\d+)/(?P<a>\d+)$',views.show),#将提取的值赋给指定名称的变量

2. 在视图函数中接收参数

    地址: http://127.0.0.1:8000/users/get?a=10&a=22&c=100

    属性request.GET用于获取查询字符串中的数据
    属性类型为django.http.request.QueryDict
    注意：只要参数出现在地址中，使用?***格式，就使用request.GET属性获取与请求方式无关
    类型django.http.request.QueryDict提供的方法
    getlist()：键重复时使用
    get()：键不重复时使用

    # 获取查询字符串的数据
    def get(request):
        dict1 = request.GET
        a = dict1.getlist('a')
        b = dict1.get('b')
        c = dict1.get('c')
        return  HttpResponse('%s-%s-%s' % (a,b,c))

3. 请求体获取参数
    \<from method='post'></from>
    表单,只适用于post请求方式
    # 请求体参数:表单
    def post(request):
        dict1 = request.POST
        a = dict1.getlist('a')
        c = dict1.get('c')
        return HttpResponse('%s-%s' % (a, c))

    通用请求方式 json 格式数据
    注: json 必须使用双引号
    {
    "a":10,
    "a":55,
    "c":"python"
    }

    接收：request.body==>bytes==>.decode()==>json.loads()==>dict

    问：在python中如何将str转换成dict
    答：json
    方法loads()将字符串转换成字典

    方法dumps()将字符转换成字符串

    # 请求参数 json
    def put(request):
        json_data = request.body.decode()
        dict1 = json.loads(json_data)

        a = dict1.get('a')
        # b = dict1.get('b')
        c = dict1.get('c')
        return HttpResponse('%s-%s' % (a, c))
        # return HttpResponse('ok')
```

## 响应对象

    JsonResponse 返回json 格式的数据
    
    JsonResponse(字典)

### 状态保持

1. cookie

    浏览器中存储的键值对的字符串,基于域名安全,浏览器会自动将cookie信息包含在请求头中发给服务器
        写: request.set_cookie(key,value,过期时间(秒)) 如果不设置过期时间,默认关闭浏览器过期
        读: request.COOKIES.get(key)
        删: request.delete_cookie(key)
2. session

    服务器中存储的数据,可以通过&nbsp;setting.py 进行设置,以键值对的格式存储
        写: request.session[key] = value
        读: request.session,get(key)
        默认过期时间 : 2 周

### 设置redis 为django缓存数据库

``` Python

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# 设置session的存储方案：与cache一致
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

```

## 类视图

### 代码实现

1. 在views.py定义类,继承自django.views.View
2. 在类中定义函数,要求请求方式与小写的一致
3. 在urls 中注册路由,调用类的.as_view() 进行注册

### 装饰器的使用

1. 直接在函数上添加装饰器
2. 通过装饰器,装饰类,用于限定某个方法使用指定的装饰器

    文件目录

    ``` python
    .
    └── py3_django
        ├── db.sqlite3
        ├── manage.py
        ├── py3_django
        │   ├── __init__.py
        │   ├── __init__.pyc
        │   ├── settings.py
        │   ├── settings.pyc
        │   ├── urls.py
        │   └── wsgi.py
        └── users
            ├── admin.py
            ├── apps.py
            ├── decorators.py
            ├── __init__.py
            ├── migrations
            │   └── __init__.py
            ├── models.py
            ├── tests.py
            ├── urls.py
            └── views.py

    views.py

        @method_decorator(decorators.register, name='dispatch')
        class RegisterView(View, ):

            def get(self, request):
                return HttpResponse('get')

            def put(self, request):
                return HttpResponse('put')

            def post(self, request):
                return HttpResponse('post')

    decorators.py

        # 定义装饰器
        def register(f):
            def fun(*args,**kwargs):
                print('-'*20)
                return f(*args,**kwargs)
            return fun

    users/urls.py

            url(r'^register/$',views.RegisterView.as_view()),
    ```

3. 可以使用装饰器的原生语法：装饰器(函数)
4. 扩展Mixin(不推荐)

## 中间件

功能类似于 flask 的请求钩子

作用: 当大部分视图都要执行一段代码时,考虑将这些代码卸载中间件里,对于不希望执行此代码的视图,可以在中间件里进行判断

说明: 卸载中间件里的代码,每次请求响应都会执行. 调用外键属性

## 数据库

### 环境配置

1. 准备环境

        pip install pymysql
    
        在django 工程同名子目录的__init__.py 下 添加语句
    
            ```
            from pymysql import install_as_MySQLdb
    
            install_as_MySQLdb()
            ```

2. 配置

    ``` Python
    
    setting.py
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    
    ```
3. 修改DATABASES的配置信息

    ``` python
            DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'HOST': '127.0.0.1',  # 数据库主机
                'PORT': 3306,  # 数据库端口
                'USER': 'root',  # 数据库用户名
                'PASSWORD': 'mysql',  # 数据库用户密码
                'NAME': 'django_demo'  # 数据库名字
            }
        }
    ```
4. 在MySQL中.创建数据库

### 定义模型类

应用model.py

导入模型类

from django.db import models

定义模型类
class 类名称(models.Model):
    属性=models.类型(选项)

``` python
class HeroInfo(models.Model):
    GENDER_CHOICES = (
        (True, '男'),
        (False, '女')
    )
    name = models.CharField(max_length=30, verbose_name='名字')
    gender = models.BooleanField(choices=GENDER_CHOICES, default=False, verbose_name='性别')
    comment = models.CharField(max_length=200, verbose_name='描述信息')
    is_delete = models.BooleanField(default=0, verbose_name='逻辑删除')
    book = models.ForeignKey(BookInfo)

    class Meta:
        db_table = 'tb_heros'
        verbose_name = '英雄'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def book_title(self):
        return self.book.title
    book_title.short_description = '书名'

```

1) 数据库表名

    模型类如果没指定表名,Django默认以小写App应用名_小写模型类名为数据库表名

    可通过 db_table 指定数据库表名
2) 关于主键

    django会自动为表创建自增主键(id),每个模型只能有一个主键列,如果使用选项设置某属性为主键列后,django不会在自动创建自增的主键列

    主键可以使用pk代替.
3) 属性命名限制

    - 不能是 Python 保留关键字
    - 不允许使用连续的下划线,这是由django的查询方式决定的
    - 定义属性需要知名字段类型,通过字段类型的参数指定选项.

        属性=models.字段类型(选项)

4) 字段类型

    | 类型             | 说明                                                         |
    | ---------------- | ------------------------------------------------------------ |
    | AutoField        | 自动增长的IntegerField，通常不用指定，不指定时Django会自动创建属性名为id的自动增长属性 |
    | BooleanField     | 布尔字段，值为True或False                                    |
    | NullBooleanField | 支持Null、True、False三种值                                  |
    | CharField        | 字符串，参数max_length表示最大字符个数                       |
    | TextField        | 大文本字段，一般超过4000个字符时使用                         |
    | IntegerField     | 整数                                                         |
    | DecimalField     | 十进制浮点数， 参数max_digits表示总位数， 参数decimal_places表示小数位数 |
    | FloatField       | 浮点数                                                       |
    | DateField        | 日期， 参数auto_now表示每次保存对象时，自动设置该字段为当前时间，用于"最后一次修改"的时间戳，它总是使用当前日期，默认为False； 参数auto_now_add表示当对象第一次被创建时自动设置当前时间，用于创建的时间戳，它总是使用当前日期，默认为False; 参数auto_now_add和auto_now是相互排斥的，组合将会发生错误 |
    | TimeField        | 时间，参数同DateField                                        |
    | DateTimeField    | 日期时间，参数同DateField                                    |
    | FileField        | 上传文件字段                                                 |
    | ImageField       | 继承于FileField，对上传的内容进行校验，确保是有效的图片      |

5) 选项
    | 选项        | 说明                                                         |
    | ----------- | ------------------------------------------------------------ |
    | null        | 如果为True，表示允许为空，默认值是False                      |
    | blank       | 如果为True，则该字段允许为空白，默认值是False                |
    | db_column   | 字段的名称，如果未指定，则使用属性的名称                     |
    | db_index    | 若值为True, 则在表中会为此字段创建索引，默认值是False        |
    | default     | 默认                                                         |
    | primary_key | 若为True，则该字段会成为模型的主键字段，默认值是False，一般作为AutoField的选项使用 |
    | unique      | 如果为True, 这个字段在表中必须有唯一值，默认值是False        |

    **null是数据库范畴的概念，blank是表单验证范畴的**
6) 外键

在设置外键时，需要通过on_delete选项指明主表删除数据时，对于外键引用表数据如何处理，在django.db.models中包含了可选常量：

- CASCADE 级联 , 删除主表数据时连通一起删除外键表中数据
- PROTECT 保护 , 通过抛出ProtectedError异常，来阻止删除主表中被外键应用的数据
- SET_NULL 设置为NULL , 仅在该字段null=True允许为null时可用
- SET_DEFAULT 设置默认值 , 仅在该字段设置了默认值时可用
- SET() 设置为特定值或者调用特定方法

    ```python
    from django.conf import settings
    from django.contrib.auth import get_user_model
    from django.db import models
    
    def get_sentinel_user():
        return get_user_model().objects.get_or_create(username='deleted')[0]
    
    class MyModel(models.Model):
        user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.SET(get_sentinel_user),
        )
    ```
- DO_NOTHING 不做任何操作，如果数据库前置指明级联性，此选项会抛出IntegrityError异常

### 迁移

本质: 创建表,将模型类同步到数据库中

``` Python
1. 生成迁移文件

    python manage.py makemigrations

2. 同步到数据库中

    python manage.py migrate

```

### 查看MySQL数据库日志

    1. 修改配置文件
    
        sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
    
        general_log_file            =/var/log/mysql/mysql/log
        general_log                 =1
        把68，69行前面的#去除，然后保存并使用如下命令重启mysql服务。
    
    2. 重启mysql服务
    
        sudo service msyql restart
    
    3. 查看MySQL日志
    
        tail -f /var/log/mysql/mysql.log  # 可以实时查看数据库的日志内容
        # 如提示需要sudo权限，执行
        # sudo tail -f /var/log/mysql/mysql.log

### 数据库操作(CRUD)

1. 增加

    1) save

        通过创建模型类对象,执行对象的save()方法保存到数据库中

        ``` Python
            def post(self, request):
            bookinfo_dict = request.POST
        
            title = bookinfo_dict.get('title')
            pub_time = bookinfo_dict.get('pub_time')
        
            book = BookInfo()
            book.title = title
            book.pub_date = datetime.strptime(pub_time, '%Y-%m-%d')
            book.save()
            return redirect('/bk/index')
        
        ```
    2) create

        通过模型类.objects.create()保存

        ``` Python
            book = BookInfo.objects.create(title=title1, pub_date=pub_date1)
        ```
2. 查询

    2.1 基本查询

        get 查询单一结果,如果不存在会抛出模型类.DoesNotExist异常。
        all 查询多个结果
        count 查询结果的数量

    2.2 过滤查询

    实现MySQL中的where功能

    - filter 过滤出多个结果
    - exclude 排除掉符合条件剩下的结果
    - get 过滤单一结果

        过滤条件的表达语法如下:

            属性名称__比较运算符=值
            # 属性名称和比较运算符间使用两个下划线，所以属性名不能包括多个下划线

        1) 相等

            exact: 表示判等

                查询编号1 的图书
                BookInfo.objects.filter(id__exact=1)
                简写为  BookInfo.objects.filter(id=1)

        2) 模糊查询

            contains : 是否包含
                说明: 如果要包含%无需转义,直接写即可

                查询书名包含传的图书
            
                BookInfo.objects.filter(btitle__contains='传')

            startswith、endswith：以指定值开头或结尾

                BookInfo.objects.filter(btitle__endswith='部')

            以上运算符都区分大小写，在这些运算符前加上i表示不区分大小写，如iexact、icontains、istartswith、iendswith.

        3) 空查询
            isnull: 是否为null

                查询书名不为空的图书
                BookInfo.objects.filter(btitle__isnull=False)

        4) 范围查询
            in：是否包含在范围内.

                查询编号为1,3,5的图书
                BookInfo.objects.filter(id__in=[1, 3, 5])

        5) 比较查询

            - gt 大于 (greater then)
            - gte 大于等于 (greater then equal)
            - lt 小于 (less then)
            - lte 小于等于 (less then equal)

            ``` python
                查询编号大于3的图书
                BookInfo.objects.filter(id__gt=3)
            
                不等于的运算符，使用exclude()过滤器。
            
                查询编号不等于3的图书
                BookInfo.objects.exclude(id=3)
            
            ```
        6) 日期查询

            year、month、day、week_day、hour、minute、second：对日期时间类型的属性进行运算。

                查询1980年发表的图书。
                BookInfo.objects.filter(bpub_date__year=1980)
                
                查询1980年1月1日后发表的图书。
                BookInfo.objects.filter(bpub_date__gt=date(1990, 1, 1))

    F 对象

        F对象：在等号的右边写属性
        
        语法: F(属性名)
        
        ``` Python
        
            查询阅读量大于等于评论量的图书。
            from django.db.models import F
        
            BookInfo.objects.filter(bread__gte=F('bcomment'))
        
            查询阅读量大于2倍评论量的图书
            BookInfo.objects.filter(bread__gt=F('bcomment') * 2)
        ```

    Q 对象

        Q对象 : 实现逻辑或、与、非
        
            查询阅读量大于20，并且编号小于3的图书。
            BookInfo.objects.filter(bread__gt=20,id__lt=3)
            或
            BookInfo.objects.filter(bread__gt=20).filter(id__lt=3)
        
        如果需要实现逻辑或or的查询，需要使用Q()对象结合|运算符，Q对象被义在django.db.models中。
        
            Q(属性名__运算符=值)
        
                查询阅读量大于20的图书，改写为Q对象如下。
        
                ``` Python
                from django.db.models import Q
        
                BookInfo.objects.filter(Q(bread__gt=20))
                ```
        
        Q对象可以使用&、|连接，&表示逻辑与，|表示逻辑或。
        
                查询阅读量大于20，或编号小于3的图书，只能使用Q对象实现
                BookInfo.objects.filter(Q(bread__gt=20) | Q(pk__lt=3))
        
        Q对象前可以使用~操作符，表示非not。
        
                查询编号不等于3的图书。
                BookInfo.objects.filter(~Q(pk=3))

    聚合函数

        使用aggregate()过滤器调用聚合函数。
        
        聚合函数包括：Avg 平均，Count 数量，Max 最大，Min 最小，Sum 求和，被定义在django.db.models中。
        
        ``` Python
        查询图书的总阅读量。
            from django.db.models import Sum
        
            BookInfo.objects.aggregate(Sum('bread'))
        
        aggregate返回的是一个字典类型 {'属性名__聚合类小写':值}
        
        使用count时一般不使用aggregate()过滤器。
            查询图书总数。
            BookInfo.objects.count()
        
        count函数的返回值是一个数字。
        ```
    2.3 排序

        使用order_by排序
        
            BookInfo.objects.all().order_by('bread')  # 升序
            BookInfo.objects.all().order_by('-bread')  # 降序

    2.4 关联查询

        由一到多的访问语法：
            一对应的模型类对象.多对应的模型类名小写_set
        
            b = BookInfo.objects.get(pk=1)
            b.hreoinfo_set.all()
        
        由多到一的访问语法:
            多对应的模型类对象.多对应的模型类中的关系类属性名 例
        
            h = HeroInfo.objects.get(id=1)
            h.hbook
        
        访问一对应的模型类关联对象的id语法:
            多对应的模型类对象.关联类属性_id
            h = HeroInfo.objects.get(id=1)
            h.hbook_id

    关联过滤查询

    由多模型类条件查询一模型类数据:

        语法:
            关联模型类名小写__属性名__条件运算符=值
        
        例子:
        
            查询图书，要求图书英雄为"孙悟空"
                BookInfo.objects.filter(heroinfo__hname='孙悟空')
        
            查询图书，要求图书中英雄的描述包含"八"
                BookInfo.objects.filter(heroinfo__hcomment__contains='八')

    由一模型条件查询多类型数据:

        语法:
            一模型类关联属性名__一模型类属性名__条件运算符=值
        
        例子:
            查询书名为“天龙八部”的所有英雄。
                HeroInfo.objects.filter(hbook__btitle='天龙八部')
        
            查询图书阅读量大于30的所有英雄
                HeroInfo.objects.filter(hbook__bread__gt=30)
3. 修改

    1) save

        修改模型类对象的属性,执行save()方法

        ``` Python
            hero = HeroInfo.objects.get(hname='猪八戒')
            hero.hname = '猪悟能'
            hero.save()
        ```
    2) update

        使用模型类.objects.filter().update()，会返回受影响的行数

            HeroInfo.objects.filter(hname='沙悟净').update(hname='沙僧')

4. 删除

    1) 模型类对象delete

        hero = HeroInfo.objects.get(id=13)
        hero.delete()

    2)模型类.objects.filter().delete()

        HeroInfo.objects.filter(id=14).delete()

### 查询集 QuerySet

当调用如下过滤器方法时,会返回查询集

- all() : 返回所有的数据
- filter() : 返回满足条件的数据
- exclude() : 返回满足条件之外的数据
- order_by() : 对结果进行排序

对查询集可以再次用过滤器进行过滤

    BookInfo.objects.filter(bread__gt=30).order_by('bpub_date')

判断某一个查询集中是否有数据：

    - exists()：判断查询集中是否有数据，如果有则返回True，没有则返回False。

#### 2 大特性

    1) 惰性执行
    
        创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化、与if合用
    
        例:
            qs = BookInfo.objects.all()
            当执行该语句时,只是创建一个查询集,并未进行数据库查询.
    
            for book in qs:
                print(book.btitle)
            继续执行遍历迭代操作后,才真正进行数据库查询
    
    2) 缓存
    
            使用同一个查询集，第一次使用时会发生数据库的查询，然后Django会把结果缓存下来，再次使用这个查询集时会使用缓存的数据，减少了数据库的查询次数。
    
            例:
                两个查询集，无法重用缓存，每次查询都会与数据库进行一次交互，增加了数据库的负载。
                    from booktest.models import BookInfo
                    [book.id for book in BookInfo.objects.all()]
                    [book.id for book in BookInfo.objects.all()]
    
                经过存储后，可以重用查询集，第二次使用缓存中的数据。
                    qs=BookInfo.objects.all()
                    [book.id for book in qs]
                    [book.id for book in qs]

#### 限制查询集

可以对查询集进行取下标或切片操作，等同于sql中的limit和offset子句。

    不支持负数索引.

对查询集进行切片后返回一个新的查询集，不会立即执行查询。

如果获取一个对象，直接使用[0]，等同于[0:1].get()，但是如果没有数据，[0]引发IndexError异常，[0:1].get()如果没有数据引发DoesNotExist异常。

获取1,2项
    qs = BookInfo.objects.all()[0:2]

## 管理器对象

### 自定义管理器

一旦为模型类指明自定义的过滤器后，Django不再生成默认管理对象objects。

自定义管理器类主要用于两种情况:

    1. 修改原始查询集，重写all()方法.
    
        a)打开booktest/models.py文件,定义类BookInfoManager
    
            ``` Python
    
            #图书管理器
            class BookInfoManager(models.Manager):
                def all(self):
                    #默认查询未删除的图书信息
                    #调用父类的成员语法为：super().方法名
                    return super().filter(is_delete=False)
            ```
        b)在模型类BookInfo中定义管理器
    
            ``` python
            class BookInfo(models.Model):
            ...
            books = BookInfoManager()
            ```
        c) 使用方法
    
            BookInfo.books.all()
    
    2. 在管理器中补充定义新的方法
    
        ``` Python
        a）打开booktest/models.py文件，定义方法create。
        class BookInfoManager(models.Manager):
            #创建模型类，接收参数为属性赋值
            def create_book(self, title, pub_date):
                #创建模型类对象self.model可以获得模型类
                book = self.model()
                book.btitle = title
                book.bpub_date = pub_date
                book.bread=0
                book.bcommet=0
                book.is_delete = False
                # 将数据插入进数据表
                book.save()
                return book
    
        b）为模型类BookInfo定义管理器books语法如下
    
        class BookInfo(models.Model):
            ...
            books = BookInfoManager()
    
        c）调用语法如下：
    
        book=BookInfo.books.create_book("abc",date(1980,1,1))
        ```

## Admin站点

### 管理界面本地化

LANGUAGE_CODE = 'zh-hans' # 使用中国语言
TIME_ZONE = 'Asia/Shanghai' # 使用中国上海时间

### 创建超级管理员

python manage.py createsuperuser
输入用户密码

进入后台管理界面

    http://127.0.0.1:8000/admin/

### 注册模型类

打开应用/admin.py

    from django.contrib import admin
    from booktest.models import BookInfo,HeroInfo
    
    admin.site.register(BookInfo)
    admin.site.register(HeroInfo)

### 定义与使用Admin管理类(待补充)

``` Python
1. admin.py

class BookInfoAdmin(admin.ModelAdmin):
    # 每页显示的数量
    list_per_page = 2
    # 操作选项底部设置
    actions_on_bottom = True

    # 列表中的列

    list_display = ['id', 'title', 'pub_date', 'book_image']

    # # 编辑页
    # fields = ['title','pub_date']

    # 分组编辑
    # 'classes': ('collapse'),  # 是否折叠显示}
    fieldsets = [
        ('必填项', {'fields': ('title', 'pub_date')}),
        ('选填项', {'fields': ('bread', 'comment', 'book_image'), 'classes': ('collapse',)})
    ]

    # 添加嵌入类
    # inlines = [HeroInfoInline]

    def pub_date(self):
        return self.bpub_date.strftime('%Y年%m月%d日')

    pub_date.admin_order_field = 'pub_date'


2. model.py
# 图书类
class BookInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='名称')
    pub_date = models.DateField(verbose_name='出版时间')
    bread = models.IntegerField(default=0, verbose_name='阅读量')
    comment = models.IntegerField(default=0, verbose_name='评论量')
    is_delete = models.BooleanField(default=0, verbose_name='逻辑删除')
    book_image = models.ImageField(upload_to='book_images', null=True, blank=True, verbose_name='封面')

    class Meta:
        # 知名数据库表名
        db_table = 'tb_books'
        # 在admin 站点中显示的名称
        verbose_name = '图书'
        # 显示的复数名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
# 英雄类
class HeroInfo(models.Model):
    GENDER_CHOICES = (
        (True, '男'),
        (False, '女')
    )
    name = models.CharField(max_length=30, verbose_name='名字')
    gender = models.BooleanField(choices=GENDER_CHOICES, default=False, verbose_name='性别')
    comment = models.CharField(max_length=200, verbose_name='描述信息')
    is_delete = models.BooleanField(default=0, verbose_name='逻辑删除')
    book = models.ForeignKey(BookInfo)

    class Meta:
        db_table = 'tb_heros'
        verbose_name = '英雄'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def book_title(self):
        return self.book.title

    book_title.short_description = '书名'

```

#### 列表页的选项

list_per_page = 10 分页时每页显示的条数.

actions_on_top = True 动作在顶部显示.

actions_on_bottom = False  动作在底部显示.

list_display = ['id', 'title', 'pub_date', 'bpub_date']#表格中显示哪些属性或方法

list_filter = ['book','gender'] 右侧快速过滤

search_fields = ['name','content'] 顶部搜索框

#### 编辑页的选项

fields = [] 指定可编辑的属性
fieldsets=[]：分组，指定本组可编辑的属性
两个选项二选一使用
inlines=[嵌入类]：在编辑对象时，嵌入相关的对象

#### 标题

admin.site.site_header = 页面顶部文本
admin.site.site_title = 浏览器标签提示文本
admin.site.index_title = 首页标题文本

#### 上传图片

1. 设置环境

    安装依赖包 pip install Pliiow

    ``` python
    setting.py
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
        os.path.join(BASE_DIR, 'media')
    ]

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    ```

2. 为模型类添加 ImageField字段

    ``` Python
    class BookInfo(models.Model):
        title = models.CharField(max_length=20, verbose_name='名称')
        pub_date = models.DateField(verbose_name='出版时间')
        bread = models.IntegerField(default=0, verbose_name='阅读量')
        comment = models.IntegerField(default=0, verbose_name='评论量')
        is_delete = models.BooleanField(default=0, verbose_name='逻辑删除')
        book_image = models.ImageField(upload_to='book_images', null=True, blank=True, verbose_name='封面')
    
        class Meta:
            # 知名数据库表名
            db_table = 'tb_books'
            # 在admin 站点中显示的名称
            verbose_name = '图书'
            # 显示的复数名称
            verbose_name_plural = verbose_name
    
        def __str__(self):
    
    ```
3. 上传图片测试.

    最终保存路径为：media_root/upload_to/文件名

    访问路径：/static/属性值==>/static/booktest/2.jpg