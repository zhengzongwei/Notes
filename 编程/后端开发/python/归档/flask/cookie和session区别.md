# 浅谈cookie和session的区别

目的: 跟踪会话(状态保持)

cookie是储存在客户端(浏览器)的键值对的字符串
而session 是依托cookie存在的 session_id存在浏览器中,它的值存在服务器中,

细节：session存的数字不会转成字符串，而cookie存值会转为字符串

安全性:

cookie 是明文存在浏览器中,不安全

session是加密存储的,较安全.
