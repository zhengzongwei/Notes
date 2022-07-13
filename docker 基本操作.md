# docker基本操作

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

```

## 3. 备份

```shell
```

## 4. docker compose配置
```shell
```

