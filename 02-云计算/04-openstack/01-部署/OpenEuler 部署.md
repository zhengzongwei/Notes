# openEuler OpenStack Bobcat

## 系统配置

```bash
#  dnf install gcc python3-devel python3-unversioned-command git 

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### SElinux 配置

```bash
# 关闭 SELinux
setenforce 0
vi /etc/selinux/config
SELINUX=disabled
```

### 防火墙

```bash
systemctl stop firewalld && systemctl disable firewalld
systemctl status firewalld
```

## 中间件部署

### SQL DataBase

```bash
yum install mariadb mariadb-server python3-PyMySQL

vim /etc/my.cnf.d/openstack.cnf
[mysqld]
bind-address = 192.168.31.196
default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8



systemctl enable mariadb.service
systemctl start mariadb.service
```

### RabbitMQ

```bash
yum install rabbitmq-server

systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service

rabbitmqctl add_user openstack openstack

rabbitmqctl set_permissions openstack ".*" ".*" ".*"

rabbitmq-plugins enable rabbitmq_management 
```

### Memcached

```bash
yum install memcached python3-memcached

vim /etc/sysconfig/memcached

OPTIONS="-l 127.0.0.1,::1,controller"

systemctl enable memcached.service
systemctl start memcached.service

memcached-tool controller stats
```

## OpenStack 组件部署

### Keystone

- 配置系统环境

  ```bash
  # 安装系统依赖包
  dnf install httpd mod_wsgi
  
  # 创建keystone用户
  getent group keystone >/dev/null || groupadd -r keystone 
  if ! getent passwd keystone >/dev/null; then
    useradd -r -g keystone -G keystone,nobody -d /var/lib/keystone -s /sbin/nologin -c "OpenStack Keystone Daemons" keystone
  fi
  
  # 创建文件夹
  mkdir -p /etc/keystone/ /var/lib/keystone /var/log/keystone
  
  # 赋予相关权限
  chown -R keystone:keystone /etc/keystone/ /var/lib/keystone /var/log/keystone
  ```

- 克隆源码

  ```bash
  git clone https://opendev.org/openstack/keystone.git /opt/keystone
  ```

- 虚拟环境配置

  ```bash
  python -m venv /opt/keystone/venv
  source /opt/ketstone/venv/bin/activate
  
  # 安装依赖包
  pip install -r keystone.txt
  
  # 安装keystone
  python /opt/keystone/setup.py install
  
  # 系统nova环境
  cp /opt/keystone/venv/bin/keystone-* /usr/bin/
  ```

- 数据库配置

  ```bash
  # 数据库操作
  CREATE DATABASE keystone;
  
  GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' \
  IDENTIFIED BY 'keystone';
  
  GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' \
  IDENTIFIED BY 'keystone';
  
  # 退出数据库后操作 同步数据
  keystone-manage db_sync
  
  # 初始化Fernet密钥仓库
  keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
  keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
  ```

- keystone配置

  ```bash
  # vim /etc/keystone/keystone.conf
  
  [database]
  connection = mysql+pymysql://keystone:keystone@controller/keystone
  
  [token]
  provider = fernet
  
  
  
  keystone-manage bootstrap --bootstrap-password admin \
  --bootstrap-admin-url http://controller:5000/v3/ \
  --bootstrap-internal-url http://controller:5000/v3/ \
  --bootstrap-public-url http://controller:5000/v3/ \
  --bootstrap-region-id RegionOne
  
  ln -s /opt/keystone/httpd/wsgi-keystone.conf /etc/httpd/conf.d/
  
  vim /etc/httpd/conf.d/wsgi-keystone.conf
  Listen 5000
  
  <VirtualHost *:5000>
      WSGIDaemonProcess keystone-public processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP} home=/opt/keystone python-home=/opt/keystone/venv python-path=/opt/keystone/venv/lib/python3.9/site-packages
      WSGIProcessGroup keystone-public
      WSGIScriptAlias / /opt/keystone/venv/bin/keystone-wsgi-public
      WSGIApplicationGroup %{GLOBAL}
      WSGIPassAuthorization On
      LimitRequestBody 114688
      <IfVersion >= 2.4>
        ErrorLogFormat "%{cu}t %M"
      </IfVersion>
      ErrorLog /var/log/httpd/keystone_error.log
      CustomLog /var/log/httpd/keystone_access.log combined
  
      <Directory /opt/keystone/venv>
          <IfVersion >= 2.4>
              Require all granted
          </IfVersion>
          <IfVersion < 2.4>
              Order allow,deny
              Allow from all
          </IfVersion>
      </Directory>
  </VirtualHost>
  Alias /identity /opt/keystone/venv/bin/keystone-wsgi-public
  <Location /identity>
      SetHandler wsgi-script
      Options +ExecCGI
  
      WSGIProcessGroup keystone-public
      WSGIApplicationGroup %{GLOBAL}
      WSGIPassAuthorization On
  </Location>
  
  
  systemctl restart httpd
  
  
  
  ```

- 服务创建

  ```bash
  # 创建环境变量
  cat << EOF >> ~/.admin-openrc
  export OS_PROJECT_DOMAIN_NAME=Default
  export OS_USER_DOMAIN_NAME=Default
  export OS_PROJECT_NAME=admin
  export OS_USERNAME=admin
  export OS_PASSWORD=admin
  export OS_AUTH_URL=http://controller:5000/v3
  export OS_IDENTITY_API_VERSION=3
  export OS_IMAGE_API_VERSION=2
  EOF
  
  openstack domain create --description "An Example Domain" example
  
  openstack project create --domain default --description "Service Project" service
  
  openstack project create --domain default --description "Demo Project" demo-project
  openstack user create --domain default --password-prompt demo
  openstack role create demo
  openstack role add --project demo-project --user demo demo
  ```

- 验证

  ```bash
  openstack --os-auth-url http://controller:5000/v3 \
  --os-project-domain-name Default --os-user-domain-name Default \
  --os-project-name admin --os-username admin token issue
  
  ```

  

```bash
git clone https://opendev.org/openstack/keystone.git /opt/keystone
python -m venv /opt/keystone/venv


