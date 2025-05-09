# DevStack 部署

## 系统环境

| 系统               | 内核                | openStack | 备注 |
| ------------------ | ------------------- | --------- | ---- |
| Openeuler-2203 LTS | 5.10.0-153.30.0.107 | 2023.1    | 失败 |
| Ubuntu 22.04.2 LTS | 5.15.0-76-generic   | 2023.1    |      |
| CentOS Stream 9    |                     | 2023.2    |      |

## 安装部署

### openeuler

```bash
dnf install python3-devel httpd-devel gcc memcached pcp-system-tools groff
```



### 下载devstack

```shell
git clone https://opendev.org/openstack/devstack /opt/devstack
```

### 初始化的devtack环境配置

```shell
# 创建devstack 用户
/opt/devstack/tools/create-stack-user.sh

# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

/opt/stack/data/venv/bin/pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 修改目录权限
sudo chown -R stack:stack /opt/devstack
sudo chown -R stack:stack /opt/stack
sudo chmod -R 755 /opt/devstack
sudo chmod -R 755 /opt/stack

git checkout .
# 切换到要部署的openstack版本分支，以yoga为例，不切换的话，默认安装的是master版本的openstack
git checkout  -b stable/2023.2 remotes/origin/stable/2023.2
```

### 初始化devstacl配置文件

#### Base配置

```shell
切换到stack用户
su stack
此时，请确认stack用户的PATH环境变量是否包含了`/usr/sbin`，如果没有，则需要执行
PATH=$PATH:/usr/sbin
新增配置文件
vi /opt/devstack/local.conf

[[local|localrc]]
ADMIN_PASSWORD=admin
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD

GIT_BASE=http://git.trystack.cn
NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git

HOST_IP=127.0.0.1

OVN_BUILD_FROM_SOURCE=True

# 启用 Ironic
enable_plugin ironic https://opendev.org/openstack/ironic
enable_plugin ironic-ui https://opendev.org/openstack/ironic-ui
enable_service ironic
enable_service ironic-api
enable_service ironic-conductor
enable_service dhcp
enable_service dnsmasq
enable_service tftp
enable_service tempest

# 网络配置
FLAT_INTERFACE=ens34  # 替换为你的网络接口名称
PUBLIC_INTERFACE=ens33

# 使用 qemu 模拟裸机
IRONIC_DEPLOY_DRIVER=fake-hardware
IRONIC_ENABLED_NETWORK_INTERFACES=flat,neutron

# Enabling Neutron (network) Service
# openeuler 
# enable_service placement-api 

# disable_service n-net
# enable_service q-svc
# enable_service q-agt
# enable_service q-dhcp
# enable_service q-l3
# enable_service q-meta
# enable_service q-metering
# enable_service neutron
enable_plugin skyline-apiserver https://opendev.org/openstack/skyline-apiserver stable/2023.2
# disable_service horizon


## Neutron options
Q_USE_SECGROUP=True
FLOATING_RANGE="192.168.1.0/24"
FIXED_RANGE="10.0.0.0/24"
Q_FLOATING_ALLOCATION_POOL=start=10.211.55.100,end=10.211.55.110
PUBLIC_NETWORK_GATEWAY="10.211.55.2"
Q_L3_ENABLED=True
PUBLIC_INTERFACE=enp0s6
Q_USE_PROVIDERNET_FOR_PUBLIC=True
OVS_PHYSICAL_BRIDGE=br-ex
PUBLIC_BRIDGE=br-ex
OVS_BRIDGE_MAPPINGS=public:br-ex

# #VLAN configuration.
Q_PLUGIN=ml2
ENABLE_TENANT_VLANS=True
ML2_VLAN_RANGES=physnet1:1000:2000

# Logging
LOGFILE=/opt/stack/logs/stack.sh.log
VERBOSE=True
LOG_COLOR=True
SCREEN_LOGDIR=/opt/stack/logs

# aarch64 
[[post-config|$NOVA_CONF]]
[libvirt]
cpu_mode=custom
cpu_model=cortex-a72

```

#### Ubuntu 2204 LTS配置

```bash
"local.conf" [readonly] 20L, 496B                                                                        1,1           All
[[local|localrc]]
ADMIN_PASSWORD=admin
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD

GIT_BASE=http://git.trystack.cn
GIT_BASE=https://opendev.org/openstack
NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git

HOST_IP=127.0.0.1


enable_plugin skyline-apiserver https://opendev.org/openstack/skyline-apiserver stable/2023.2
disable_service horizon

[[post-config|$NOVA_CONF]]
[libvirt]
cpu_mode=custom
cpu_model=cortex-a72





[[local|localrc]]
ADMIN_PASSWORD=admin
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD
HOST_IP=192.168.248.143

# 启用 Skyline 组件
enable_plugin skyline-apiserver https://opendev.org/openstack/skyline-apiserver
enable_plugin skyline-console https://opendev.org/openstack/skyline-console
enable_service skyline-api skyline-console

# Neutron 网络配置
disable_service n-net
enable_service q-svc,q-agt,q-dhcp,q-l3,q-meta,neutron

# Neutron ML2 插件配置
[[post-config|$NEUTRON_CONF]]
[DEFAULT]
service_plugins = router
allow_overlapping_ips = True

[[post-config|/etc/neutron/plugins/ml2/ml2_conf.ini]]
[ml2]
type_drivers = flat,vxlan
tenant_network_types = vxlan
mechanism_drivers = openvswitch,l2population

[ml2_type_vxlan]
vni_ranges = 1:1000

[securitygroup]
enable_ipset = True

# Open vSwitch 配置
[[post-config|/etc/neutron/plugins/ml2/openvswitch_agent.ini]]
[agent]
tunnel_types = vxlan
l2_population = True

[ovs]
local_ip = $HOST_IP
bridge_mappings = public:br-ex

USE_PYTHON3=True

# 加速下载配置
GIT_BASE=http://git.trystack.cn
NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
USE_PYTHON3=True
```



