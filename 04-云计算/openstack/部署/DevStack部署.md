# DevStack 部署

## 系统环境

系统：openEuler 2203 LTS SP1

内核：5.10.0-136.12.0.86.oe2203sp1.x86_64

openStack版本：Wallaby

## 安装部署

### 下载devstack

```shell
dnf install -y
dnf install git
cd /opt/
git clone https://opendev.org/openstack/devstack
```

### 初始化的devtack环境配置

```shell
# 创建devstack 用户
/opt/devstack/tools/create-stack-user.sh

# 修改目录权限
chown -R stack:stack /opt/devstack
chmod -R 755 /opt/devstack
chmod -R 755 /opt/stack
# 切换到要部署的openstack版本分支，以yoga为例，不切换的话，默认安装的是master版本的openstack
git checkout stable/wallaby
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
DATABASE_PASSWORD=root
RABBIT_PASSWORD=root
SERVICE_PASSWORD=root
ADMIN_PASSWORD=root
OVN_BUILD_FROM_SOURCE=True
```

openEuler没有提供OVN的RPM软件包，因此需要配置`OVN_BUILD_FROM_SOURCE=True`, 从源码编译OVN

另外如果使用的是arm64虚拟机环境，则需要配置libvirt嵌套虚拟化，在`local.conf`中追加如下配置：

```shell
[[post-config|$NOVA_CONF]]
[libvirt]
cpu_mode=custom
cpu_model=cortex-a72
```

如果安装Ironic，需要提前安装依赖：

```shell
sudo dnf install syslinux-nonlinux
```

### 部署OpenStack

```shell
# devstack 用户执行
bash /opt/devstack stack.sh
```