CREATE DATABASE keystone;

GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' \
IDENTIFIED BY 'keystone';

GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' \
IDENTIFIED BY 'keystone';
```

```bash
# 安装软件包
dnf install httpd mod_wsgi

# 配置keystone
mkdir -p /etc/keystone/
vim /etc/keystone/keystone.conf

[database]
connection = mysql+pymysql://keystone:keystone@controller/keystone

[token]
provider = fernet

# 系统nova环境
cp /opt/keystone/venv/bin/keystone-* /usr/bin/

# 同步数据
keystone-manage db_sync


# 初始化Fernet密钥仓库

keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
keystone-manage credential_setup --keystone-user keystone --keystone-group keystone

chown -R keystone:keystone /etc/keystone
chown -R keystone:keystone /opt/keystone

# 启动服务
keystone-manage bootstrap --bootstrap-password admin \
--bootstrap-admin-url http://controller:5000/v3/ \
--bootstrap-internal-url http://controller:5000/v3/ \
--bootstrap-public-url http://controller:5000/v3/ \
--bootstrap-region-id RegionOne

keystone-manage bootstrap --bootstrap-password admin \
--bootstrap-admin-url http://controller:5000/v2/ \
--bootstrap-internal-url http://controller:5000/v2/ \
--bootstrap-public-url http://controller:5000/v2/ \
--bootstrap-region-id RegionOne

ln -s /opt/keystone/httpd/wsgi-keystone.conf /etc/httpd/conf.d/

systemctl enable httpd.service
systemctl start httpd.service

vim /etc/httpd/conf.d/wsgi-keystone.conf
Listen 5000

