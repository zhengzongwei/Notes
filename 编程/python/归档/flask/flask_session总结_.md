# flask 四种session

1. ## 状态保持

session: 与框架语言无关,cookie 和session的概念,本质是 键值对的字符串,session是基于cookie实现的

2. ## Flask 的session

session: 请求上下文对象.封装了用户信息,可以对redis数据库中缓存的用户信息进行读写操作

3. ## 数据库会话对象session

Flask-SQLAlchemy扩展包,封装了数据库的基本操作.

4. ## flask-session 的Session

封装了状态保持中的用户缓存的位置,对session信息进行签名.加上前缀

1 2 4 都是为了实现状态保持
