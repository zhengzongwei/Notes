# DevStack 部署

## 系统环境

系统:Ubuntu 22.04.2 LTS

内核:5.15.0-76-generic

openStack版本: zed

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
```

### 部OpenStack

```shell
# devstack 用户执行
bash /opt/devstack/stack.sh
```





