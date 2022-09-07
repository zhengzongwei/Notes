# docker基本操作

```shell
# 创建docker 组
sudo groupadd docker

# 将当前用户加入docker组
sudo gpasswd -a ubuntu docker

# 刷新docker组
newgrp docker
```



## 1. docker images

### 拉取镜像

```shell
dokcer pull image_name
```

### 重命名镜像

```shell
docker tag image_id 仓库:标签

docker tag old_image_name new_image_name
```

### 删除镜像

```shell
# 删除时需要保证镜像没有被容器使用
docker rm image_id
```

### 镜像导入/导出

```shell
# 导出镜像
docker save d72b5e7fce8f > zentao.tar
docker save -o image.tar easysoft/zentao:17.6 mariadb:latest

# 导入镜像
docker load < zentao.tar
```

## 2. docker container

### 运行容器

```shell

```

### 操作容器

```shell

```

### 复制文件

```shell
# docker 复制文件到容器
docker cp 本地路径 容器名：路径

# docker 容器文件复制到本地
docker 容器名：路径 本地路径
```

### 容器导入/导出

```shell
# 导出容器
docker export d72b5e7fce8f > zentao.tar
# 导入容器
docker import - zentao < zentao.tar
```

## 3. logs