<VirtualHost *:5000>
    WSGIDaemonProcess keystone-public processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP} home=/opt/keystone python-home=/opt/keystone/venv python-path=/opt/keystone/venv/lib/python3.9/site-packages
    WSGIProcessGroup keystone-public
    WSGIScriptAlias / /opt/keystone/venv/bin/keystone-wsgi-public
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    LimitRequestBody 114688
    <IfVersion >= 2.4>
      ErrorLogFormat "%{cu}t %M"
    </IfVersion>
    ErrorLog /var/log/httpd/keystone_error.log
    CustomLog /var/log/httpd/keystone_access.log combined

    <Directory /opt/keystone/venv>
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
        <IfVersion < 2.4>
            Order allow,deny
            Allow from all
        </IfVersion>
    </Directory>
</VirtualHost>
Alias /identity /opt/keystone/venv/bin/keystone-wsgi-public
<Location /identity>
    SetHandler wsgi-script
    Options +ExecCGI

    WSGIProcessGroup keystone-public
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
</Location>


# 创建环境变量
cat << EOF >> ~/.admin-openrc
export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=admin
export OS_AUTH_URL=http://controller:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
EOF



openstack domain create --description "An Example Domain" example

openstack project create --domain default --description "Service Project" service

openstack project create --domain default --description "Demo Project" demo-project
openstack user create --domain default --password-prompt demo
openstack role create demo
openstack role add --project demo-project --user demo demo

# 验证
openstack --os-auth-url http://controller:5000/v3 \
--os-project-domain-name Default --os-user-domain-name Default \
--os-project-name admin --os-username admin token issue

```

### Glance

```bash
# 创建用户
getent group glance >/dev/null || groupadd -r glance
if ! getent passwd glance >/dev/null; then
  useradd -r -g glance -G glance,nobody -d /var/lib/glance -s /sbin/nologin -c "OpenStack Glance Daemons" glance
fi

# 相关文件夹创建
mkdir -p /var/lib/glance/ /var/log/glance /etc/glance /etc/glance/glance-api.conf.d/ /etc/glance/glance.conf.d/
# 创建数据库
CREATE DATABASE glance;
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' IDENTIFIED BY 'glance';
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY 'glance';

# 创建服务凭证
openstack user create --domain default --password-prompt glance
openstack role add --project service --user glance admin
openstack service create --name glance --description "OpenStack Image" image

# 创建端点
openstack endpoint create --region RegionOne image public http://controller:9292
openstack endpoint create --region RegionOne image internal http://controller:9292
openstack endpoint create --region RegionOne image admin http://controller:9292

# 安装glance 包
git clone https://opendev.org/openstack/glance.git /opt/glance
# 切换分支
cd /opt/glance/
git checkout -b stable/2023.2 remotes/origin/stable/2023.2

# 配置环境
python -m venv /opt/glance/venv
source /opt/glance/venv/bin/activate
pip install -r glance.txt
python setup.py install
cp /opt/glance/venv/bin/glance-* /usr/bin/

# 配置文件
vim /etc/glance/glance-api.conf
[database]
connection = mysql+pymysql://glance:glance@controller/glance

[keystone_authtoken]
www_authenticate_uri  = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = glance
password = glance

[paste_deploy]
flavor = keystone

[glance_store]
stores = file,http
default_store = file
filesystem_store_datadir = /var/lib/glance/images/



chown -R glance:glance /etc/glance/ /var/log/glance/ /var/lib/glance/
chown -R glance:glance /var/log/glance/
chown -R glance:glance /var/lib/glance/

cp /opt/pkgs/openstack-glance/openstack-glance.logrotate/ /etc/logrotate.d/glance

cp /opt/pkgs/openstack-glance/openstack-glance-api.service /usr/lib/systemd/system/
systemctl enable openstack-glance-api.service
systemctl restart  openstack-glance-api.service

openstack image create --disk-format qcow2 --container-format bare --file cirros-0.6.2-aarch64-disk.img --public cirros

