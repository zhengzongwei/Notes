# DevStack 部署

## 系统环境

| 系统               | 内核                | openStack | 备注 |
| ------------------ | ------------------- | --------- | ---- |
| Openeuler-2203 LTS | 5.10.0-153.30.0.107 | 2023.1    | 失败 |
| Ubuntu 22.04.2 LTS | 5.15.0-76-generic   | 2023.1    |      |
| CentOS Stream 9    |                     | 2023.2    |      |

## 安装部署

### openeuler

### 下载devstack

```shell
git clone https://opendev.org/openstack/devstack /opt/devstack
```

### 初始化的devtack环境配置

```shell
# 创建devstack 用户
/opt/devstack/tools/create-stack-user.sh

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 修改目录权限
sudo chown -R stack:stack /opt/devstack
sudo chown -R stack:stack /opt/stack
chmod -R 755 /opt/devstack
chmod -R 755 /opt/stack

git checkout .
# 切换到要部署的openstack版本分支，以yoga为例，不切换的话，默认安装的是master版本的openstack
git checkout remotes/origin/stable/2023.2 -b stable/2023.2
```

### 初始化devstacl配置文件

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


Q_PLUGIN=ml2
ENABLE_TENANT_VLANS=True
ML2_VLAN_RANGES=physnet1:1000:2000


OVN_BUILD_FROM_SOURCE=True



# Enabling Neutron (network) Service
# openeuler 
enable_service placement-api 

disable_service n-net
enable_service q-svc
enable_service q-agt
enable_service q-dhcp
enable_service q-l3
enable_service q-meta
enable_service q-metering
enable_service neutron
enable_service horizon


## Neutron options
Q_USE_SECGROUP=True
FLOATING_RANGE="192.168.1.0/24"
FIXED_RANGE="10.0.0.0/24"
Q_FLOATING_ALLOCATION_POOL=start=192.168.1.102,end=192.168.1.110
PUBLIC_NETWORK_GATEWAY="192.168.1.2"
Q_L3_ENABLED=True
PUBLIC_INTERFACE=ens192
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
