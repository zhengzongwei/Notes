# brctl

> brctl 命令用于设置、维护和检查Linux内核中的以太网网桥配置

以太网网桥是一种设备，通常用于将以太网的不同网络连接在一起，以便这些以太网对参与者显示为一个以太网。所连接的每个以太网对应于网桥中的一个物理接口。这些单独的以太网被聚集成一个更大的（“逻辑”）以太网，这个更大的以太网对应于网桥网络接口。

语法格式：brctl [参数] <bridge>

## 常用参数

| addbr         | 创建网桥               |
| ------------- | ---------------------- |
| delbr         | 删除网桥               |
| addif         | 将网卡接口接入网桥     |
| delif         | 删除网桥接入的网卡接口 |
| show          | 查询网桥信息           |
| stp {on\|off} | 启用禁用 STP           |
| showstp       | 查看网桥 STP 信息      |
| setfd         | 设置网桥延迟           |
| showmacs      | 查看 mac 信息          |

## 命令示例

| `addbr <bridge>`          | 创建网桥               | **brctl** addbr br10      |
| ------------------------- | ---------------------- | ------------------------- |
| `delbr <bridge>`          | 删除网桥               | **brctl** delbr br10      |
| `addif <bridge> <device>` | 将网卡接口接入网桥     | **brctl** addif br10 eth0 |
| `delif <bridge> <device>` | 删除网桥接入的网卡接口 | **brctl** delif br10 eth0 |
| `show <bridge>`           | 查询网桥信息           | **brctl** show br10       |
| `stp <bridge> {on|off}`   | 启用禁用 STP           | **brctl** stp br10 off/on |
| `showstp <bridge>`        | 查看网桥 STP 信息      | **brctl** showstp br10    |
| `setfd <bridge> <time>`   | 设置网桥延迟           | **brctl** setfd br10 10   |
| `showmacs <bridge>`       | 查看 mac 信息          | **brctl** showmacs br10   |