#### debian 配置

```
[[local|localrc]]
# 基本密码设置
ADMIN_PASSWORD=admin
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD

# 使用国内镜像加速
GIT_BASE=http://git.trystack.cn
NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git

# 主机 IP 配置
HOST_IP=127.0.0.1

# 使用 OVN（Open Virtual Network）
OVN_BUILD_FROM_SOURCE=True

# 启用 Ironic
enable_plugin ironic https://opendev.org/openstack/ironic
enable_plugin ironic-ui https://opendev.org/openstack/ironic-ui
enable_service ironic
enable_service ironic-api
enable_service ironic-conductor
enable_service dhcp
enable_service dnsmasq
enable_service tftp
enable_service tempest

# 网络配置
FLAT_INTERFACE=ens33              # 平坦网络的物理网卡
PUBLIC_INTERFACE=ens34           # 公网访问的物理网卡

# 使用 qemu 模拟裸机
IRONIC_DEPLOY_DRIVER=fake-hardware
IRONIC_ENABLED_NETWORK_INTERFACES=flat,neutron

# 启用 Neutron 和 OVS
disable_service ovn-northd
disable_service ovn-controller
disable_service ovn-controller-vtep
disable_service ovn-metadata-agent
disable_service ovn

enable_service q-svc              # 启用 Neutron 服务
# enable_service q-agt              # 启用 Neutron OVS Agent
enable_service q-dhcp             # 启用 DHCP 服务
enable_service q-l3               # 启用 L3 路由
enable_service q-meta             # 启用 Metadata 服务
enable_service q-ovs

# 启用 Skyline 组件
enable_plugin skyline-apiserver https://opendev.org/openstack/skyline-apiserver stable/2023.2
# disable_service horizon          # 禁用 Horizon

## Neutron 网络选项
Q_USE_SECGROUP=True
FLOATING_RANGE="192.168.31.0/24"    # 浮动 IP 范围
FIXED_RANGE="10.0.0.0/24"          # 固定 IP 范围
Q_FLOATING_ALLOCATION_POOL=start=192.168.31.200,end=192.168.31.210
PUBLIC_NETWORK_GATEWAY="192.168.31.1"
Q_L3_ENABLED=True
Q_USE_PROVIDERNET_FOR_PUBLIC=True

# Open vSwitch 配置
OVS_PHYSICAL_BRIDGE=br-ex          # 公网桥接
PUBLIC_BRIDGE=br-ex
OVS_BRIDGE_MAPPINGS=public:br-ex   # 将物理网络映射到 br-ex

# VLAN 配置
Q_PLUGIN=ml2
ENABLE_TENANT_VLANS=True
ML2_VLAN_RANGES=physnet1:1000:2000

# 日志配置
LOGFILE=/opt/stack/logs/stack.sh.log
VERBOSE=True
LOG_COLOR=True
SCREEN_LOGDIR=/opt/stack/logs

# ARM 架构配置
[[post-config|$NOVA_CONF]]
[libvirt]
cpu_mode=custom
cpu_model=cortex-a72
```



#### openeuler 配置

```bash
[[local|localrc]]
ADMIN_PASSWORD=admin
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD

OVN_BUILD_FROM_SOURCE=True


GIT_BASE=http://git.trystack.cn
GIT_BASE=https://opendev.org/openstack
NOVNC_REPO=http://git.trystack.cn/kanaka/noVNC.git
SPICE_REPO=http://git.trystack.cn/git/spice/spice-html5.git

HOST_IP=127.0.0.1
RECLONE=False
PIP_UPGRADE=True

[[post-config|$NOVA_CONF]]
[libvirt]
cpu_mode=custom
cpu_model=cortex-a72
```



#### centos 配置



### Delpoy DevStack

```shell
# devstack 用户执行
bash /opt/devstack/stack.sh
```



```bash
# admin-openrc
export OS_PROJECT_DOMAIN_ID=default
export OS_USER_DOMAIN_ID=default
export OS_PROJECT_NAME=admin
export OS_TENANT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=ADMIN_PASS
export OS_AUTH_URL=http://192.168.237.143/identify
export OS_IDENTITY_API_VERSION=3
```



## 遇到问题IP

### Unable to create the network. No tenant network is available for allocation

这是由于在创建network的时候需要先去取vlan id，但是这里没有配置VLAN RANGE，所以创建网络报错．

解决方法：在localrc中增加VLAN RANGE的配置项

```bash
Q_PLUGIN=ml2
ENABLE_TENANT_VLANS=True
ML2_VLAN_RANGES=physnet1:1000:2000
```

### ModuleNotFoundError: No module named 'pbr.build'

安装模块 pip install pbr

### 页面打不开

```bash
/sbin/iptables -I INPUT -p tcp --dport 80 -j ACCEPT
```

## 调试

```bash
# 查看特定服务日志
sudo journalctl -f --unit devstack@n-cpu.service


# 查看neutron server 日志
sudo journalctl -f --unit devstack@q-svc.service

# 查看指定日期日志
sudo journalctl --since "2023-12-29 13:00:00" --unit "2023-12-29 14:00:00" devstack@q-svc.service > neutron.log
```



## 参考文档

1. [devstack官方文档]([DevStack — DevStack 文档 (openstack.org)](https://docs.openstack.org/devstack/latest/))

2. [OpenStack安装－DevStack]([OpenStack安装－DevStack (trystack.cn)](http://trystack.cn/Articles/devstack1.html))
