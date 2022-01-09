# mysql/mariadb 在docker中的配置

## 下载镜像
``` 
    docker pull mariadb
```

## 配置镜像
```shell
# 使用默认存储文件
 docker run --detach --name mariadb-server --env MARIADB_USER=zhengzongwei --env MARIADB_PASSWORD=zhengzongwei --env MARIADB_ROOT_PASSWORD=zhengzongwei -p 3306:3306 mariadb:latest


docker run --name mariadb-develop -p3306:3306 -v C:\mariadb\data:/var/lib/mysql -v C:\mariadb\conf:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=develop -d mariadb:latest


```

