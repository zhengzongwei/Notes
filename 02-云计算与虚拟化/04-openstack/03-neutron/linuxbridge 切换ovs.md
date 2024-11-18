# Neutron Linuxbridge 切换到OVS

## 背景

在部署超融合系统时，neutron使用的linuxbridge，现有模块不满足当前测试需求，更换为ovs

## 基本信息

### 环境信息

系统：**openEuler release 22.03 (LTS-SP3)**

内核：5.10.0-220.0.0.123.aarch64

CPU：S5000C/64

### 网络规划

物理网地址

控制面地址

数据面地址



## 操作步骤

### 1. 记录现有网络信息

```bash
brctl show
ip address show
```

### 2. 停止Neutron Linux brdige agent 

```bash
systemctl stop neutron-linuxbridge-agent
```

### 3. 拆分现有Linux bridge

在迁移过程中，需要拆除当前的 Linux Bridge，并将其物理网卡接口配置到 OVS。

```bash
# 停止 Linux Bridge 并删除相关配置
ip link set br-lan down  # 假设 br-lan 是 Linux Bridge 的名称
brctl delbr br-lan
```

### 4. 创建OVS网桥

```bash
ovs-vsctl add-br br-ex  # 创建 OVS 网桥，名称可以根据你的需求命名
ovs-vsctl add-port br-ex <物理网卡名称>  # 将物理网卡加入 OVS 网桥
```

### 5. 配置IP地址和路由

⚠️ 可能会断网

```bash
ip addr add <IP地址>/<子网掩码> dev br-ex
ip link set br-ex up
```

### 6. 更新Neutron配置

```bash
```

