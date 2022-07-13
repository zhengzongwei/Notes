# Flask 模板

## 模板template

reader_template 函数调用了模板引擎Jinja2

## 过滤器

使用方式: 变量名|过滤器

## 常见内建过滤器

### 字符串操作

- safe 禁用转义
- capitalize 变量值的首字母大写,其余字母小写
- lower 把值转换成小写
- upper 把值转换成大写
- title 把值中的每个单词的首字母转成大写
- reverse 反转字符串
- format 格式化输出
- striptags 渲染之前把值中所有的HTML标签都删掉
- truncate 字符串截断

### 列表操作

- first 取第一个元素
- last 取最后一个元素
- length 获取列表长度
- sum 列表求和
- sort 列表排序

### 语句块过滤

``` html
{% filter upper%}
    # 一大段文字#
{% endfilter%}
```

### 自定义过滤器

过滤器本质是函数: 过滤器只能在模板中使用

实现自定义过滤器的方式

- 通过Flask应用对象的add_temolate_filter()
- 通过装饰器来实现自定义过滤器

**注:**自定义的过滤器名称如果和内置的过滤器重名,会覆盖内置的过滤器.该方法的第一个参数是参数名,第二个参数是自定义的过滤器名称

> 需求: 添加列表反转的过滤器

方式一:通过调用应用程序实例的add_template_filter方法实现自定义过滤器

``` python
# 自定义过滤器 一
def do_listreverse(li):
    temp_li = list(li)
    temp_li.reverse()
    return temp_li

app.add_template_filter(do_listreverse, 'lireverse')
```

方式二:用装饰器来实现自定义过滤器.装饰器传入的参数时自定义的过滤器的名称

``` python
# 自定义过滤器 二
@app.template_filter('lireverse')
def do_listreverse(li):
    temp_li = list(li)
    temp_li.reverse()
    return temp_li
```

## 控制代码块

控制代码块主要包含两个

- if/else if /else/ endif

``` python

{% if comments | length > 0 %}
    There are {{ comments | length }} comments
{% else %}
    There are no comments
{% endif %}

```

- for / endfor

``` python
{% for post in posts %}
    <div>
        <h1>{{ post.title }}</h1>
        <p>{{ post.text | safe }}</p>
    </div>
{% endfor %}
```

- 嵌套使用

``` Python
{# 控制语句代码块 #}

{% for item in my_list if item.id != 5 %}
    {% if loop.index == 1 %}
        <li style="background-color: blue">{{ item.value }}</li>
    {% elif loop.index == 2 %}
        <li style="background-color: pink">{{ item.value }}</li>
    {% elif loop.index == 3 %}
        <li style="background-color: green">{{ item.value }}</li>
    {% elif loop.index == 4 %}
        <li style="background-color: gold">{{ item.value }}</li>


    {% endif %}

{#    {{ loop.index0 }} #}
{#    {{ item }} <br>#}
{% endfor %}

```

变量 | 描述
-|-|
loop.index | 当前循环迭代的次数（从 1 开始）
loop.index0 | 当前循环迭代的次数（从 0 开始）
loop.revindex | 到循环结束需要迭代的次数（从 1 开始）
loop.revindex0 | 到循环结束需要迭代的次数（从 0 开始）
loop.first | 如果是第一次迭代，为 True 。
loop.last | 如果是最后一次迭代，为 True 。
loop.length | 序列中的项目数。
loop.cycle | 在一串序列间期取值的辅助函数。见下面示例程序。

## 模板代码复用

### 模板继承

模板的继承本质就是代码的替换.

语法:

父模板 : {% block top %} {% endblock %} --- 定义标签内容
子模板 : {% extends 'base.html' %}      --- extends指令声明这个模板继承自哪

1、父模板：实现多个页面中相同的区域块，一般都是顶部、底部、中间部分内容

2、子模板：如果想要实现自己特有的页面内容，直接重写指定的区域块，自己填充内容;

3、子模板：如果不想要父模板中部分内容，直接声明区域块，内容为空;

4、子模板：如果既想要实现自己的内容，又想要使用父模板的，使用super()

- base.html 父模板

``` html
{% block top %}
    <p>这是base的顶部信息</p>

{% endblock %}

{% block center %}
    <p>这是base的内容信息</p>

{% endblock %}

{% block bottom %}
    <p>这是base的底部信息</p>

{% endblock %}

```

- base_sun.html 子模板

``` html
{% extends 'base.html' %}
```

- app.py

``` python
from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/index')
def index():
    return render_template('base_sun.html')
if __name__ == '__main__':
    app.run(debug=True)

```

### 宏(macro)

使用: 宏的本质是函数,用于实现模板页面动态的代码封装

宏的定义 使用都在模板
定义宏之后一定要**调用**.

#### 导入宏

导入宏

{% import 'macro_.html' as f %}

调用导入宏

{% f.fun() %}

marco_.html

``` html
{#定义宏#}
{% macro fun() %}
<input type="{{ type }}" name="{{ name }}">

{% endmacro %}

{#调用宏 #}
{{ fun() }}
```

macro.py

``` python
from flask import Flask,render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/index')
def index():
    type = 'text'
    name = 'zheng'
    return render_template('macro_.html',type=type,name=name)
if __name__ == '__main__':
    app.run(debug=True)

```

### 包含(include)

包含的使用: 包含的本质是完整的复用;如果包含文件不存在,使用 ignore missing 忽略错误.

## WTForms

表单是由三部分组成  表单标签/表单域/表单按钮

表单: 允许用户输入数据,负责采集数据,通过表单将用户输入的数据提交给服务器.

使用 Flask-WTF 要配置 SECRET_KEY

WTForms 支持的HTML标准字段
字段对象 | 说明
-|-|
StringField | 文本字段
TextAreaField | 多行文本字段
PasswordField | 密码文本字段
HiddenField | 隐藏文件字段
DateField | 文本字段，值为 datetime.date 文本格式
DateTimeField | 文本字段，值为 datetime.datetime 文本格式
IntegerField | 文本字段，值为整数
DecimalField | 文本字段，值为decimal.Decimal
FloatField | 文本字段，值为浮点数
BooleanField | 复选框，值为True 和 False
RadioField | 一组单选框
SelectField | 下拉列表
SelectMutipleField | 下拉列表，可选择多个值
FileField | 文件上传字段
SubmitField | 表单提交按钮
FormField | 把表单作为字段嵌入另一个表单
FieldList | 一组指定类型的字段

WTForms 常用验证函数
验证函数 | 说明
-|-|
DataRequired | 确保字段中有数据
EqualTo | 比较两个字段的值，常用于比较两次密码输入
Length | 验证输入的字符串长度
NumberRange | 验证输入的值在数字范围内
URL | 验证URL
AnyOf | 验证输入值在可选列表中
NoneOf | 验证输入值不在可选列表中

``` python

```