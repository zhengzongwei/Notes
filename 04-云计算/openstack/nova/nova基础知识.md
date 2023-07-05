## 数据库更新

`nova-manage db version`		打印当前主数据库版本

  

`nova-manage db sync [--version <version>] [--local_cell]`			将主数据库架构升级到最新版本或指定 





## 创建虚拟机

```shell
nova_snap.py create_vm -f 8d50e67c-99c7-4e88-a032-0635d35258e5 -n snap_test --image ca292943-d9fc-45b7-8cfb-75f016262d95 -c c1 --IP 10.21.0.234 --host kec-local-1

python nova_snap.py create_vm -f 8d50e67c-99c7-4e88-a032-0635d35258e5 -n snap_test --image ca292943-d9fc-45b7-8cfb-75f016262d95 -c c1 --IP 10.21.0.234
```





内存快照接口开发

1. API接口输出
2. nova数据库中添加表 [已验证]
3. db增删改查接口添加
4. nova libvirt dirver 添加相关接口
5. nova action 接口添加

