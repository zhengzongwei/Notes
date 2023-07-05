# Kolla-ansible 部署 Openstack

## 环境信息

服务器最低配置

2 个网卡接口

8GB 内存

40GB 磁盘

支持的操作系统

- CentOS Stream 9
- Debian Bullseye (11)
- openEuler 22.03 LTS
- Rocky Linux 9
- Ubuntu Jammy (22.04)



- 网卡

  nat网卡 

  桥接网卡



## 环境准备

### 系统设置

安装基本系统工具

```shell
yum -y install tmux vim

net-tools vim wget bash-completion lrzsz 
```

### 关闭Selinux 和防火墙

```shell
setenforce 0 
vim /etc/selinux/config
将SELINUX=enforcing改为SELINUX=disabled
systemctl stop firewalld && systemctl disable firewalld && systemctl status firewalld
```

### 修改hosts

```shell
vim /etc/hosts
192.168.130.138 openstack
```



### 构建python依赖项

1. 对于 Debian 或 Ubuntu，请更新软件包索引。

   ```
   sudo apt update
   ```

2. 安装 Python 构建依赖项：

   对于 CentOS、Rocky 或 openEuler，请运行：

   ```
   sudo dnf install git python3-devel libffi-devel gcc openssl-devel python3-libselinux
   ```

   对于 Debian 或 Ubuntu，运行：

   ```
   sudo apt install git python3-dev libffi-dev gcc libssl-dev
   ```

### 为虚拟环境安装依赖项

1. 安装虚拟环境依赖项。

   对于 CentOS、Rocky 或 openEuler，你不需要做任何事情。

   对于 Debian 或 Ubuntu，运行：

   ```
   sudo apt install python3-venv
   ```

2. 创建虚拟环境并激活它：

   ```
   python3 -m venv /path/to/venv
   source /path/to/venv/bin/activate
   ```

   在运行任何命令之前，应激活虚拟环境： 取决于其中安装的软件包。

3. 确保安装了最新版本的 pip：

   ```
   pip install -U pip
   ```

4. 安装 [Ansible](http://www.ansible.com/)。Kolla Ansible 至少需要 支持高达 .安斯布核心不能更大 由于回归，比 2.14.2。`6``7`

   ```
   pip install 'ansible-core>=2.13,<=2.14.2'
   pip install 'ansible>=6,<8'
   ```

### 安装 Kolla-ansible

1. 使用 安装 kolla-ansible 及其依赖项。`pip`

   ```
   pip install git+https://opendev.org/openstack/kolla-ansible@master
   ```

2. 创建目录。`/etc/kolla`

   ```
   sudo mkdir -p /etc/kolla
   sudo chown $USER:$USER /etc/kolla
   ```

3. 复制 和 到目录。`globals.yml``passwords.yml``/etc/kolla`

   ```
   cp -r /path/to/venv/share/kolla-ansible/etc_examples/kolla/* /etc/kolla
   ```

4. 将库存文件复制到当前目录。`all-in-one`

   ```
   cp /path/to/venv/share/kolla-ansible/ansible/inventory/all-in-one .
   ```





## 参考链接

1. [支持矩阵 — kolla-ansible 16.1.0.dev7 文档 (openstack.org)](https://docs.openstack.org/kolla-ansible/latest/user/support-matrix)

   