```

### Placement

```bash
getent group placement >/dev/null || groupadd -r placement 
if ! getent passwd placement >/dev/null; then
  useradd -r -g placement -G placement,nobody -d /var/lib/placement -s /sbin/nologin -c "OpenStack Placement Daemons" placement
fi

git clone https://gitee.com/src-openeuler/placement.git /opt/placement

python -m venv /opt/placement/venv

git checkout -b stable/2023.2 remotes/origin/stable/2023.2
python setup.py install
cp /opt/placement/venv/bin/placement-* /usr/bin/
cp -r /opt/placement/etc/placement/ /etc/
mkdir -p /var/log/placement/ 

CREATE DATABASE placement;
GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'localhost' IDENTIFIED BY 'placement';
GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'%' IDENTIFIED BY 'placement';





# 创建Placement API服务
openstack user create --domain default --password-prompt placement
openstack role add --project service --user placement admin
openstack service create --name placement --description "Placement API" placement

# 创建服务端点
openstack endpoint create --region RegionOne placement public http://controller:8778
openstack endpoint create --region RegionOne placement internal http://controller:8778
openstack endpoint create --region RegionOne placement admin http://controller:8778

# 配置文件
vim /etc/placement/placement.conf

[placement_database]
connection = mysql+pymysql://placement:placement@controller/placement
[api]
auth_strategy = keystone
[keystone_authtoken]
auth_url = http://controller:5000/v3
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = placement
password = placement

placement-manage db sync


vim /etc/httpd/conf.d/00-placement-api.conf
Listen 8778

<VirtualHost *:8778>
  WSGIProcessGroup placement-api
  WSGIApplicationGroup %{GLOBAL}
  WSGIPassAuthorization On
  WSGIDaemonProcess placement-api processes=5 threads=1 user=placement group=placement display-name=%{GROUP} home=/opt/placement python-home=/opt/placement/venv python-path=/opt/placement/venv/lib/python3.9/site-packages
  WSGIScriptAlias / /usr/bin/placement-api
  <IfVersion >= 2.4>
    ErrorLogFormat "%M"
  </IfVersion>
  ErrorLog /var/log/placement/placement-api.log
  #SSLEngine On
  #SSLCertificateFile ...
  #SSLCertificateKeyFile ...
    <Directory /usr/bin>
    <IfVersion >= 2.4>
      Require all granted
    </IfVersion>
    <IfVersion < 2.4>
      Order allow,deny
      Allow from all
    </IfVersion>
  </Directory>
  <Directory /opt/keystone/venv/bin>
    <IfVersion >= 2.4>
      Require all granted
    </IfVersion>
    <IfVersion < 2.4>
      Order allow,deny
      Allow from all
    </IfVersion>
  </Directory>
</VirtualHost>

Alias /placement-api /opt/keystone/venv/bin/placement-api
<Location /placement-api>
  SetHandler wsgi-script
  Options +ExecCGI
  WSGIProcessGroup placement-api
  WSGIApplicationGroup %{GLOBAL}
  WSGIPassAuthorization On
</Location>


# 验证

curl http://controller:8778

placement-status upgrade check

```

### Nova

```bash
getent group nova >/dev/null || groupadd -r nova 
if ! getent passwd nova >/dev/null; then
  useradd -r -g nova -G nova,nobody -d /var/lib/nova -s /sbin/nologin -c "OpenStack Nova Daemons" nova
fi

dnf install novnc libvirt*

usermod -aG libvirt nova
chown -R nova:nova /opt/nova/


git clone https://opendev.org/openstack/nova.git /opt/nova
python -m venv /opt/nova/venv


git checkout -b stable/2023.2 remotes/origin/stable/2023.2
source /opt/nova/venv/bin/activate

pip install -r nova.txt

# 数据库配置

CREATE DATABASE nova_api;
CREATE DATABASE nova;
CREATE DATABASE nova_cell0;
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' IDENTIFIED BY 'nova';
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY 'nova';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' IDENTIFIED BY 'nova';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY 'nova';
GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' IDENTIFIED BY 'nova';
GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' IDENTIFIED BY 'nova';

