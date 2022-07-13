# Flask_数据库

## ORM Object-Relation Mapping 对象关系映射

本质: 实现模型对象到关系数据库数据的映射

**优点**:

1. 只需要面对对象编程,不需要面向数据库编写代码

    - 对数据库的操作转化为对类属性和方法的操作
    - 不用编写各种数据库的SQL语句

2. 实现了数据模型与数据库的解耦,屏蔽了不同数据库操作上的差异
    - 不在关注用的是mysql,还是Oracle...
    - 通过简单的配置就可以轻松更换数据库.

**缺点**:

1. 相比较直接使用SQL语句操作数据库,性能上有损失
2. 根据对象操作转换成SQL语句,根据查询的结果转化为对象,在映射过程中性能有损失.

## Flaks-SQLAlchemy 安装配置

- SQLALchemy 实际上是对数据库的抽象，让开发者不用直接和 SQL 语句打交道，而是通过 Python 对象来操作数据库，在舍弃一些性能开销的同时，换来的是开发效率的较大提升

- SQLAlchemy是一个关系型数据库框架，它提供了高层的 ORM 和底层的原生数据库的操作。flask-sqlalchemy 是一个简化了 SQLAlchemy 操作的flask扩展。

### 安装

    pip install flask-sqlalchemy

如果连接是mysql,需要安装mysqldb  pip install flask-mysqldb

### 数据库连接其他配置

名字| 备注|
-|-|
SQLALCHEMY_DATABASE_URI|用于连接的数据库 URI 。例如:sqlite:////tmp/test.dbmysql://username:password@server/db
SQLALCHEMY_BINDS | 一个映射 binds 到连接 URI 的字典。更多 binds 的信息见用 Binds 操作多个数据库。
SQLALCHEMY_ECHO | 如果设置为Ture， SQLAlchemy 会记录所有 发给 stderr 的语句，这对调试有用。(打印sql语句)
SQLALCHEMY_RECORD_QUERIES | 可以用于显式地禁用或启用查询记录。查询记录 在调试或测试模式自动启用。更多信息见get_debug_queries()。
SQLALCHEMY_NATIVE_UNICODE | 可以用于显式禁用原生 unicode 支持。当使用 不合适的指定无编码的数据库默认值时，这对于 一些数据库适配器是必须的（比如 Ubuntu 上 某些版本的 PostgreSQL ）。
SQLALCHEMY_POOL_SIZE | 数据库连接池的大小。默认是引擎默认值（通常 是 5 ）
SQLALCHEMY_POOL_TIMEOUT | 设定连接池的连接超时时间。默认是 10 。
SQLALCHEMY_POOL_RECYCLE | 多少秒后自动回收连接。这对 MySQL 是必要的， 它默认移除闲置多于 8 小时的连接。注意如果 使用了 MySQL ， Flask-SQLALchemy | 自动设定 这个值为 2 小时。

### 连接其他数据库

- Postgres:

    postgresql://scott:tiger@localhost/mydatabase

- Mysql:

    mysql://scott:tiger@localhost/mydatabase

- Oracle:

    oracle://scott:tiger@127.0.0.1:1521/sidname

- SQLite:

    sqlite:////absolute/path/to/foo.db

### 常用 SQLAlchemy 字段类型

类型名| Python中类型|说明
-|-|-|
Integer | int | 普通整数，一般是32位
SmallInteger | int | 取值范围小的整数，一般是16位
BigInteger | int或long | 不限制精度的整数
Float | float | 浮点数
Numeric | decimal.Decimal | 普通整数，一般是32位
String | str | 变长字符串
Text | str | 变长字符串，对较长或不限长度的字符串做了优化
Unicode | unicode | 变长Unicode字符串
UnicodeText | unicode | 变长Unicode字符串，对较长或不限长度的字符串做了优化
Boolean | bool | 布尔值
Date | datetime.date | 时间
Time | datetime.datetime | 日期和时间
LargeBinary | str | 二进制文件

### SQLAlchemy 列选项

