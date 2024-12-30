# Kolla-ansible 部署 Openstack

## 环境信息

### 服务器最低配置

- CPU 4C

- 网卡

  - nat网卡


  - 桥接网卡


- 8G 内存

- 40GB 磁盘

- 系统 Debian 11 +
- openstack 版本 zed /2023.1

## 环境准备

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
   
   
   sudo apt install python3-pip
   
   
   ```

### 虚拟环境安装依赖项

1. 安装虚拟环境依赖项。

   对于 CentOS、Rocky 或 openEuler，你不需要做任何事情。

   对于 Debian 或 Ubuntu，运行：

   ```
   sudo apt install python3-venv python-is-python3
   ```

2. 创建虚拟环境并激活它：

   ```
   python3 -m venv /opt/cloud/.venv
   source /opt/cloud/.venv/bin/activate
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
   pip install git+https://opendev.org/openstack/kolla-ansible@stable/2023.2
   ```

2. 创建目录。`/etc/kolla`

   ```
   sudo mkdir -p /etc/kolla
   sudo chown $USER:$USER /etc/kolla
   ```

3. 复制 和 到目录。`globals.yml``passwords.yml``/etc/kolla`

   ```
   cp -r /opt/cloud/.venv/share/kolla-ansible/etc_examples/kolla/* /etc/kolla
   ```

4. 将库存文件复制到当前目录。`all-in-one`

   ```
   cp /opt/cloud/.venv/share/kolla-ansible/ansible/inventory/all-in-one /etc/kolla
   ```

5. 配置部署文件

   ```yaml
   less /etc/kolla/globals.yml
   
   workaround_ansible_issue_8743: yes
   kolla_base_distro: "debian"
   openstack_release: "2023.1"
   # aarch64
   openstack_tag_suffix: "-aarch64"
   kolla_internal_vip_address: "192.168.237.250"
   docker_registry: "quay.nju.edu.cn"
   network_interface: "ens160"
   neutron_external_interface: "ens192"
   enable_skyline: "yes"
   nova_compute_virt_type: "qemu"
   
   
   
   ```

   

6. 开始部署

   ```shell
   # 
   kolla-ansible install-deps
   
   # 生成密码
   kolla-genpwd
   
   # 带有 kolla 部署依赖项的 Bootstrap 服务器
   kolla-ansible -i /etc/kolla/all-in-one bootstrap-servers
   
   # 安装前检查
   kolla-ansible -i /etc/kolla/all-in-one prechecks
   
   # 下载镜像
   kolla-ansible -i /etc/kolla/all-in-one pull
   
   # 部署
   kolla-ansible -i /etc/kolla/all-in-one deploy
   ```

## 参考链接

1. [支持矩阵 — kolla-ansible 16.1.0.dev7 文档 (openstack.org)](https://docs.openstack.org/kolla-ansible/latest/user/support-matrix)



