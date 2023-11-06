# DevStack 部署

## 系统环境

| 系统               | 内核                | openStack | 备注 |
| ------------------ | ------------------- | --------- | ---- |
| Openeuler-2203 LTS | 5.10.0-153.30.0.107 | 2023.1    | 失败 |
| Ubuntu 22.04.2 LTS | 5.15.0-76-generic   | 2023.1    |      |
|                    |                     |           |      |



## 安装部署

### 下载devstack

```shell

cd /opt/
git clone https://opendev.org/openstack/devstack
```

### 初始化的devtack环境配置

```shell
# 创建devstack 用户
/opt/devstack/tools/create-stack-user.sh

# 修改目录权限
sudo chown -R stack:stack /opt/devstack
chmod -R 755 /opt/devstack
chmod -R 755 /opt/stack
# 切换到要部署的openstack版本分支，以yoga为例，不切换的话，默认安装的是master版本的openstack

git checkout .
git checkout -b stable/zed
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

Q_PLUGIN=ml2
ENABLE_TENANT_VLANS=True
ML2_VLAN_RANGES=physnet1:1000:2000
```

### 部OpenStack

```shell
# devstack 用户执行
bash /opt/devstack/stack.sh
```

## 遇到问题

### Unable to create the network. No tenant network is available for allocation.

这是由于在创建network的时候需要先去取vlan id，但是这里没有配置VLAN RANGE，所以创建网络报错．

解决方法：在localrc中增加VLAN RANGE的配置项

```bash
Q_PLUGIN=ml2
ENABLE_TENANT_VLANS=True
ML2_VLAN_RANGES=physnet1:1000:2000
```



## 参考文档

1. [devstack官方文档]([DevStack — DevStack 文档 (openstack.org)](https://docs.openstack.org/devstack/latest/))

2. [OpenStack安装－DevStack]([OpenStack安装－DevStack (trystack.cn)](http://trystack.cn/Articles/devstack1.html))

