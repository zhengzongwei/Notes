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

## docker mairadb镜像

```dockerfile
# 使用官方 MariaDB 镜像作为基础镜像
FROM mariadb:11.2.2

# 设置环境变量
ENV MARIADB_ROOT_PASSWORD=mysql
ENV MARIADB_DATABASE=bookcloud
ENV MARIADB_USER=bookcloud
ENV MARIADB_PASSWORD=bookcloud

# 将初始化 SQL 脚本拷贝到容器中
#COPY init.sql /docker-entrypoint-initdb.d/

# 暴露 MariaDB 默认端口
EXPOSE 3306

```



可以设置 官方镜像环境变量 [MariaDB Server Docker 官方镜像环境变量 - MariaDB知識庫](https://mariadb.com/kb/en/mariadb-server-docker-official-image-environment-variables/#mariadb_random_root_password-mysql_random_root_password)

### MARIADB_ALLOW_EMPTY_ROOT_PASSWORD / MYSQL_ALLOW_EMPTY_PASSWORD

设置为非空值（如 ），以允许使用 root 用户的空白密码启动容器。注意：除非您真的知道自己在做什么，否则不建议将此变量设置为 yes，因为这将使您的 MariaDB 实例完全不受保护，从而允许任何人获得完全的超级用户访问权限。`1`

### MARIADB_RANDOM_ROOT_PASSWORD / MYSQL_RANDOM_ROOT_PASSWORD

设置为非空值（如 yes）可为 root 用户生成随机初始密码。生成的 root 密码将打印到 stdout（生成的 root 密码：.....）。

### MARIADB_ROOT_HOST / MYSQL_ROOT_HOST

这是创建的 root 用户的主机名部分。默认情况下，这是%，但是可以将其设置为任何默认的MariaDB允许的主机名组件。将其设置为 localhost 将阻止任何 root 用户访问，除非通过 unix 套接字。

### MARIADB_DATABASE / MYSQL_DATABASE

此变量允许您指定要在映像启动时创建的数据库的名称。

### MARIADB_USER / MYSQL_USER， MARIADB_PASSWORD_HASH / MARIADB_PASSWORD / MYSQL_PASSWORD

用户变量和密码变量以及数据库都是创建用户所必需的。此用户将被授予对MARIADB_DATABASE数据库的所有访问权限（对应于 GRANT ALL）。

不要使用此机制创建 root 超级用户，默认情况下，该用户是使用 MARIADB_ROOT_PASSWORD / MYSQL_ROOT_PASSWORD 变量指定的密码创建的。

### MARIADB_MYSQL_LOCALHOST_USER / MARIADB_MYSQL_LOCALHOST_GRANTS

将 MARIADB_MYSQL_LOCALHOST_USER 设置为非空值以创建mysql@locahost数据库用户。此用户对于各种运行状况检查和备份脚本特别有用。

默认情况下，mysql@localhost用户将获得权限。如果需要更多访问权限，可以以逗号分隔列表的形式提供额外的全局权限。如果您共享包含 MariaDB 的 unix 套接字（默认为 /var/run/mysqld）的卷，则超出权限可能会导致机密性、完整性和可用性风险，因此请使用最小集。它也可以用于[Mariadb-backup](https://mariadb.com/kb/en/mariabackup/)。[healthcheck.sh](https://mariadb.com/kb/en/using-healthcheck-sh-script/) 脚本还记录了每个运行状况检查测试所需的权限。`USAGE``USAGE`

### MARIADB_HEALTHCHECK_GRANTS

将 MARIADB_HEALTHCHECK_GRANTS 设置为需要授予 、 、 用户的授权。如果未指定，则默认授权为 。`healtcheck@localhost``healtcheck@127.0.0.1``healtcheck@::1``USAGE`

这里使用的主要值将是`REPLICA MONITOR for the healthcheck --replication test.`

### MARIADB_INITDB_SKIP_TZINFO / MYSQL_INITDB_SKIP_TZINFO

默认情况下，入口点脚本会自动加载 CONVERT_TZ（） 函数所需的时区数据。如果不需要，则任何非空值都将禁用时区加载。

### MARIADB_AUTO_UPGRADE / MARIADB_DISABLE_UPGRADE_BACKUP

将 MARIADB_AUTO_UPGRADE 设置为非空值，让入口点检查 [mariadb-upgrade](https://mariadb.com/kb/en/mariadb-upgrade/) 是否需要运行，如果需要，请在启动 MariaDB 服务器之前运行升级。

在升级之前，将在 datadir 的顶部创建一个名为 system_mysql_backup_*.sql.zst 的系统数据库备份。可以通过将 MARIADB_DISABLE_UPGRADE_BACKUP 设置为非空值来禁用此备份过程。

### MARIADB_MASTER_HOST

指定后，容器将连接到此主机并从中复制。

### MARIADB_REPLICATION_USER / MARIADB_REPLICATION_PASSWORD_HASH / MARIADB_REPLICATION_PASSWORD

指定 MARIADB_MASTER_HOST 时，将使用 MARIADB_REPLICATION_USER 和 MARIADB_REPLICATION_PASSWORD 连接到主设备。

如果未指定，则将使用客户端启动复制所需的 REPLICATION REPLICA 授权创建MARIADB_REPLICATION_USER。



```bash
docker run -d --name mariadb -e MYSQL_ROOT_PASSWORD=mysql -p 16030:3306 -v mariadb/mariadb:/var/lib/mysql mariadb:11.2.2
```

