# MySQL

## 常用命令

```sql

-- 创建用户
create user 'bookcloud'@'%' identified by 'bookcloud';

-- 查询用户
select user,host from mysql.user;

-- 删除用户
drop user admin@'%';

-- 更改密码
set password for test =password('1122');

---------------------第二种方式----------------------
update  mysql.user set  password=password('1234')  where user='test'
-- 刷新
flush privileges;

-- 用户分配权限
grant all privileges on book_cloud.* to 'bookcloud'@'%';

-- 刷新权限
flush privileges; 
```