# 服务凭证
openstack user create --domain default --password-prompt nova

openstack role add --project service --user nova admin

openstack service create --name nova --description "OpenStack Compute" compute

# 端点
openstack endpoint create --region RegionOne compute public http://controller:8774/v2.1

openstack endpoint create --region RegionOne compute internal http://controller:8774/v2.1

openstack endpoint create --region RegionOne compute admin http://controller:8774/v2.1


cp /opt/nova/venv/bin/nova-* /usr/bin/
cp -r /opt/nova/etc/nova/ /etc/
mkdir -p /var/log/nova/ /var/lib/nova/instances/

git clone https://gitee.com/src-openeuler/openstack-nova.git
# 软件包 需修改

cp /opt/pkgs/openstack-nova/openstack-nova-api.service \
/opt/pkgs/openstack-nova/openstack-nova-compute.service \
/opt/pkgs/openstack-nova/openstack-nova-conductor.service \
/opt/pkgs/openstack-nova/openstack-nova-scheduler.service \
/opt/pkgs/openstack-nova/openstack-nova-novncproxy.service \
/usr/lib/systemd/system/


vim /etc/nova/nova.conf

[DEFAULT]
enabled_apis = osapi_compute,metadata
transport_url = rabbit://openstack:openstack@controller:5672/
my_ip = 192.168.31.196
use_neutron = true
firewall_driver = nova.virt.firewall.NoopFirewallDriver
compute_driver=libvirt.LibvirtDriver
instances_path = /var/lib/nova/instances/
lock_path = /var/lib/nova/tmp
log_dir = /var/log/nova/

[api_database]
connection = mysql+pymysql://nova:nova@controller/nova_api

[database]
connection = mysql+pymysql://nova:nova@controller/nova

[api]
auth_strategy = keystone

[keystone_authtoken]
www_authenticate_uri = http://controller:5000/
auth_url = http://controller:5000/
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = nova
password = nova

[vnc]
enabled = true
server_listen = $my_ip
server_proxyclient_address = $my_ip
novncproxy_base_url = http://controller:6080/vnc_auto.html

[libvirt]
virt_type = qemu
# cpu_mode = custom
# cpu_model = cortex-a72

[glance]
api_servers = http://controller:9292

[oslo_concurrency]
lock_path = /var/lib/nova/tmp

[placement]
region_name = RegionOne
project_domain_name = Default
project_name = service
auth_type = password
user_domain_name = Default
auth_url = http://controller:5000/v3
username = placement
password = placement

[neutron]
auth_url = http://controller:5000
auth_type = password
project_domain_name = default
user_domain_name = default
region_name = RegionOne
project_name = service
username = neutron
password = neutron
service_metadata_proxy = true
metadata_proxy_shared_secret = METADATA_SECRET   


# 同步数据库
nova-manage api_db sync
nova-manage cell_v2 map_cell0
nova-manage cell_v2 create_cell --name=cell1 --verbose
nova-manage db sync
nova-manage cell_v2 list_cells
nova-manage cell_v2 discover_hosts --verbose

# 启动服务
cp openstack-nova-api.service openstack-nova-scheduler.service openstack-nova-conductor.service openstack-nova-novncproxy.service /usr/lib/systemd/system/

systemctl restart \
openstack-nova-api.service \
openstack-nova-scheduler.service \
openstack-nova-conductor.service \
openstack-nova-novncproxy.service

```

### Neutron

```bash
# 创建用户
getent group neutron >/dev/null || groupadd -r neutron
if ! getent passwd neutron >/dev/null; then
  useradd -r -g neutron -G neutron,nobody -d /var/lib/neutron -s /sbin/nologin -c "OpenStack Neutron Daemons" neutron
fi

