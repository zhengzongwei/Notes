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
   sudo apt install git python3-dev libffi-dev gcc libssl-dev  python3-pip libdbus-1-dev libdbus-glib-1-dev
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
   python3 -m venv /opt/kolla-ansible/.venv
   source /opt/kolla-ansible/.venv/bin/activate
   ```

   在运行任何命令之前，应激活虚拟环境： 取决于其中安装的软件包。

3. 确保安装了最新版本的 pip：

   ```
   pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
   pip install -U pip
   ```

4. 安装 [Ansible](http://www.ansible.com/)。Kolla Ansible 至少需要 支持高达 .安斯布核心不能更大 由于回归，比 2.14.2。`6``7`

   ```
   pip install 'ansible-core>=2.15,<2.17'
   pip install 'ansible>=6,<8'
   ```

### 安装 Kolla-ansible

1. 使用 安装 kolla-ansible 及其依赖项。`pip`

   ```
   pip install git+https://opendev.org/openstack/kolla-ansible@stable/2024.1
   ```

2. 创建目录。`/etc/kolla`

   ```
   sudo mkdir -p /etc/kolla
   sudo chown $USER:$USER /etc/kolla
   ```

3. 复制 和 到目录。`globals.yml``passwords.yml``/etc/kolla`

   ```
   cp -r /opt/kolla-ansible/.venv/share/kolla-ansible/etc_examples/kolla/* /etc/kolla
   ```

4. 将库存文件复制到当前目录。`all-in-one`

   ```
   cp /opt/kolla-ansible/.venv/share/kolla-ansible/ansible/inventory/all-in-one /etc/kolla
   ```

5. 配置部署文件

   ```yaml
   workaround_ansible_issue_8743: yes
   kolla_base_distro: "debian"
   kolla_dev_mode: true
   openstack_release: "2024.1"
   
   
   # aarch64
   openstack_tag_suffix: "-aarch64"
   kolla_internal_vip_address: "10.211.55.250"
   docker_registry: "quay.nju.edu.cn"
   network_interface: "enp0s5"
   neutron_external_interface: "enp0s6"
   nova_compute_virt_type: "qemu"
   
   enable_cinder: "yes"
   enable_cinder_backend_lvm: "yes"
   cinder_volume_group: "cinder-volumes"  # 需提前创建LVM卷组
   
   enable_skyline: "yes"
   
   
   
   
   
   
   less /etc/kolla/globals.yml
   
   workaround_ansible_issue_8743: yes
   kolla_base_distro: "debian"
   kolla_dev_mode: true
   openstack_release: "2024.1"
   
   
   # aarch64
   openstack_tag_suffix: "-aarch64"
   kolla_internal_vip_address: "10.211.55.250"
   docker_registry: "quay.nju.edu.cn"
   network_interface: "enp0s5"
   neutron_external_interface: "enp0s6"
   nova_compute_virt_type: "qemu"
   
   enable_neutron: "yes"
   enable_nova: "yes"
   
   # ironic
   enable_ironic: "yes"
   ironic_dnsmasq_interface: "ens160"
   ironic_cleaning_network: "public1"
   ironic_dnsmasq_dhcp_ranges:
     - range: "192.168.237.130,192.168.237.140"
   
   ironic_dnsmasq_boot_file: pxelinux.0
   ironic_inspector_kernel_cmdline_extras: ['ipa-lldp-timeout=90.0', 'ipa-collect-lldp=1']
   ironic_http_port: "8089"
   ironic_dnsmasq_serve_ipxe: "no"
   
   # curl https://tarballs.opendev.org/openstack/ironic-python-agent/dib/files/ipa-centos9-master.kernel -o /etc/kolla/config/ironic/ironic-agent.kernel
   
   # curl https://tarballs.opendev.org/openstack/ironic-python-agent/dib/files/ipa-centos9-master.initramfs -o /etc/kolla/config/ironic/ironic-agent.initramfs
   
   # skyline
   
   skyline_version: "2024.1"
   enable_skyline: "yes"
   skyline_enable_sso: "yes"
   
   
   ```

   

6. 开始部署

   ```shell
   # 
   kolla-ansible install-deps
   
   # 生成密码
   kolla-genpwd
   
   # 带有 kolla 部署依赖项的 Bootstrap 服务器
   kolla-ansible bootstrap-servers -i /etc/kolla/all-in-one
   
   # 安装前检查
   kolla-ansible prechecks -i /etc/kolla/all-in-one
   
   # 下载镜像
   kolla-ansible pull -i /etc/kolla/all-in-one 
   
   # 部署
   kolla-ansible deploy -i /etc/kolla/all-in-one 
   
   kolla-ansible reconfigure -i /etc/kolla/all-in-one 
   
   # 升级单组件
   docker pull quay.nju.edu.cn/openstack.kolla/skyline-apiserver:2024.1-debian-bookworm-aarch64
   docker pull quay.nju.edu.cn/openstack.kolla/skyline-console:2024.1-debian-bookworm-aarch64
   
   kolla-ansible -i /etc/kolla/all-in-one pull -t skyline
   kolla-ansible -i /etc/kolla/all-in-one upgrade -t skyline
   ```

## 参考链接

1. [支持矩阵 — kolla-ansible 16.1.0.dev7 文档 (openstack.org)](https://docs.openstack.org/kolla-ansible/latest/user/support-matrix)

2. [Quick Start for deployment/evaluation — kolla-ansible 19.1.0.dev108 documentation](https://docs.openstack.org/kolla-ansible/latest/user/quickstart.html)

   



