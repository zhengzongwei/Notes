服务器有两个网口，一个连内网（enp0s25)，一个连外网(enp9s0)
使用route 查看

```shell
$ route
目标            网关            子网掩码        标志  跃点   引用  使用 接口
default         gateway         0.0.0.0         UG    100    0        0 enp0s25
default         gateway         0.0.0.0         UG    101    0        0 enp9s0
162.105.89.0    0.0.0.0         255.255.255.0   U     100    0        0 enp0s25
162.105.129.122 gateway         255.255.255.255 UGH   100    0        0 enp0s25
link-local      0.0.0.0         255.255.0.0     U     1000   0        0 enp0s25
192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 enp9s0
```

发现默认网口enp0s25在前面，然后我执行如下命令

```shell
route add default gw 192.168.1.1
```

192.168.1.1对应的是enp9s0连的网关IP，然后就可以连github了，再次察看route

```shell
$ route
内核 IP 路由表
目标            网关            子网掩码        标志  跃点   引用  使用 接口
default         gateway         0.0.0.0         UG    0      0        0 enp9s0
default         gateway         0.0.0.0         UG    100    0        0 enp0s25
default         gateway         0.0.0.0         UG    101    0        0 enp9s0
162.105.89.0    0.0.0.0         255.255.255.0   U     100    0        0 enp0s25
162.105.129.122 gateway         255.255.255.255 UGH   100    0        0 enp0s25
link-local      0.0.0.0         255.255.0.0     U     1000   0        0 enp0s25
192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 enp9s0
```

设置永久路由的方法

（1） 在/etc/rc.local里添加

# 配置的路由信息

route add -net 192.168.3.0/24 dev eth0
route add -net 192.168.2.0/24 gw 192.168.3.254
1
2
3
（2）在/etc/sysconfig/network里添加到末尾

GATEWAY=gw-ip` 或者 `GATEWAY=gw-dev
1
（3）/etc/sysconfig/static-router :

# 设置静态路由

any net x.x.x.x/24 gw y.y.y.y

## 操作

```shell
# 删除默认网关
route del default gw 

# 添加默认网关
route add default gw 192.168.20.1
```