# 相关文件夹创建
mkdir -p /var/lib/neutron/ /var/log/neutron /etc/neutron /usr/share/neutron/server /usr/share/neutron/l3_agent /etc/neutron/conf.d/common /etc/neutron/conf.d/neutron-server/ etc/neutron/conf.d/neutron-metadata-agent /etc/neutron/conf.d/neutron-dhcp-agent /etc/neutron/conf.d/neutron-l3-agent  /etc/neutron/conf.d/neutron-linuxbridge-agent

# 数据库
CREATE DATABASE neutron;
GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' IDENTIFIED BY 'neutron';
GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' IDENTIFIED BY 'neutron';

# 服务凭证
openstack user create --domain default --password-prompt neutron
openstack role add --project service --user neutron admin
openstack service create --name neutron --description "OpenStack Networking" network

# Endpoint
openstack endpoint create --region RegionOne network public http://controller:9696

openstack endpoint create --region RegionOne network internal http://controller:9696
openstack endpoint create --region RegionOne network admin http://controller:9696 


# 包安装
 dnf install ebtables ipset
 
 
git clone https://opendev.org/openstack/neutron.git /opt/neutron
python -m venv /opt/neutron/venv


git checkout -b stable/2023.2 remotes/origin/stable/2023.2
source /opt/neutron/venv/bin/activate