选项名 | 说明
-|-|
primary_key | 如果为True，代表表的主键
unique | 如果为True，代表这列不允许出现重复的值
index | 如果为True，为这列创建索引，提高查询效率
nullable | 如果为True，允许有空值，如果为False，不允许有空值
default | 为这列定义默认值

### SQLAlchemy 关系选项

选项名 | 说明
-|-|
backref | 在关系的另一模型中添加反向引用
primary join | 明确指定两个模型之间使用的联结条件
uselist | 如果为False，不使用列表，而使用标量值
order_by | 指定关系中记录的排序方式
secondary | 指定多对多关系中关系表的名字
secondary join | 在SQLAlchemy中无法自行决定时，指定多对多关系中的二级联结条件

## 数据库的基本操作

- Flask-SQLAlchemy中,插入/修改/删除等操作,均有数据库会话管理.

    会话用 db.session 表示. 在准备把数据写入数据库前,要先把数据添加到会话中,然后调用commit()方法提交会话

- Flask-SQLAlchemy中,查询操作通过query 对象操作.

    最基本的查询是返回表中的所有数据,可以通过过滤器进行更精确的数据库查询.

### 视图函数中定义的模型类

``` Python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#设置连接数据库的URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    us = db.relationship('User', backref='role')

    #repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Role:%s'% self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User:%s'%self.name
if __name__ == '__main__':
    app.run(debug=True)
```

### 模型之前的关联

#### 一对多

``` python
class Role(db.Model):
    # 定义表名,如果未定义,默认创建同类名的表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    us = db.relationship('User', backref='role',lazy='dynamic')
    # 定义关系时,第一个是多方模型的类名,第二个定义的关系
    # us给一方使用,实现一对多的查询,backref 给多方使用,实现多对一的查询
    #repr()方法显示一个可读字符串
    def __repr__(self):
        return 'Role:%s'% self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 定义外键,指向一方的主键
```

> 一方定义关系,多方定义外键

\__tablename__ 定义表名,如果未定义,默认创建同类名的表名

- realtionship 描述了Role和User的关系,第一个参数为对应参照的类名(一方的类名)
- 第二个参数backref 为类USer申明新属性的方法
- 第三个参数 lazy 决定了什么时候SQLAlchemy 从数据库中加载数据

    - 如果设置为子查询方式(subquery)，则会在加载完Role对象后，就立即加载与其关联的对象，这样会让总查询数量减少，但如果返回的条目数量很多，就会比较慢

        - 设置为 subquery 的话，role.users 返回所有数据列表

    - 另外,也可以设置为动态方式(dynamic)，这样关联对象会在被使用的时候再进行加载，并且在返回前进行过滤，如果返回的对象数很多，或者未来会变得很多，那最好采用这种方式

        - 设置为 dynamic 的话，role.users 返回查询对象，并没有做真正的查询，可以利用查询对象做其他逻辑，比如：先排序再返回结果

### 多对多

``` Python
tb_student_course = db.Table('tb_student_course',
                             db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                             db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
                             )

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    courses = db.relationship('Course', secondary=tb_student_course,
                              backref=db.backref('students', lazy='dynamic'),
                              lazy='dynamic')

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
```

> 两个多对一 ,设定secondary

### 自关联多对多

``` python
tb_user_follows = db.Table(
    "tb_user_follows",
    db.Column('follower_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True),  # 粉丝id
    db.Column('followed_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True)  # 被关注人的id
)

class User(db.Model):
    """用户表"""
    __tablename__ = "info_user"

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(32), unique=True, nullable=False)

    # 用户所有的粉丝，添加了反向引用followed，代表用户都关注了哪些人
    followers = db.relationship('User',
                                secondary=tb_user_follows,
                                primaryjoin=id == tb_user_follows.c.followed_id,
                                secondaryjoin=id == tb_user_follows.c.follower_id,
                                backref=db.backref('followed', lazy='dynamic'),
                                lazy='dynamic')
```

