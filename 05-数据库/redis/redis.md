# Redis 

## 开启密码验证

```bash
ACL SETUSER zhengzongwei on >zhengzongwei allkeys allcommands
```



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



## String CRUD



