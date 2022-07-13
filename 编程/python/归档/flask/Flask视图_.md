# Flask视图

## Flask框架的基本认识

flask 是由python语言实现的

特点:轻量,简洁,扩展性强

核心:werkzeug 和 Jinja2

## 环境的配置和安装

> 为什么要配置虚拟环境?

各个项目有独立的运行空间,彼此互不影响,python解释器彼此互不影响.

### 配置安装

1. 创建虚拟环境 mkvirtualenv -p python3
2. 移除虚拟环境 rmvirtualenv
3. 进入虚拟环境 workon
4. 退出虚拟环境 deactivate

### 依赖包

1. 批量导出 pip freeze > requirements.txt
2. 批量安装 pip install -r requirements.txt

## 基本程序的实现

\_\_name\_\_ 确定程序所在的位置 可以传入\_\_main__,不能传入数值,可以传入字符串

### 视图函数

route方法必须传入一个字符串形式的url路径,路径必须以斜线开始
>url可以重复吗？视图函数可以重复吗？

url可以重复,url可以指定不同的请求方式

url 查找视图 从上往下执行,如果找到,不会继续匹配

**视图函数**不能重复,函数只允许有一个返回值

### 装饰器路由的实现

创建一个url 默认会有两个映射

1. Rule 存储url映射的视图函数名,存储的路由映射(存储url路径和视图函数的映射关系)
2. Map  存储所有rule对象,一个独立的flask项目只有一个map对象
3. MapAdapter 匹配url和视图函数

## **装饰器路由的具体实现**

1. Rule类 ------用来构造不同的URL模式的对象，路由URL规则
2. Map类---------存储所有的URL规则和一些配置参数
3. MapAdapter类----负责协调Rule做具体的匹配的工作
4. BaseConverter的子类-----负责定义匹配规则

### 调试模式(DEBUG)

特点: 动态加载代码,不用重启服务器,会调试错误信息;生产模式不能开启

### 加载配置文件

1. 加载配置对象 app.config.from_object(配置对象)
2. 加载配置文件 app.config.from_pyfile(配置文件)
3. 加载环境变量 app.config.from_envvar(环境变量)

## 重定向(redirect)

本质: 把当前请求返回的响应,向其他url再次发送请求,跳转页面.

作用: 当项目文件或目录发生改变时,可以使用重定向.

缺点: redirect函数接收的参数为固定url,不建议直接使用,扩展性不强,需要配合url_for 实现重定向,接收的参数为函数名,

``` Python
# 重定向

from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def index():
    a = 'https://www.baidu.com'
    return redirect(a)

if __name__ == '__main__':
    app.run()

# redirect + url_for
from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/')
def center():
    return 'hello Flask!'


@app.route('/get')
def geturl():
    return redirect(url_for('index'))


@app.route('/c')
def index():
    a = 'https://www.baidu.com'
    return redirect(a)


if __name__ == '__main__':
    app.run(port='8080')

```

## 状态码

return 后面可以自定义不符合http协议的状态码,实现前后端数据交互,也可以返回符合http协议的状态码,相当于修改了框架封装好的默认响应报文中的状态码

## 异常处理(abort)

abort 函数接收的参数为符合http协议的状态码,作用为配合errorhandler修饰的函数必须传入参数,参数为错误异常,实现自定义错误页面

``` Python
# 异常处理
from flask import Flask, abort
import flask_00.Configuration

app = Flask(__name__)
app.config.from_object(flask_00.Configuration.Config)

@app.route('/center')
def center():
    abort(403)
@app.errorhandler(403)
def errorhandler(e):
    return '服务器已经理解请求，但是拒绝执行它。'
@app.route('/')
def index():
    return 'hello python',999


if __name__ == '__main__':
    print(app.url_map)
    app.run(port='8080')

```

## JSON

![JSON](Flask%E8%A7%86%E5%9B%BE_.images/JSON-4759866.png)

JavaScript Object Notation
基于键值对的字符串,用来实现数据的传输

前端 ---> json <----python

JSON.parse(info): 把json转成对象
JSON.stringify(): 把对象转成json

json.dumps(info): 把字典转成json
json.loads(info): 把json转成字典

### 建议

建议使用Flask封装的jsonfy方法,不仅返回json数据,可以指定响应的数据类型

## 传参

### 固定参数

&lt;args&gt; 固定参数,必须传给视图函数,转换器限制参数的数据类型

``` Python
# 给路由传参数
# 语法格式 <args>
#网址后面输入参数
from flask import Flask

app = Flask(__name__)

@app.route('/<args>')
def index(args):
    return 'hello %s' %args

if __name__ == '__main__':
    app.run()

```

### 转换器

> 为什么使用转换器?
限制数据类型,使用内置的转换器

内置转换器6种
类型 | 名称
-|-|
'default'|         UnicodeConverter
'string' |        UnicodeConverter
'any'    |         AnyConverter
'path'   |        PathConverter
'int'    |         IntegerConverter
'float'  |        FloatConverter
'uuid'   |         UUIDConverter
简单转换器

``` python
# 转换器

from flask import Flask
from flask_00.Configuration import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/<int:args>')
def index(args):
    return 'hello %s' % args


if __name__ == '__main__':
    app.run()

```