#### 常用的SQLAlchemy 查询过滤器

过滤器 | 说明
-|-|
filter() | 把过滤器添加到原查询上，返回一个新查询
filter_by() | 把等值过滤器添加到原查询上，返回一个新查询
limit | 使用指定的值限定原查询返回的结果
offset() | 偏移原查询返回的结果，返回一个新查询
order_by() | 根据指定条件对原查询结果进行排序，返回一个新查询
group_by() | 根据指定条件对原查询结果进行分组，返回一个新查询

``` Python
# filter_by 精确查询
User.query.filter_by(name='wang').all()

# filter 模糊查询
User.query.filter(User.name.endswith('g')).all()

# get 参数为主键,如果主键不存在没有返回内容
User.query.get()

# 逻辑非，返回名字不等于wang的所有数据
User.query.filter(User.name!='wang').all()

# 非 not_
from sqlalchemy import not_
User.query.filter(not_(User.name=='chen')).all()

# 与 and_
from sqlalchemy import and_
User.query.filter(and_(User.name!='wang',User.email.endswith('163.com'))).all()

# 或 or_
from sqlalchemy import or_
User.query.filter(or_(User.name!='wang',User.email.endswith('163.com'))).all()

```

#### 常用的SQLAlchemy 查询执行器

方法 | 说明
-|-|
all() | 以列表形式返回查询的所有结果
first() | 返回查询的第一个结果，如果未查到，返回None
first_or_404() | 返回查询的第一个结果，如果未查到，返回404
get() | 返回指定主键对应的行，如不存在，返回None
get_or_404() | 返回指定主键对应的行，如不存在，返回404
count() | 返回查询结果的数量
paginate() | 返回一个Paginate对象，它包含指定范围内的结果

> paginate 方法详解

``` python
# page 为当前页
# per_page 每页显示的记录数量
# Flase 没有记录时不报错
paginate = paginate(page,per_page,False)
#   paginate.items分页后的总数据
#   paginate.pagesf分页后的总页数
#   paginate.page当前页数
```

#### paginate 参数详解

属性 | 说明
-|-|
items | 当前页面中的记录
query | 分页的源查询
page  | 当前页数
pages | 查询得到的总页数
per_page | 每页显示的记录数量
total | 查询返回的记录的总数
prev_num | 上一页的页数
next_num | 下一页的页数
has_next | 如果有下一页返回True
has_prev | 如果有上一页,返回True

#### 创建表 db.create_all()

#### 删除表 db.drop_all()

## 数据库迁移

- 在开发过程中，需要修改数据库模型，而且还要在修改之后更新数据库。最直接的方式就是删除旧表，但这样会丢失数据。
- 更好的解决办法是使用数据库迁移框架，它可以追踪数据库模式的变化，然后把变动应用到数据库中。
- 在Flask中可以使用Flask-Migrate扩展，来实现数据迁移。并且集成到Flask-Script中，所有操作通过命令就能完成。
- 为了导出数据库迁移命令，Flask-Migrate提供了一个MigrateCommand类，可以附加到flask-script的manager对象上。

### 准备

安装 Flask_Migrate
    pip install flask_migrate

### 迁移命令

1. 初始化
    python database.py db init
2. 创建迁移脚本
    python database.py db migrate -m '描述信息'
3. 更新数据
    python database.py db upgrade
4. 返回以前的版本
    - 输出格式：<base> ->  版本号 (head), initial migration
        python database.py db history
    - 回滚到指定版本
        python database.py db downgrade 版本号

### 实际操作顺序

1.python 文件 db init

2.python 文件 db migrate -m"版本名(注释)"

3.python 文件 db upgrade 然后观察表结构

4.根据需求修改模型

5.python 文件 db migrate -m"新版本名(注释)"

6.python 文件 db upgrade 然后观察表结构

7.若返回版本,则利用 python 文件 db history查看版本号

8.python 文件 db downgrade(upgrade) 版本号

### 出错的解决方法

删除项目中的迁移文件夹,重新再来一遍.
