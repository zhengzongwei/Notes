#  virtual studio code不能使用remote ssh连接openeuler



## 修改openeuler配置

```shell
# 打开注释
AllowAgentForwarding yes
AllowTcpForwarding yes
```