>为什么自定义转换器? 怎么自定义转换器?

已有的转换器无法满足需要,无法定义长度.

``` python
# 自定义转换器
# # 正则固定不变,拓展性不好
# class RegexConverter(BaseConverter):
#     regex = '[\w]{3}'
class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        super().__init__(map)
        self.regex = args[0]

# 添加转换器
app.url_map.converters['regex'] = RegexConverter


# @app.route('/<regex:args>')
@app.route('/<regex("[\w]{3}"):args>')
def index(args):
    return 'hello %s' % args


if __name__ == '__main__':
    app.run()

```

### 查询字符串

url?后面的,以=进行传参,以&进行分隔,叫做查询字符串

获取值 request.args.get(key)
获取表单数据 request.form.get(表单中字段的key)
获取表单的文件 request.files.get(表单中的文件key)
cookies: request.cookies.get(cookie的key)

#### request

属性| 说明|   类型
-|-|-|
data| 记录请求的数据，并转换为字符串 |*
form| 记录请求中的表单数据 |MultiDict
args| 记录请求中的查询参数 |MultiDict
cookies| 记录请求中的cookie信息 |Dict
headers| 记录请求中的报文头 |EnvironHeaders
method| 记录请求使用的HTTP方法 |GET/POST
url| 记录请求的URL地址 |string
files| 记录请求上传的文件 |*

## **请求钩子**

>两种请求前执行

1. before_first_request 在处理第一个请求前执行(只执行一次)
2. before_request 每次请求前都执行

>两种请求后执行

1. after_request 没有错误,每次请求后执行,接受一个参数,视图函数做出的相应.
2. teardown_request 每一次请求之后都会调用,接受一个参数(参数时服务器出现的错误信息)

``` python
# 请求钩子
from flask import Flask, abort
import flask_00.Configuration

app = Flask(__name__)
app.config.from_object(flask_00.Configuration.Config)


# 在第一次请求前开始调用,可以在内部做一些初始化设置
@app.before_first_request
def before_first_request():
    print('before_first_request')


# 每次请求前执行,有一个参数
@app.before_request
def before_request():
    print('before_request')


# 在执行完视图函数之后会调用，并且会把视图函数所生成的响应传入,可以在此方法中对响应做最后一步统一的处理
@app.after_request
def after_request(response):
    print('after_request')
    # print(response)  <Response 6 bytes [200 OK]>
    return response


@app.teardown_request
def teardown_request(e):
    print('teardown_request')


@app.route('/')
def index():
    return 'hello'


@app.errorhandler(403)
def errorhandler(e):
    return '服务器已经理解请求，但是拒绝执行它'


@app.route('/abort')
def abort_page():
    abort(403)


@app.route('/center')
def center():
    return 'center'


if __name__ == '__main__':
    app.run()
```

## 上下文

请求上下文: 封装了客户端和服务器交互过程中的信息

1. request 表示请求的参数信息 user = request.args.get('user') --> 获取的是get请求的参数
2. session 表示用户信息 记录用户信息 session['name']=user.id 获取用户信息 session.get('name')

应用上下文: 封装了程序运行过程中的一些配置信息,比如调用的函数,模块,加载的工具类,文件等

1. current_app 生命周期最长,用来记录项目日志
2. g对象 可以在请求过程中临时存储数据

## **状态保持**

>为什么要进行状态保持?

http协议是一种无状态协议,浏览器请求服务器是无状态的.

http协议底层是TCP/IP协议,三次握手,四次挥手,返回数据后会断开连接,下次链接相当于新的请求,不会记得刚刚的请求信息.

**cookie** :在服务器中生成,储存在浏览器中,不安全.

**session**:session_id储存在浏览器中,它的值存在服务器中,相对安全.

### cookie

``` python
from flask import Flask,make_response,request
from setting import Config
app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def hello_world():
    # 使用响应对象,设置cookie
    response = make_response('set cookie')
    # 设置cookie,并制定有效期
    response.set_cookie('name','python2',max_age=60)
    return response

# 获取cookie
@app.route('/get')
def get_cookie():
    name = request.cookies.get('name')
    return name

@app.route('/hello')
def index():
    return 'hello world'

# 状态保持---session：session基于cookie实现
# session数据存储在内存型数据库，redis、

# 设置session
@app.route('/set')
def set_session():
    session['name']='python02'
    return 'set session success!'

# 获取session
@app.route('/get_session')
def get_session():
    name = session.get('name')
    return name

if __name__ =='__main__':
    app.run()
```

## Flask_script 扩展包

``` Python
from flask import Flask
# 导入Flask_script扩展包
from flask_script import Manager

# 导入配置文件
from setting import Config
app = Flask(__name__)
app.config.form_object(Config)

# 实例化管理器对象
manager = Manager(app)

@app.route('/')
def hello_world():
    return 'hello world!'

if __name__ == '__main__':
    # 代替app.run()
    # 在终端使用命令动态指定host和port,在生产环境下不用手动修改代码的host和port
    # 在pycharm运行需要添加runserver参数
    manager.run()
```
