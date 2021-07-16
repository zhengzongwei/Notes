# mysql/mariadb 在docker中的配置

## 下载镜像
``` 
    docker pull mariadb
```

## 配置镜像
```
docker run --name mariadb-develop -p3306:3306 -v C:\mariadb\data:/var/lib/mysql -v C:\mariadb\conf:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=develop -d mariadb:latest
```