cp -r  /opt/neutron/etc/neutron/* /etc/neutron/

# 配置文件
vim /etc/neutron/neutron.conf

[DEFAULT]
core_plugin = ml2
service_plugins = router
allow_overlapping_ips = true
transport_url = rabbit://openstack:openstack@controller
auth_strategy = keystone
notify_nova_on_port_status_changes = true
notify_nova_on_port_data_changes = true
api_workers = 3  

[database]
connection = mysql+pymysql://neutron:neutron@controller/neutron

[keystone_authtoken]
www_authenticate_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = neutron
password = neutron

[nova]
auth_url = http://controller:5000
auth_type = password
project_domain_name = Default
user_domain_name = Default
region_name = RegionOne
project_name = service
username = nova
password = nova

[oslo_concurrency]
lock_path = /var/lib/neutron/tmp

[experimental]
linuxbridge = true

vim /etc/neutron/plugins/ml2/ml2_conf.ini

[ml2]
type_drivers = flat,vlan,vxlan
tenant_network_types = vxlan
mechanism_drivers = linuxbridge,l2population
extension_drivers = port_security

[ml2_type_flat]
flat_networks = provider

[ml2_type_vxlan]
vni_ranges = 1:1000

[securitygroup]
enable_ipset = true


ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini




vim /etc/neutron/plugins/ml2/linuxbridge_agent.ini

[linux_bridge]
physical_interface_mappings = provider:PROVIDER_INTERFACE_NAME

[vxlan]
enable_vxlan = true
local_ip = OVERLAY_INTERFACE_IP_ADDRESS
l2_population = true

[securitygroup]
enable_security_group = true
firewall_driver = neutron.agent.linux.iptables_firewall.IptablesFirewallDriver


vim /etc/neutron/l3_agent.ini

[DEFAULT]
interface_driver = linuxbridge


vim /etc/neutron/dhcp_agent.ini

[DEFAULT]
interface_driver = linuxbridge
dhcp_driver = neutron.agent.linux.dhcp.Dnsmasq
enable_isolated_metadata = true

vim /etc/neutron/metadata_agent.ini
[DEFAULT]
nova_metadata_host = controller
metadata_proxy_shared_secret = METADATA_SECRET


neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head

su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf \
--config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron



cp /opt/pkgs/neutron/openstack-neutron/neutron-linuxbridge-agent.service \
/opt/pkgs/neutron/openstack-neutron/neutron-server.service \
/opt/pkgs/neutron/openstack-neutron/neutron-dhcp-agent.service \
/opt/pkgs/neutron/openstack-neutron/neutron-metadata-agent.service \
/opt/pkgs/neutron/openstack-neutron/neutron-l3-agent.service \
/usr/lib/systemd/system/

cp /opt/pkgs/openstack-neutron/neutron-linuxbridge-agent.service \
/opt/pkgs/openstack-neutron/neutron-server.service \
/opt/pkgs/openstack-neutron/neutron-dhcp-agent.service \
/opt/pkgs/openstack-neutron/neutron-metadata-agent.service \
/opt/pkgs/openstack-neutron/neutron-l3-agent.service \
/usr/lib/systemd/system/


systemctl restart openstack-nova-api.service

cp neutron-dist.conf /usr/share/neutron/

cp neutron-enable-bridge-firewall.sh /usr/bin/

cp /opt/neutron/etc/api-paste.ini /usr/share/neutron/

chown -R neutron:neutron /usr/share/neutron /var/log/neutron /var/lib/neutron 

# 虚拟环境配置，缺失 rootwrap.conf
vim /etc/neutron/rootwrap.d/rootwrap.filters
privsep-helper: CommandFilter, /opt/neutron/venv/bin/privsep-helper, root

cp neutron-sudoers /etc/sudoers.d/neutron
neutron-linuxbridge-agent.service


systemctl restart neutron-server.service \
neutron-linuxbridge-agent.service \
neutron-dhcp-agent.service \
neutron-metadata-agent.service \
neutron-l3-agent.service
```

### Cinder

```bash
# 创建用户
getent group cinder >/dev/null || groupadd -r cinder
if ! getent passwd cinder >/dev/null; then
  useradd -r -g cinder -G cinder,nobody -d /var/lib/cinder -s /sbin/nologin -c "OpenStack Cinder Daemons" cinder
fi
# 文件夹创建
mkdir -p /var/log/cinder/ /var/lib/cinder /etc/cinder

chown -R cinder:cinder /var/log/cinder/ /var/lib/cinder /etc/cinder

dnf install lvm2 scsi-target-utils rpcbind nfs-utils
# 数据库
CREATE DATABASE cinder;
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' IDENTIFIED BY 'cinder';
GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' IDENTIFIED BY 'cinder';

# 服务凭证
openstack user create --domain default --password-prompt cinder
openstack role add --project service --user cinder admin
openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2
openstack service create --name cinderv3 --description "OpenStack Block Storage" volumev3

# Endpoint
openstack endpoint create --region RegionOne volumev2 public http://controller:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne volumev2 internal http://controller:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne volumev2 admin http://controller:8776/v2/%\(project_id\)s
openstack endpoint create --region RegionOne volumev3 public http://controller:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne volumev3 internal http://controller:8776/v3/%\(project_id\)s
openstack endpoint create --region RegionOne volumev3 admin http://controller:8776/v3/%\(project_id\)s


# service 服务文件
git checkout -b 2023.2 remotes/origin/Multi-Version_OpenStack-Antelope_openEuler-24.03-LTS

cp cinder-sudoers /etc/sudoers.d/cinder

cp openstack-cinder-api.service \
   openstack-cinder-volume.service \
   openstack-cinder-scheduler.service \
   openstack-cinder-backup.service \
   /usr/lib/systemd/system/


# 准备存储设备
pvcreate /dev/sdc
vgcreate cinder-volumes /dev/sdc

vim /etc/lvm/lvm.conf


devices {
...
filter = [ "a/sdc/", "r/.*/"]


# 准备NFS

mkdir -p /data/cinder/backup

cat << EOF >> /etc/export
/data/cinder/backup
192.168.31.196.0/24(rw,sync,no_root_squash,no_all_squash)
EOF

# 配置文件
vim /etc/cinder/cinder.conf

[DEFAULT]
transport_url = rabbit://openstack:openstack@controller
auth_strategy = keystone
my_ip = 10.211.55.17
enabled_backends = lvm
backup_driver=cinder.backup.drivers.nfs.NFSBackupDriver
backup_share=controller:/data/cinder/backup

[database]
connection = mysql+pymysql://cinder:cinder@controller/cinder

[keystone_authtoken]
www_authenticate_uri = http://controller:5000
auth_url = http://controller:5000
memcached_servers = controller:11211
auth_type = password
project_domain_name = Default
user_domain_name = Default
project_name = service
username = cinder
password = cinder

