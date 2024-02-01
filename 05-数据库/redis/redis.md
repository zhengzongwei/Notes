# Redis 

## 基本配置

### 开启远程访问

- 开启端口访问

  ```bash
  sudo firewall-cmd --zone=public --add-port=6379/tcp --permanent
  
  sudo firewall-cmd --reload
  
  # 验证端口是否打开
  sudo firewall-cmd --zone=public --list-ports
  ```

- 修改配置文件

  ```bash
  # vi /etc/redis/redis.conf
  
  # 注释掉 bind 127.0.0.1 -::1
  
  # 设置 requirepass
  requirepass redis-client
  ```

- 创建用户

  ```bash
  [root@VM-16-5-centos ~]# redis-cli
  127.0.0.1:6379> acl users
  (error) NOAUTH Authentication required.
  127.0.0.1:6379>
  [root@VM-16-5-centos ~]# redis-cli
  127.0.0.1:6379> AUTH zhengzongwei
  OK
  127.0.0.1:6379> acl users
  1) "default"
  127.0.0.1:6379> ACL SETUSER zhengzongwei on >zhengzongwei allkeys allcommands
  OK
  127.0.0.1:6379> acl list
  1) "user default on #c93f42386649a528f6030f78ea8182f34c9ccf8c851649b17725acdea484d911 ~* &* +@all"
  2) "user zhengzongwei on #c93f42386649a528f6030f78ea8182f34c9ccf8c851649b17725acdea484d911 ~* &* +@all"
  ```
### 开启密码验证

```bash
ACL SETUSER zhengzongwei on >zhengzongwei allkeys allcommands

```



## ACL基本操作

- 查看用户

  ```bash
  [root@VM-16-5-centos ~]# redis-cli
  127.0.0.1:6379> acl users
  (error) NOAUTH Authentication required.
  127.0.0.1:6379> AUTH zhengzongwei
  OK
  127.0.0.1:6379> acl list
  1) "user default on #c93f42386649a528f6030f78ea8182f34c9ccf8c851649b17725acdea484d911 ~* &* +@all"
  2) "user zhengzongwei on #c93f42386649a528f6030f78ea8182f34c9ccf8c851649b17725acdea484d911 ~* &* +@all"
  
  127.0.0.1:6379> acl users
  1) "default"
  2) "zhengzongwei"
  ```

- 查看当前用户

  ```bash
  127.0.0.1:6379> ACL WHOAMI
  "default"
  ```

- 获取指定用户的详细权限信息

  ```bash
  127.0.0.1:6379> ACL GETUSER default
   1) "flags"
   2) 1) "on"
      2) "allkeys"
      3) "allchannels"
      4) "allcommands"
   3) "passwords"
   4) 1) "c93f42386649a528f6030f78ea8182f34c9ccf8c851649b17725acdea484d911"
   5) "commands"
   6) "+@all"
   7) "keys"
   8) 1) "*"
   9) "channels"
  10) 1) "*"
  127.0.0.1:6379>
  ```

- 创建用户

  ```bash
  127.0.0.1:6379> ACL SETUSER redis-user
  OK
  127.0.0.1:6379> acl list
  1) "user default on #c93f42386649a528f6030f78ea8182f34c9ccf8c851649b17725acdea484d911 ~* &* +@all"
  2) "user redis-user off &* -@all"
  3) "user zhengzongwei on #c93f42386649a528f6030f78ea8182f34c9ccf8c851649b17725acdea484d911 ~* &* +@all"
  127.0.0.1:6379>
  ```

- 启用/禁用用户

  ```bash
  127.0.0.1:6379> ACL SETUSER redis-user on
  OK
  127.0.0.1:6379> acl list
  1) "user default on #c93f42386649a528f6030f78ea8182f34c9ccf8c851649b17725acdea484d911 ~* &* +@all"
  2) "user redis-user on &* -@all"
  3) "user zhengzongwei on #c93f42386649a528f6030f78ea8182f34c9ccf8c851649b17725acdea484d911 ~* &* +@all"
  127.0.0.1:6379>
  ```

- 设置密码/取消密码

  ```bash
  # 设置密码
  127.0.0.1:6379> ACL SETUSER redis-user >123456
  OK
  # 取消密码
  127.0.0.1:6379> ACL SETUSER redis-user <123456
  OK
  ```

- 删除用户

  ```bash
  127.0.0.1:6379> ACL DELUSER redis-user
  (integer) 1
  127.0.0.1:6379> acl list
  1) "user default on #c93f42386649a528f6030f78ea8182f34c9ccf8c851649b17725acdea484d911 ~* &* +@all"
  2) "user zhengzongwei on #c93f42386649a528f6030f78ea8182f34c9ccf8c851649b17725acdea484d911 ~* &* +@all"
  127.0.0.1:6379>
  ```

## 用户的权限操作




## Redis Config File

### CONFIG GET 命令的基本语法

```bash
127.0.0.1:6379> CONFIG GET CONFIG_SETTING_NAME
```

### 查看日志等级

```bash
127.0.0.1:6379> CONFIG GET loglevel
1) "loglevel"
2) "notice"
127.0.0.1:6379>
```

### 获取所有配置

```bash
127.0.0.1:6379> CONFIG GET *
```

## 参考链接

1. [redis用户权限管理]([一文搞懂redis的用户权限管理（ACL）功能_redis acl-CSDN博客](https://blog.csdn.net/cj_eryue/article/details/131401400))

