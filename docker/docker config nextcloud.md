# docker 下 配置  nextcloud server 


## 下载镜像
```
docker pull nextcloud
```

## 配置镜像

```
docker run --name nextcloud -v C:\nextcloudserver:/var/www/html -p 8080:80 -d nextcloud:latest
```