# docker 下 Mongo



```shell
# 不启用 认证
docker run --name mongo -p 27017:27017 -d mongo:latest

# 启用认证

 docker run -d -p 27017:27017 --name mongo -e MONGO_INITDB_ROOT_USERNAME=zhengzongwei -e MONGO_INITDB_ROOT_PASSWORD=zhengzongwei mongo
```