[oslo_concurrency]
lock_path = /var/lib/cinder/tmp

[lvm]
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
volume_group = cinder-volumes
iscsi_protocol = iscsi
iscsi_helper = tgtadm

# 

cinder-manage db sync


systemctl enable openstack-cinder-api.service openstack-cinder-scheduler.service 

systemctl enable rpcbind.service nfs-server.service tgtd.service iscsid.service \
                 openstack-cinder-volume.service \
                 openstack-cinder-backup.service
                 
                 
# /etc/tgt/tgtd.conf
include /var/lib/cinder/volumes/*


systemctl restart openstack-cinder-api.service openstack-cinder-scheduler.service \
rpcbind.service nfs-server.service tgtd.service iscsid.service \
                 openstack-cinder-volume.service \
                 openstack-cinder-backup.service

```

### 验证

```bash
# 创建网络
 openstack network create --project bff2e2c0897945ef8fc242c2e8c34c99 --share --provider-network-type flat --provider-physical-network provider sharednet
 # 创建子网
 openstack subnet create subnet --network sharednet --project bff2e2c0897945ef8fc242c2e8c34c99 --subnet-range 10.0.0.0/24 --allocation-pool start=10.0.0.200,end=10.0.0.254 --gateway 10.0.0.1 --dns-nameserver 10.0.0.10
 # 创建flavor
 openstack flavor create --id 2 --vcpus 1 --ram 512 --disk 10 1C0.5G10G
 
 openstack flavor create --id 1 --vcpus 1 --ram 2048 --disk 10 m1.small
 
 openstack flavor create --id 4 --vcpus 4 --ram 8192 --disk 10 --ephemeral 10 m2.large
 
 # 安全组
 openstack security group create secgroup
 
 # 创建虚拟机
 openstack server create --flavor 1C0.5G10G --image cirros --security-group secgroup --nic net-id=29a1144f-9046-46bf-b734-ab99054ae213 --password 123 cirros
 
  openstack server create --flavor 1C0.5G10G --image cirros --security-group secgroup --nic net-id=7014e416-3b67-48f6-92be-918811689b02 --password 123 cirros
```

```
# 创建虚拟机流程

 接收请求 /opt/nova/venv/lib64/python3.9/site-packages/eventlet/wsgi.py:1037
 _process_stack /opt/nova/nova/api/openstack/wsgi.py:513
```



## 问题记录

### Keystone

- keystone-manage db_sync  AttributeError: 'NoneType' object has no attribute 'getcurrent'

```bash
(venv) [root@MiWiFi-RD03-srv keystone]# keystone-manage db_sync
2024-05-09 00:58:15.218 216354 INFO alembic.runtime.migration [-] Context impl MySQLImpl.
2024-05-09 00:58:15.220 216354 INFO alembic.runtime.migration [-] Will assume non-transactional DDL.
Exception ignored in: <function _removeHandlerRef at 0x7fa784cb88b0>
Traceback (most recent call last):
  File "/usr/lib64/python3.9/logging/__init__.py", line 831, in _removeHandlerRef
  File "/usr/lib64/python3.9/logging/__init__.py", line 225, in _acquireLock
  File "/usr/lib64/python3.9/threading.py", line 156, in acquire
  File "/opt/keystone/venv/lib64/python3.9/site-packages/eventlet/green/thread.py", line 36, in get_ident
AttributeError: 'NoneType' object has no attribute 'getcurrent'

```



问题解决

```bash
# 宿主机环境为例，虚拟环境进入相应目录
vim /opt/keystone/venv/lib64/python3.9/site-packages/eventlet/green/thread.py

def get_ident(gr=None):
    try:
        if gr is None:
            return id(greenlet.getcurrent())
        else:
            return id(gr)
    except:
        return id(gr)
    #if gr is None:
    #    return id(greenlet.getcurrent())
    #else:
    #    return id(gr)
```

