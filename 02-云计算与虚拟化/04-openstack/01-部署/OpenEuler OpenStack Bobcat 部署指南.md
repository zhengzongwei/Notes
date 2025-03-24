# OpenStack Bobcat 部署指南

本文档是基于 openEuler 24.03 LTS SP1的OpenStack部署指南

## 基础信息

### 硬件信息

- CPU 4C
- 内存 8G
- 磁盘 
  - 系统盘 100G
  - 数据盘 200G
- 网络
  - enp0s5
  - enp0s6

### 软件信息

- 内核 `6.6.0-72.0.0.76.oe2403sp1.aarch64`
- libvirt `libvirt-9.10.0-14.oe2403sp1.aarch64`
- qemu `qemu-8.2.0-27.oe2403sp1.aarch64`

## 部署

- 变量

  ```shell
  HOSTNAME=controller-1
  IPADDR=10.211.55.82
  RABBITMQ_SERVER_OPENSTACK_PASSWD=openstack
  REPO_URL=https://opendev.org/openstack
  BRANCH_VERSION="2023.2"
  ADMIN_PASS=admin
  KEYSTONE_PASS=keystone
  GLANCE_PASS=glance
  NOVA_PASS=nova
  PLACEMENT_PASS=placement
  NEUTRON_PASS=neutron
  CINDER_PASS=cinder
  OCTAVIA_PASS=octavia
  ```
  

### 系统配置

#### 1. 修改主机名

```
hostnamectl set-hostname $HOSTNAME


sed -i "$a\10.211.55.82 $HOSTNAME" /etc/hosts
```

#### 2. 时钟同步

集群环境时刻要求每个节点时间一致，一般由时钟同步软件保证

- Controller 节点

  1. 安装服务

     ```shell
     dnf install chrony
     ```

  2. 修改`/etc/chrony.conf`,新增一行

     ```shell
     # 表示允许哪些IP从本节点同步时钟
     allow 192.168.0.0/24
     
     sed -i '/^allow 192.168.0.0\/24/d; $a\allow 192.168.0.0/24' /etc/chrony.conf
     ```

  3. 开启自启动并启动服务

     ```shell
     systemctl enable --now chronyd
     ```

- 其他节点

  1. 安装服务

     ```shell
     dnf install chrony
     ```

  2. 修改`/etc/chrony.conf`,新增一行

     注释 `pool pool.ntp.org iburst`表示不从公网同步时钟。

     ```shell
     # NTP_SERVER是controller IP，表示从这个机器获取时间，这里我们填192.168.0.2，或者在`/etc/hosts`里配置好的controller名字即可。
     server NTP_SERVER iburst
     ```

  3. 开启自启动并启动服务

     ```shell
     systemctl ensble --now chronyd
     ```

  4. 验证

     ```shell
     chronyc sources
     
     MS Name/IP address         Stratum Poll Reach LastRx Last sample
     ===============================================================================
     ^* 192.168.0.2                 4   6     7     0  -1406ns[  +55us] +/-   16ms
     ```

#### 3.  Selinux 配置

1. 关闭SELinux

   ```shell
   setenforce 0
   ```

2. 持久化关闭Selinux

   ```shell
   sed -i 's/SELINUX=enfircing/SELINUX=disabled/g' /etc/selinux/config
   ```

#### 4. 防火墙

1. 关闭防火墙和自启动

   ```shell
   systemctl disable --now firewalld
   ```

#### 5. pip 源配置

```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 6. 依赖包安装

```shell
dnf install gcc python3-devel python3-unversioned-command git 
```

### 中间件

#### memcache

1. 安装软件包

   ```shell
   dnf install memcached
   ```

2. 修改配置文件

   ```shell
   sed -i "s/::1/&,$HOSTNAME/" /etc/sysconfig/memcached
   ```

3. 启动服务

   ```shell
   systemctl enable --now memcached
   ```

#### rabbitmq-server

1. 安装软件包

   ```shell
   dnf install rabbitmq-server
   ```

2. 启动服务

   ```shell
   systemctl enable --now rabbitmq-server
   ```

3. 配置openstack用户

   ```shell
   rabbitmqctl add_user openstack $RABBITMQ_SERVER_OPENSTACK_PASSWD
   rabbitmqctl set_permissions openstack ".*" ".*" ".*"
   ```

#### Mariadb

1. 安装软件包

   ```shell
   dnf install mariadb mariadb-server python3-PyMySQL
   ```

2. 配置文件新增

   ```shell
   cat <<EOF | sudo tee /etc/my.cnf.d/openstack.cnf > /dev/null
   [mysqld]
   bind-address = $IPADDR
   default-storage-engine = innodb
   innodb_file_per_table = on
   max_connections = 4096
   collation-server = utf8_general_ci
   character-set-server = utf8
   EOF
   ```

3. 启动服务

   ```shell
   systemctl enable --now mariadb
   ```

4. 初始化数据库

   ```shell
   mysql_secure_installation
   ```

   - 示例如下

     ```shell
     NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
         SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!
     
     In order to log into MariaDB to secure it, we'll need the current
     password for the root user. If you've just installed MariaDB, and
     haven't set the root password yet, you should just press enter here.
     
     Enter current password for root (enter for none): 
     
     #这里输入密码，由于我们是初始化DB，直接回车就行
     
     OK, successfully used password, moving on...
     
     Setting the root password or using the unix_socket ensures that nobody
     can log into the MariaDB root user without the proper authorisation.
     
     You already have your root account protected, so you can safely answer 'n'.
     
     # 这里根据提示输入N
     
     Switch to unix_socket authentication [Y/n] N
     
     Enabled successfully!
     Reloading privilege tables..
     ... Success!
     
     
     You already have your root account protected, so you can safely answer 'n'.
     
     # 输入Y，修改密码
     
     Change the root password? [Y/n] Y
     
     New password: 
     Re-enter new password: 
     Password updated successfully!
     Reloading privilege tables..
     ... Success!
     
     
     By default, a MariaDB installation has an anonymous user, allowing anyone
     to log into MariaDB without having to have a user account created for
     them.  This is intended only for testing, and to make the installation
     go a bit smoother.  You should remove them before moving into a
     production environment.
     
     # 输入Y，删除匿名用户
     
     Remove anonymous users? [Y/n] Y
     ... Success!
     
     Normally, root should only be allowed to connect from 'localhost'.  This
     ensures that someone cannot guess at the root password from the network.
     
     # 输入Y，关闭root远程登录权限
     
     Disallow root login remotely? [Y/n] Y
     ... Success!
     
     By default, MariaDB comes with a database named 'test' that anyone can
     access.  This is also intended only for testing, and should be removed
     before moving into a production environment.
     
     # 输入Y，删除test数据库
     
     Remove test database and access to it? [Y/n] Y
     - Dropping test database...
     ... Success!
     - Removing privileges on test database...
     ... Success!
     
     Reloading the privilege tables will ensure that all changes made so far
     will take effect immediately.
     
     # 输入Y，重载配置
     
     Reload privilege tables now? [Y/n] Y
     ... Success!
     
     Cleaning up...
     
     All done!  If you've completed all of the above steps, your MariaDB
     installation should now be secure.
     ```

### OpenStack服务

#### openstackclient

- 创建环境

  1. 创建openstackclient目录

     ```shell
     mkdir /opt/openstackclient
     ```

  2. 创建虚环境

     ```shell
     python -m venv /opt/openstackclient/venv
     ```

  3. 激活虚环境

     ```shell
     source /opt/openstackclient/venv/bin/activate
     ```

  4. 安装openstackclient

     ```shell
     pip install openstackclient
     ```

  5. 将openstack命令移动到 /usr/bin/

     ```shell
     cp /opt/openstackclient/venv/bin/openstack* /usr/bin/
     ```

#### keystone

- 依赖包安装

  ```shell
  dnf install httpd mod_wsgi
  ```

- 创建keystone用户

  ```shell
  getent group keystone >/dev/null || groupadd -r keystone 
  if ! getent passwd keystone >/dev/null; then
    useradd -r -g keystone -G keystone,nobody -d /var/lib/keystone -s /sbin/nologin -c "OpenStack Keystone Daemons" keystone
  fi
  ```

- 文件夹配置

  1. 创建文件夹

     ```shell
     mkdir -p /etc/keystone/ /var/lib/keystone /var/log/keystone
     ```

  2. 赋予相关权限

     ```shell
     chown -R keystone:keystone /etc/keystone/ /var/lib/keystone /var/log/keystone
     ```

  3. 日志配置

     ```shell
     tee /etc/logrotate.d/nova > /dev/null <<EOF
     /var/log/keystone/*.log {
         weekly
         dateext
         rotate 10
         size 1M
         missingok
         compress
         notifempty
         su nova nova
         minsize 100k
     }
     EOF
     ```

- 源代码拉取

  1. 拉取keystone代码

     ```shell
     git clone $REPO_URL/keystone.git /opt/keystone && git config --global --add safe.directory 
     ```

  2. 切换分支

     ```shell
     cd /opt/keystone && git checkout -b stable/$BRANCH_VERSION remotes/origin/stable/$BRANCH_VERSION
     ```

- 虚环境创建

  1. 创建目录

     ```shell
     python -m venv /opt/keystone/venv
     ```

  2. 激活虚环境

     ```shell
     source /opt/keystone/venv/bin/activate
     ```

  3. 安装依赖包

     ```shell
     pip install -r requirements.txt && python /opt/keystone/setup.py install && pip install python-memcached pymysql SQLAlchemy==1.4.52
     ```

- 配置文件

  ```shell
  tee /etc/keystone/keystone.conf > /dev/null <<EOF
  [database]
  connection = mysql+pymysql://keystone:$KEYSTONE_PASS@$HOSTNAME/keystone
  
  [token]
  allow_rescope_scoped_token = True
  provider = fernet
  expiration = 7200
  EOF
  
  chown -R keystone:keystone /etc/keystone/ 
  ```

- 数据库配置

  1. 创建数据库用户和表

     ```shell
     mysql -e "\
         CREATE DATABASE keystone; \
         GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY '$KEYSTONE_PASS'; \
         GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY '$KEYSTONE_PASS';"
     ```

  2. 同步数据库表结构

     ```shell
     keystone-manage db_sync 
     
     # 确认表是否同步
     mysql -e "use keystone;show tables;"
     ```

  3. 初始化Fernet密钥

     ```shell
     keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone && \
     keystone-manage credential_setup --keystone-user keystone --keystone-group keystone
     ```

- 初始化keystone

  ```shell
  keystone-manage bootstrap --bootstrap-password $ADMIN_PASS \
  --bootstrap-admin-url http://$HOSTNAME:5000/v3/ \
  --bootstrap-internal-url http://$HOSTNAME:5000/v3/ \
  --bootstrap-public-url http://$HOSTNAME:5000/v3/ \
  --bootstrap-region-id RegionOne
  ```

- httpd配置

  1. /etc/httpd/conf.d/wsgi-keystone.conf

     ```shell
     tee /etc/httpd/conf.d/wsgi-keystone.conf > /dev/null <<EOF
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
         ErrorLog /var/log/keystone/keystone_error.log
         CustomLog /var/log/keystone/keystone_access.log combined
     
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
     
     EOF
     ```

     

  2. httpd.conf

     ```shell
     sed -i "s/#ServerName www.example.com:80/ServerName $HOSTNAME/g" /etc/httpd/conf/httpd.conf
     
     # 验证是否已修改
     cat /etc/httpd/conf/httpd.conf | grep ServerName
     ```

     

- 验证

  1. 环境变量创建

     ```shell
     tee /root/.admin-openrc > /dev/null <<EOF
     export OS_PROJECT_DOMAIN_NAME=Default
     export OS_USER_DOMAIN_NAME=Default
     export OS_PROJECT_NAME=admin
     export OS_USERNAME=admin
     export OS_PASSWORD=$ADMIN_PASS
     export OS_AUTH_URL=http://$HOSTNAME:5000/v3
     export OS_IDENTITY_API_VERSION=3
     export OS_IMAGE_API_VERSION=2
     EOF
     ```

  2. 创建项目、用户、service

     ```shell
     source ~/.admin-openrc && openstack domain create --description "An Example Domain" example && \
         openstack project create --domain default --description "Service Project" service && \
         openstack project create --domain default --description "Demo Project" demo-project && \
         openstack user create --domain default --password "demo" demo && \
         openstack role create demo && \
         openstack role add --project demo-project --user demo demo
     ```

  3. 验证

     ```shell
     openstack --os-auth-url http://$HOSTNAME:5000/v3 \
         --os-project-domain-name Default --os-user-domain-name Default \
         --os-project-name admin --os-username admin token issue
     ```

#### placement

- 创建placement用户

  ```shell
  getent group placement >/dev/null || groupadd -r placement 
  if ! getent passwd placement >/dev/null; then
    useradd -r -g placement -G placement,nobody -d /var/lib/placement -s /sbin/nologin -c "OpenStack Placement Daemons" placement
  fi
  ```

- 源代码拉取

  1. 拉取placement代码

     ```shell
     git clone $REPO_URL/placement.git /opt/placement && git config --global --add safe.directory /opt/placement
     ```

  2. 切换分支

     ```shell
     cd /opt/placement && git checkout -b stable/$BRANCH_VERSION remotes/origin/stable/$BRANCH_VERSION
     ```

- 文件夹配置

  1. 创建文件夹

     ```shell
     mkdir -p /var/log/placement/ /etc/placement/ 
     ```

  2. 文件夹授权

     ```shell
     chown -R placement:placement /var/log/placement/ /etc/placement/ /opt/placement/
     ```

  3. 日志配置

     ```shell
     tee /etc/logrotate.d/placement > /dev/null <<EOF
     /var/log/placement/*.log {
         weekly
         dateext
         rotate 10
         size 1M
         missingok
         compress
         notifempty
         su placement placement
         minsize 100k
     }
     
     EOF
     ```

- 虚环境创建

  1. 创建目录

     ```shell
     python -m venv /opt/placement/venv
     ```

  2. 激活虚环境

     ```shell
     source /opt/placement/venv/bin/activate
     ```

  3. 安装依赖包

     SQLAlchemy 默认安装的版本是 2.0.39,代码不兼容2.0版本

     ```shell
     pip install -r requirements.txt && python /opt/placement/setup.py install && pip install python-memcached pymysql SQLAlchemy==1.4.52
     ```

  4. 移动执行文件到指定目录

     ```shell
     cp /opt/placement/venv/bin/placement-* /usr/bin/
     ```

- 配置文件

  1. /etc/placement/placement.conf

     ```shell
     tee /etc/placement/placement.conf > /dev/null <<EOF
     [placement_database]
     connection = mysql+pymysql://placement:$PLACEMENT_PASS@${HOSTNAME}/placement
     [api]
     auth_strategy = keystone
     [keystone_authtoken]
     auth_url = http://${HOSTNAME}:5000/v3
     memcached_servers = ${HOSTNAME}:11211
     auth_type = password
     project_domain_name = Default
     user_domain_name = Default
     project_name = service
     username = placement
     password = $PLACEMENT_PASS
     
     EOF
     ```

  2. /etc/httpd/conf.d/00-placement-api.conf

     ```shell
     tee /etc/httpd/conf.d/00-placement-api.conf > /dev/null <<EOF
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
       <Directory /opt/placement/venv/bin>
         <IfVersion >= 2.4>
           Require all granted
         </IfVersion>
         <IfVersion < 2.4>
           Order allow,deny
           Allow from all
         </IfVersion>
       </Directory>
     </VirtualHost>
     
     Alias /placement-api /opt/placement/venv/bin/placement-api
     <Location /placement-api>
       SetHandler wsgi-script
       Options +ExecCGI
       WSGIProcessGroup placement-api
       WSGIApplicationGroup %{GLOBAL}
       WSGIPassAuthorization On
     </Location>
     
     EOF
     ```

- 数据库配置

  1. 数据表创建

     ```shell
     mysql -e "\
         CREATE DATABASE placement; \
         GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'localhost' IDENTIFIED BY '$PLACEMENT_PASS'; \
         GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'%' IDENTIFIED BY '$PLACEMENT_PASS';"
     ```

  2. 数据库同步

     ```shell
     su -s /bin/sh -c "placement-manage db sync" placement
     ```

- 创建placement服务

  ```shell
  source ~/.admin-openrc && openstack user create --domain default --password "$PLACEMENT_PASS" placement \
      && openstack role add --project service --user placement admin \
      && openstack service create --name placement --description "Placement API" placement \
      && openstack endpoint create --region RegionOne placement public http://${HOSTNAME}:8778 \
      && openstack endpoint create --region RegionOne placement internal http://${HOSTNAME}:8778 \
      && openstack endpoint create --region RegionOne placement admin http://${HOSTNAME}:8778
  ```

  

- 验证

  ```shell
  # 重启httpd
  systemctl restart httpd
  
  curl http://${HOSTNAME}:8778
  placement-status upgrade check
  ```

#### glance

- 创建glance用户

  ```shell
  getent group glance >/dev/null || groupadd -r glance
  if ! getent passwd glance >/dev/null; then
    useradd -r -g glance -G glance,nobody -d /var/lib/glance -s /sbin/nologin -c "OpenStack Glance Daemons" glance
  fi
  ```

- 源代码拉取

  1. 拉取glance代码

     ```shell
     git clone $REPO_URL/glance.git /opt/glance && git config --global --add safe.directory /opt/glance
     ```

  2. 切换分支

     ```shell
     cd /opt/glance && git checkout -b stable/$BRANCH_VERSION remotes/origin/stable/$BRANCH_VERSION
     ```

- 文件夹配置

  1. 创建文件夹

     ```shell
     mkdir -p /var/lib/glance/ /var/log/glance /etc/glance  /var/lib/glance/images/
     ```

  2. 授权文件夹

     ```shell
     chown -R glance:glance /etc/glance/ /var/log/glance/ /var/lib/glance/ /opt/glance/ /var/lib/glance/images/
     ```

- 虚环境创建

  1. 创建目录

     ```shell
     python -m venv /opt/glance/venv
     ```

  2. 激活虚环境

     ```shell
     source /opt/glance/venv/bin/activate
     ```

  3. 安装依赖

     ```shell
     pip install -r requirements.txt && python /opt/glance/setup.py install && pip install python-memcached pymysql SQLAlchemy==1.4.52 oslo.policy==4.3.0
     ```

  4. 移动执行文件到`/usr/bin`目录

     ```shell
     cp /opt/glance/venv/bin/glance-* /usr/bin/
     ```

- 配置文件

  - /etc/glance/glance-api.conf

    ```shell
    tee /etc/glance/glance-api.conf > /dev/null <<EOF
    [DEFAULT]
    # 日志文件路径，如果不想记录到文件，可以不设置此选项
    log_file = /var/log/glance/api.log
    
    [database]
    connection = mysql+pymysql://glance:$GLANCE_PASS@${HOSTNAME}/glance
    
    [keystone_authtoken]
    www_authenticate_uri  = http://${HOSTNAME}:5000
    auth_url = http://${HOSTNAME}:5000
    memcached_servers = ${HOSTNAME}:11211
    auth_type = password
    project_domain_name = Default
    user_domain_name = Default
    project_name = service
    username = glance
    password = $GLANCE_PASS
    
    [paste_deploy]
    flavor = keystone
    
    [glance_store]
    stores = file,http
    default_store = file
    filesystem_store_datadir = /var/lib/glance/images/
    
    EOF
    ```

  - glance-api-paste.ini

    ```shell
    cp /opt/glance/etc/glance-api-paste.ini /etc/glance/
    
    cp /etc/glance/glance-api.conf.sample /etc/glance/glance-api.conf
    cp /etc/glance/glance-registry.conf.sample /etc/glance/glance-registry.conf
    ```

- 数据库配置

  - 创建数据库表

    ```shell
    mysql -e "\
        CREATE DATABASE glance; \
        GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' IDENTIFIED BY '$GLANCE_PASS'; \
        GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY '$GLANCE_PASS';"
    ```

  - 数据库同步

    ```shell
    su -s /bin/sh -c "glance-manage db_sync" glance
    ```

- 服务初始化

  - 服务凭证

    ```shell
    openstack user create --domain default --password "$GLANCE_PASS" glance && \
    openstack role add --project service --user glance admin && \
    openstack service create --name glance --description "OpenStack Image" image
    ```

  - endpoint

    ```shell
    openstack endpoint create --region RegionOne image public http://${HOSTNAME}:9292 && \
    openstack endpoint create --region RegionOne image internal http://${HOSTNAME}:9292 && \
    openstack endpoint create --region RegionOne image admin http://${HOSTNAME}:9292
    ```

- 服务配置

  - 日志配置

    ```shell
    tee /etc/logrotate.d/glance > /dev/null <<EOF
    /var/log/glance/*.log {
        weekly
        dateext
        rotate 10
        size 1M
        missingok
        compress
        notifempty
        su glance glance
        minsize 100k
    }
    
    EOF
    ```

  - 服务配置

    ```shell
    tee /usr/lib/systemd/system/openstack-glance-api.service > /dev/null <<EOF
    [Unit]
    Description=OpenStack Image Service API server
    After=syslog.target network.target
    After=mariadb.service postgresql.service rabbitmq-server.service
    
    [Service]
    Type=simple
    User=glance
    Group=glance
    LimitNOFILE=131072
    LimitNPROC=131072
    WorkingDirectory=/var/lib/glance
    PrivateTmp=yes
    # the connection parameter might be stored in the glance-api related config files
    ExecStartPre=-/usr/bin/glance-manage db sync
    ExecStart=/usr/bin/glance-api
    
    [Install]
    WantedBy=multi-user.target
    EOF
    
  ln -s /usr/lib/systemd/system/openstack-glance-api.service /etc/systemd/system/openstack-glance-api.service
    ```

  - 服务启动
  
    ```shell
    systemctl enable --now openstack-glance-api.service
    ```

- 验证

  - 下载测试镜像，传入测试环境

    - x86_64

      [openEuler-24.03-LTS-SP1-x86_64.qcow2.xz](https://mirrors.jcut.edu.cn/openeuler/openEuler-24.03-LTS-SP1/virtual_machine_img/x86_64/openEuler-24.03-LTS-SP1-x86_64.qcow2.xz)

    - aarch64

      [openEuler-24.03-LTS-SP1-aarch64.qcow2.xz](https://mirrors.jcut.edu.cn/openeuler/openEuler-24.03-LTS-SP1/virtual_machine_img/aarch64/openEuler-24.03-LTS-SP1-aarch64.qcow2.xz)

    - riscv64

      [openEuler-24.03-LTS-SP1-riscv64.qcow2.xz](https://mirrors.jcut.edu.cn/openeuler/openEuler-24.03-LTS-SP1/virtual_machine_img/riscv64/openEuler-24.03-LTS-SP1-riscv64.qcow2.xz)

    - loongarch64

      [openEuler-24.03-LTS-SP1-loongarch64.qcow2.xz](https://mirrors.jcut.edu.cn/openeuler/openEuler-24.03-LTS-SP1/virtual_machine_img/loongarch64/openEuler-24.03-LTS-SP1-loongarch64.qcow2.xz)

  - 上传镜像

    ```shell
    cd /opt/ && source /root/.admin-openrc && 
    
    # hw_qemu_guest_agent=yes 更改密码 需要设置的参数
    openstack image create --progress --disk-format qcow2 --container-format bare --file openEuler-22.03-LTS-SP4-aarch64.qcow2  --property hw_qemu_guest_agent=yes  --public --property os_type='linux' --property os_variant='openEuler-2203' openEuler-22.03-LTS-SP4 
    ```


#### nova

- 依赖组件安装

  - edk2

    ```shell
    # aarch64
    dnf install edk2-aarch64
    ```

  - libguestfs

    ```shell
    dnf install libguestfs python3-libguestfs
    
    cp -r /usr/lib64/python3.9/site-packages/guestfs.py /opt/nova/venv/lib/python3.9/site-packages/
    cp /usr/lib64/python3.9/site-packages/libguestfsmod.cpython-39-aarch64-linux-gnu.so /opt/nova/venv/lib/python3.9/site-packages/
    ```

  - novnc

    ```shell
    dnf install novnc
    ```

  - qemu/libvirt

    bobcat nova 要求的nova版本为7.0 在openeuler-2203 系统中 qemu版本为6.2.0，不满足要求。当前更改代码让其兼容，不保证无其他问题

    ```shell
    # 安装qemu
    dnf install qemu*
    
    dnf install libvirt
    
    usermod -aG libvirt nova
    
    
    systemctl start libvirtd
    
    ```

    - python3-libvirt

      ```shell
      dnf install python3-libvirt
      
      cp -r /usr/lib64/python3.11/site-packages/libvirt* /opt/nova/venv/lib64/python3.11/site-packages/
      ```

      

    - ARM 架构 qemu设置

      - /etc/libvirt/qemu.conf

        ```shell
        nvram = [
                "/usr/share/AAVMF/AAVMF_CODE.fd:/usr/share/AAVMF/AAVMF_VARS.fd",
                "/usr/share/edk2/aarch64/QEMU_EFI-pflash.raw:/usr/share/edk2/aarch64/vars-template-pflash.raw"
        ]
        ```

      - /etc/qemu/firmware/edk2-aarch64.json

        ```shell
        mkdir -p /etc/qemu/firmware/
        
        tee /etc/qemu/firmware/edk2-aarch64.json > /dev/null <<EOF
        {
            "description": "UEFI firmware for ARM64 virtual machines",
            "interface-types": [
                "uefi"
            ],
            "mapping": {
                "device": "flash",
                "executable": {
                    "filename": "/usr/share/edk2/aarch64/QEMU_EFI-pflash.raw",
                    "format": "raw"
                },
                "nvram-template": {
                    "filename": "/usr/share/edk2/aarch64/vars-template-pflash.raw",
                    "format": "raw"
                }
            },
            "targets": [
                {
                    "architecture": "aarch64",
                    "machines": [
                        "virt-*"
                    ]
                }
            ],
            "features": [
        
            ],
            "tags": [
        
            ]
        }
        
        EOF
        ```

- 创建nova用户

  ```shell
  getent group nova >/dev/null || groupadd -r nova 
  if ! getent passwd nova >/dev/null; then
    useradd -r -g nova -G nova,nobody -d /var/lib/nova -s /sbin/nologin -c "OpenStack Nova Daemons" nova
  fi
  ```

- 源代码拉取

  1. 拉取nova代码

     ```
     git clone $REPO_URL/nova.git /opt/nova && git config --global --add safe.directory /opt/nova
     ```

  2. 切换分支

     ```shell
     cd /opt/nova && git checkout -b stable/$BRANCH_VERSION remotes/origin/stable/$BRANCH_VERSION
     ```

- 文件夹配置

  1. 创建文件夹

     ```shell
     mkdir -p /var/log/nova/ /etc/nova/ /var/lib/nova /var/lib/nova/instances/locks
     ```

  2. 文件夹授权

     ```shell
     chown -R nova:nova /var/log/nova/ /etc/nova/ /opt/nova/ /var/lib/nova /var/lib/nova/instances/
     ```

- 虚环境创建

  1. 创建目录

     ```shell
     python -m venv /opt/nova/venv
     ```

  2. 激活虚环境

     ```shell
     source /opt/nova/venv/bin/activate
     ```

  3. 依赖安装

     ```shell
     pip install -r requirements.txt && python /opt/nova/setup.py install && pip install python-memcached pymysql SQLAlchemy==1.4.52
     ```

  4. 移动执行文件到指定目录

     ```shell
     cp /opt/nova/venv/bin/nova-* /usr/bin/
     ```

- 配置文件

  1. 日志配置

     ```shell
     tee /etc/logrotate.d/nova > /dev/null <<EOF
     /var/log/nova/*.log {
         rotate 14
         size 10M
         missingok
         compress
         copytruncate
     }
     
     EOF
     ```

  2. 配置文件

     - 基础配置文件

       ```shell
       cp -r\
           /opt/nova/etc/nova/api-paste.ini \
           /opt/nova/etc/nova/rootwrap.conf \
           /opt/nova/etc/nova/rootwrap.d  \
           /etc/nova/
       ```

     - /etc/nova/nova.conf

       ```shell
       tee /etc/nova/nova.conf > /dev/null <<EOF
       [DEFAULT]
       osapi_compute_workers = 4
       # ec2_workers = 4
       metadata_workers = 4
       enabled_apis = osapi_compute,metadata
       transport_url = rabbit://openstack:$RABBITMQ_SERVER_OPENSTACK_PASSWD@$HOSTNAME:5672/
       my_ip = $IPADDR
       use_neutron = true
       firewall_driver = nova.virt.firewall.NoopFirewallDriver
       compute_driver=libvirt.LibvirtDriver
       allow_resize_to_same_host=True
       instances_path = /var/lib/nova/instances/
       lock_path = /var/lib/nova/tmp
       log_dir = /var/log/nova/
       verbose=debug
       debug = True
       
       rpc_response_timeout = 180
       
       # Quota
       [quota]
       instances = 100
       cores=51200
       ram=102400
       
       [api_database]
       connection = mysql+pymysql://nova:nova@$HOSTNAME/nova_api
       
       [database]
       connection = mysql+pymysql://nova:nova@$HOSTNAME/nova
       
       [scheduler]
       workers = 4
       
       [conductor]
       workers = 4
       
       [api]
       workers = 4
       auth_strategy = keystone
       
       [keystone_authtoken]
       www_authenticate_uri = http://$HOSTNAME:5000/
       auth_url = http://$HOSTNAME:5000/
       memcached_servers = $HOSTNAME:11211
       auth_type = password
       project_domain_name = Default
       user_domain_name = Default
       project_name = service
       username = nova
       password = $NOVA_PASS
       
       [vnc]
       enabled = true
       server_listen = 0.0.0.0
       server_proxyclient_address = \$my_ip
       novncproxy_base_url = http://$HOSTNAME:6080/vnc_auto.html
       
       [libvirt]
       virt_type = qemu
       cpu_mode = custom
       cpu_model = cortex-a72
       num_pcie_ports=10
       inject_password = True
       inject_key = True
       
       [glance]
       api_servers = http://$HOSTNAME:9292
       
       [oslo_concurrency]
       lock_path = /var/lib/nova/tmp
       
       [placement]
       region_name = RegionOne
       project_domain_name = Default
       project_name = service
       auth_type = password
       user_domain_name = Default
       auth_url = http://$HOSTNAME:5000/v3
       username = placement
       password = $PLACEMENT_PASS
       
       [neutron]
       auth_url = http://$HOSTNAME:5000
       auth_type = password
       project_domain_name = default
       user_domain_name = default
       region_name = RegionOne
       project_name = service
       username = neutron
       password = $NEUTRON_PASS
       service_metadata_proxy = true
       metadata_proxy_shared_secret = METADATA_SECRET
       
       [privsep_osbrick]
       user = nova
       helper_command = sudo /opt/nova/venv/bin/privsep-helper
       
       [notifications]
       notify_on_state_change = vm_and_task_state
       
       [oslo_messaging_notifications]
       driver = messaging
       
       EOF
       ```

     - /etc/nova/rootwrap.d/compute.filters

       ```shell
       tee /etc/nova/rootwrap.d/compute.filters > /dev/null <<EOF
       
       # nova-rootwrap command filters for compute nodes
       # This file should be owned by (and only-writeable by) the root user
       
       [Filters]
       privsep-helper: CommandFilter, /opt/nova/venv/bin/privsep-helper, root
       # os_brick.privileged.default oslo.privsep context
       privsep-rootwrap-os_brick: RegExpFilter, privsep-helper, root, privsep-helper, --config-file, /etc/(?!\.\.).*, --privsep_context, os_brick.privileged.default, --privsep_sock_path, /tmp/.*
       
       # nova.privsep.sys_admin_pctxt oslo.privsep context
       privsep-rootwrap-sys_admin: RegExpFilter, privsep-helper, root, privsep-helper, --config-file, /etc/(?!\.\.).*, --privsep_context, nova.privsep.sys_admin_pctxt, --privsep_sock_path, /tmp/.*
       EOF
       ```

- 数据库配置

  1. 数据表

     ```shell
      mysql -e "\
         CREATE DATABASE nova_api; \
         CREATE DATABASE nova; \
         CREATE DATABASE nova_cell0; \
         GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' IDENTIFIED BY '$NOVA_PASS'; \
         GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY '$NOVA_PASS'; \
         GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' IDENTIFIED BY '$NOVA_PASS'; \
         GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY '$NOVA_PASS'; \
         GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' IDENTIFIED BY '$NOVA_PASS'; \
         GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' IDENTIFIED BY '$NOVA_PASS';"
     ```

  2. 同步表结构

     ```shell
     su -s /bin/sh -c "nova-manage api_db sync" nova && \
         su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova && \
         su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova && \
         su -s /bin/sh -c "nova-manage db sync" nova && \
         su -s /bin/sh -c "nova-manage cell_v2 list_cells" nova && \
         su -s /bin/sh -c "nova-manage cell_v2 discover_hosts --verbose" nova
     ```

  3. 计算节点加入cell中

     每次新增计算节点需要执行此命令

     ```shell
     su -s /bin/sh -c "nova-manage cell_v2 discover_hosts --verbose" nova
     ```

     

- 服务端点

  ```shell
  source ~/.admin-openrc && openstack user create --domain default --password "$NOVA_PASS" nova \
      && openstack role add --project service --user nova admin \
      && openstack service create --name nova --description "OpenStack Compute" compute \
      && openstack endpoint create --region RegionOne compute public http://$HOSTNAME:8774/v2.1 \
      && openstack endpoint create --region RegionOne compute internal http://$HOSTNAME:8774/v2.1 \
      && openstack endpoint create --region RegionOne compute admin http://$HOSTNAME:8774/v2.1
  ```

- 服务配置

  - sudoer

    ```shell
    tee /etc/sudoers.d/nova > /dev/null <<EOF
    Defaults:nova !requiretty
    
    nova ALL = (root) NOPASSWD: /usr/bin/nova-rootwrap /etc/nova/rootwrap.conf *
    nova ALL = (root) NOPASSWD: /usr/bin/privsep-helper *
    EOF
    ```

  - 服务配置

    1. 控制节点服务
       - openstack-nova-api
       - opentack-nova-conductor
       - openstack-nova-scheduler
       - openstack-nova-novncproxy
    2. 计算节点服务
       - openstack-nova-compute

    - openstack-nova-api

      ```shell
      tee /usr/lib/systemd/system/openstack-nova-api.service > /dev/null <<EOF
      [Unit]
      Description=OpenStack Nova API Server
      After=syslog.target network.target
      
      [Service]
      Type=notify
      NotifyAccess=all
      TimeoutStartSec=0
      Restart=always
      User=nova
      ExecStart=/usr/bin/nova-api
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/openstack-nova-api.service /etc/systemd/system/openstack-nova-api.service
      ```

    - openstack-nova-conductor

      ```shell
      tee /usr/lib/systemd/system/openstack-nova-conductor.service > /dev/null <<EOF
      [Unit]
      Description=OpenStack Nova Conductor Server
      After=syslog.target network.target
      
      [Service]
      Type=notify
      NotifyAccess=all
      TimeoutStartSec=0
      Restart=always
      User=nova
      ExecStart=/usr/bin/nova-conductor
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/openstack-nova-conductor.service /etc/systemd/system/openstack-nova-conductor.service
      ```

      

    - openstack-nova-scheduler

      ```shell
      tee /usr/lib/systemd/system/openstack-nova-scheduler.service > /dev/null <<EOF
      [Unit]
      Description=OpenStack Nova Scheduler Server
      After=syslog.target network.target
      
      [Service]
      Type=notify
      NotifyAccess=all
      TimeoutStartSec=0
      Restart=always
      User=nova
      ExecStart=/usr/bin/nova-scheduler
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/openstack-nova-scheduler.service /etc/systemd/system/openstack-nova-scheduler.service
      ```

      

    - openstack-nova-novncproxy

      ```shell
      tee /usr/lib/systemd/system/openstack-nova-novncproxy.service > /dev/null <<EOF
      [Unit]
      Description=OpenStack Nova NoVNC Proxy Server
      After=syslog.target network.target
      
      [Service]
      Type=simple
      User=nova
      EnvironmentFile=-/etc/sysconfig/openstack-nova-novncproxy
      ExecStart=/usr/bin/nova-novncproxy --web /usr/share/novnc/ $OPTIONS
      Restart=on-failure
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/openstack-nova-novncproxy.service /etc/systemd/system/openstack-nova-novncproxy.service
      ```

    - openstack-nova-compute

      ```shell
      tee /usr/lib/systemd/system/openstack-nova-compute.service > /dev/null <<EOF
      [Unit]
      Description=OpenStack Nova Compute Server
      After=syslog.target network.target libvirtd.service
      
      [Service]
      Environment=LIBGUESTFS_ATTACH_METHOD=appliance
      Type=notify
      NotifyAccess=all
      TimeoutStartSec=0
      Restart=always
      User=nova
      ExecStart=/usr/bin/nova-compute
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/openstack-nova-compute.service /etc/systemd/system/openstack-nova-compute.service
      ```

  - 服务启动

    ```shell
    systemctl enable --now openstack-nova-novncproxy openstack-nova-api openstack-nova-conductor openstack-nova-scheduler openstack-nova-compute
    ```

  - flavor 配置

    ```shell
    openstack flavor create m1.tiny --id 1 --vcpus 1 --public  --ram 1024 --disk 50 --ephemeral 0 
    openstack flavor create m1.small --id 2 --vcpus 2 --public  --ram 4096 --disk 50 --ephemeral 0 
    openstack flavor create m1.medium --id 3 --vcpus 4 --public  --ram 16384 --disk 50 --ephemeral 0 
    openstack flavor create m1.large --id 4 --vcpus 8 --public  --ram 32768 --disk 50 --ephemeral 0 
    openstack flavor create m1.xlarge --id 5 --vcpus 16 --public  --ram 65536 --disk 50 --ephemeral 0 
    
    [root@controller-1 ~]# openstack  flavor list
    
    ```

- 验证

  ```shell
  # 查看服务是否启动
  openstack compute service list
  
  +--------------------------------------+----------------+--------------+----------+---------+-------+----------------------------+
  | ID                                   | Binary         | Host         | Zone     | Status  | State | Updated At                 |
  +--------------------------------------+----------------+--------------+----------+---------+-------+----------------------------+
  | a45abb26-56a3-4216-8217-bcac6efd249f | nova-conductor | controller-1 | internal | enabled | up    | 2024-08-27T03:12:30.000000 |
  | b59db6c5-4699-4bee-9203-39d3e1f57c61 | nova-scheduler | controller-1 | internal | enabled | up    | 2024-08-27T03:12:22.000000 |
  | ebf1591c-11b7-4d4f-9ff4-40c1fda10665 | nova-compute   | controller-1 | nova     | enabled | up    | 2024-08-27T03:12:27.000000 |
  +--------------------------------------+----------------+--------------+----------+---------+-------+----------------------------+
  ```

  

#### neutron

- 依赖组件安装

  - openvswitch

    ```shell
    dnf install openvswitch network-scripts
    
    systemctl enable --now openvswitch
    ```

- 系统配置

  ```shell
  cat <<EOF | sudo tee -a /etc/sysctl.conf
  
  net.bridge.bridge-nf-call-iptables = 1
  net.bridge.bridge-nf-call-ip6tables = 1
  net.bridge.bridge-nf-call-arptables = 1
  EOF
  
  modprobe br_netfilter
  
  sysctl -p
  ```

- 创建用户

  ```shell
  getent group neutron >/dev/null || groupadd -r neutron
  if ! getent passwd neutron >/dev/null; then
    useradd -r -g neutron -G neutron,nobody -d /var/lib/neutron -s /sbin/nologin -c "OpenStack Neutron Daemons" neutron
  fi
  ```

- 源代码拉取

  1. 拉取neutron代码

     ```shell
     git clone $REPO_URL/neutron.git /opt/neutron && git config --global --add safe.directory 
     ```

  2. 切换分支

     ```shell
     cd /opt/neutron && git checkout -b stable/$BRANCH_VERSION remotes/origin/stable/$BRANCH_VERSION
     ```

- 虚环境创建

  1. 创建目录

     ```shell
     python -m venv /opt/neutron/venv
     ```

  2. 激活虚环境

     ```shell
     source /opt/neutron/venv/bin/activate
     ```

  3. 安装依赖包

     ```shell
     pip install -r requirements.txt && python /opt/neutron/setup.py install && pip install python-memcached pymysql SQLAlchemy==1.4.52
     ```

  4. 移动可执行文件

     ```shell
     cp /opt/neutron/venv/bin/neutron-* /usr/bin/
     ```

- 文件夹配置

  1. 创建文件夹

     ```shell
     mkdir -p /var/lib/neutron/ /var/log/neutron /etc/neutron /etc/neutron/plugins/openvswitch/ /etc/neutron/rootwrap.d/ /etc/neutron/plugins/ml2
     ```

  2. 赋予相关权限

     ```shell
     chown -R neutron:neutron /var/lib/neutron/ /var/log/neutron /etc/neutron /opt/neutron /etc/neutron/plugins/openvswitch/ /etc/neutron/rootwrap.d/ /etc/neutron/plugins/ml2
     ```

- 网络配置

  1. 创建网桥

     ```shell
     ovs-vsctl add-br br-ex
     ovs-vsctl add-br br-int
     ovs-vsctl add-br br-tun
     
     # 删除创建的网桥
     ovs-vsctl del-br br-ex
     ovs-vsctl del-br br-int
     ovs-vsctl del-br br-tun
     
     # 手动配置IP地址
     ip addr add 10.211.55.74/24 dev br-ex
     ip link set br-ex up
     ip route add default via 10.211.55.1
     ```

  2. 绑定网卡

     该操作会断网，请谨慎操作。操作前需要知道服务器的IPMI信息

     ```shell
     #  将网卡绑定到网桥
     ovs-vsctl add-port br-ex enp0s5
     ovs-vsctl del-port br-ex enp0s5
     
     # 移除原有的IP地址
     ip addr del 10.211.55.74/24 dev enp0s5
     
     # 变更IP 地址到 br-ex
     ip addr add 10.211.55.74/24 dev br-ex
     
     # 查询当前路由
     ip route show
     
     
     # 添加默认路由
     sudo ip route add default via 10.211.55.1 dev br-ex
     # 添加路由
     sudo ip route add 10.211.55.0/24 via 10.211.55.1 dev br-ex
     
     # 删除默认路由
     sudo ip route del default
     # 删除路由
     sudo ip route del 10.211.55.0/24
     
     # 修改路由
     sudo ip route replace 10.211.55.0/24 via 10.211.55.2 dev enp0s5
     ```

  3. 网卡持久化配置

     - 创建br-ex网卡配置

       ```shell
       tee /etc/sysconfig/network-scripts/ifcfg-br-ex > /dev/null << EOF
       DEVICE=br-ex
       DEVICETYPE=ovs
       TYPE=OVSBridge
       BOOTPROTO=static
       IPADDR=10.211.55.82
       NETMASK=255.255.255.0
       GATEWAY=10.211.55.1
       DELAY=0
       DNS1=114.114.114.114
       DNS2=8.8.8.8
       ONBOOT=yes
       NM_CONTROLLED=no
       EOF
       ```

     - 修改对应绑定网卡的配置文件

       备份原有配置`cp /etc/sysconfig/network-scripts/ifcfg-enp0s5 /etc/sysconfig/network-scripts/ifcfg-enp0s5.bak`

       ```shell
       tee /etc/sysconfig/network-scripts/ifcfg-enp0s5 > /dev/null << EOF
       TYPE=OVSPort
       DEVICE=enp0s5
       ONBOOT=yes
       OVS_BRIDGE=br-ex
       NM_CONTROLLED=no
       EOF
       ```

- 配置文件

  

  1. 基础配置文件

     ```shell
     cp -r  /opt/neutron/etc/api-paste.ini /etc/neutron/
     ```

  2. /etc/neutron/rootwrap.d/rootwrap.filters

     ```shell
     tee /etc/neutron/rootwrap.d/rootwrap.filters > /dev/null << EOF
     
     # Command filters to allow privsep daemon to be started via rootwrap.
     #
     # This file should be owned by (and only-writeable by) the root user
     
     [Filters]
     
     # By installing the following, the local admin is asserting that:
     #
     # 1. The python module load path used by privsep-helper
     #    command as root (as started by sudo/rootwrap) is trusted.
     # 2. Any oslo.config files matching the --config-file
     #    arguments below are trusted.
     # 3. Users allowed to run sudo/rootwrap with this configuration(*) are
     #    also allowed to invoke python "entrypoint" functions from
     #    --privsep_context with the additional (possibly root) privileges
     #    configured for that context.
     #
     # (*) ie: the user is allowed by /etc/sudoers to run rootwrap as root
     #
     # In particular, the oslo.config and python module path must not
     # be writeable by the unprivileged user.
     
     # PRIVSEP
     # oslo.privsep default neutron context
     privsep-helper: CommandFilter, /opt/neutron/venv/bin/privsep-helper, root
     privsep: PathFilter, privsep-helper, root,
      --config-file, /etc/(?!\.\.).*,
      --privsep_context, neutron.privileged.default,
      --privsep_sock_path, /
     
     # NOTE: A second `--config-file` arg can also be added above. Since
     # many neutron components are installed like that (eg: by devstack).
     # Adjust to suit local requirements.
     
     # DEBUG
     sleep: RegExpFilter, sleep, root, sleep, \d+
     
     # EXECUTE COMMANDS IN A NAMESPACE
     ip: IpFilter, ip, root
     ip_exec: IpNetnsExecFilter, ip, root
     
     # METADATA PROXY
     haproxy: RegExpFilter, haproxy, root, haproxy, -f, .*
     haproxy_env: EnvFilter, env, root, PROCESS_TAG=, haproxy, -f, .*
     
     # DHCP
     dnsmasq: CommandFilter, dnsmasq, root
     dnsmasq_env: EnvFilter, env, root, PROCESS_TAG=, dnsmasq
     
     # DIBBLER
     dibbler-client: CommandFilter, dibbler-client, root
     dibbler-client_env: EnvFilter, env, root, PROCESS_TAG=, dibbler-client
     
     # L3
     radvd: CommandFilter, radvd, root
     radvd_env: EnvFilter, env, root, PROCESS_TAG=, radvd
     keepalived: CommandFilter, keepalived, root
     keepalived_env: EnvFilter, env, root, PROCESS_TAG=, keepalived
     keepalived_state_change: CommandFilter, neutron-keepalived-state-change, root
     keepalived_state_change_env: EnvFilter, env, root, PROCESS_TAG=, neutron-keepalived-state-change
     
     # OPEN VSWITCH
     ovs-ofctl: CommandFilter, ovs-ofctl, root
     ovsdb-client: CommandFilter, ovsdb-client, root
     
     EOF
     ```

  3. /etc/neutron/neutron.conf

     ```shell
     tee /etc/neutron/neutron.conf > /dev/null << EOF
     [DEFAULT]
     core_plugin = ml2
     #service_plugins = router
     service_plugins = router, segments, neutron.services.qos.qos_plugin.QoSPlugin, neutron.services.network_segment_range.plugin.NetworkSegmentRangePlugin
     
     allow_overlapping_ips = true
     transport_url = rabbit://openstack:$RABBITMQ_SERVER_OPENSTACK_PASSWD@${HOSTNAME}
     auth_strategy = keystone
     notify_nova_on_port_status_changes = true
     notify_nova_on_port_data_changes = true
     api_workers = 3  
     
     [database]
     connection = mysql+pymysql://neutron:$NEUTRON_PASS@${HOSTNAME}/neutron
     
     [keystone_authtoken]
     www_authenticate_uri = http://${HOSTNAME}:5000
     auth_url = http://${HOSTNAME}:5000
     memcached_servers = ${HOSTNAME}:11211
     auth_type = password
     project_domain_name = Default
     user_domain_name = Default
     project_name = service
     username = neutron
     password = $NEUTRON_PASS
     
     [nova]
     auth_url = http://${HOSTNAME}:5000
     auth_type = password
     project_domain_name = Default
     user_domain_name = Default
     region_name = RegionOne
     project_name = service
     username = nova
     password = $NOVA_PASS
     
     [privsep]
     helper_command = sudo /opt/neutron/venv/bin/privsep-helper
     
     [oslo_concurrency]
     lock_path = /var/lib/neutron/tmp
     
     [quotas]
     default_quota = -1
     quota_port = -1
     quota_router = -1
     
     [oslo_middleware]
     # 启用分页
     enable_pagination = true
     # 分页每页最大项目数
     
     EOF
     ```

  4. /etc/neutron/plugins/ml2/ml2_conf.ini

     ```shell
     tee /etc/neutron/plugins/ml2/ml2_conf.ini > /dev/null <<EOF
     [ml2]
     type_drivers = flat,vlan,vxlan
     tenant_network_types = vxlan
     mechanism_drivers = openvswitch,l2population
     extension_drivers = port_security,qos, network_segment_range
     
     [ml2_type_flat]
     flat_networks = external
     
     [ml2_type_vxlan]
     vni_ranges = 1:1000
     
     [securitygroup]
     enable_ipset = true
     firewall_driver = iptables_hybrid
     EOF
     
     tee /etc/neutron/plugins/ml2/openvswitch_agent.ini > /dev/null <<EOF
     [ovs]
     bridge_mappings = external:br-ex
     
     [securitygroup]
     firewall_driver = iptables_hybrid
     enable_security_group = true
     
     [agent]
     tunnel_types = vxlan
     l2_population = True
     EOF
     ```

     ln -s /etc/neutron/plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini

  5. /etc/neutron/l3_agent.ini

     ```shell
     tee /etc/neutron/l3_agent.ini  > /dev/null <<EOF
     [DEFAULT]
     interface_driver = openvswitch
     EOF
     ```

  6. /etc/neutron/dhcp_agent.ini

     ```shell
     tee /etc/neutron/dhcp_agent.ini  > /dev/null <<EOF
     [DEFAULT]
     interface_driver = openvswitch
     EOF
     ```

  7. /etc/neutron/metadata_agent.ini

     ```shell
     tee  /etc/neutron/metadata_agent.ini  > /dev/null <<EOF
     [DEFAULT]
     nova_metadata_host = controller-1
     metadata_proxy_shared_secret = METADATA_SECRET
     EOF
     ```

  8. /etc/neutron/plugins/openvswitch/openvswitch_agent.ini

     ```shell
     tee  /etc/neutron/plugins/openvswitch/openvswitch_agent.ini  > /dev/null <<EOF
     [ovs]
     local_ip = $IPADDR
     integration_bridge = br-int
     tunnel_bridge = br-tun
     # 物理网络和 Open vSwitch 逻辑桥接的映射
     # bridge_mappings = default:br-eth1,external:br-ex
     bridge_mappings = external:br-ex
     
     [agent]
     # Prevent ARP spoofing, can be enabled for security
     prevent_arp_spoofing = True
     tunnel_types = vxlan
     l2_population = True
     
     [securitygroup]
     # 使用 OVS 安全组
     firewall_driver = iptables_hybrid
     # firewall_driver = neutron.agent.linux.iptables_firewall.OVSHybridIptablesFirewallDriver
     
     [ml2_type_vlan]
     # 配置 VLAN 范围，取决于你希望使用的 VLAN 范围
     network_vlan_ranges = external
     
     EOF
     ```

- 数据库配置

  - 创建表

    ```shell
    mysql -e "\
        CREATE DATABASE neutron; \
        GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' IDENTIFIED BY '$NEUTRON_PASS'; \
        GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' IDENTIFIED BY '$NEUTRON_PASS';"
    ```

  - 同步表结构

    ```shell
    su -s /bin/sh -c "neutron-db-manage --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/ml2/ml2_conf.ini upgrade head" neutron
    ```

- 服务凭证

  ```shell
  source ~/.admin-openrc && openstack user create --domain default --password "$NEUTRON_PASS" neutron && openstack role add --project service --user neutron admin && \
      openstack service create --name neutron --description "OpenStack Networking" network && \
      openstack endpoint create --region RegionOne network public http://${HOSTNAME}:9696 &&  \
      openstack endpoint create --region RegionOne network internal http://${HOSTNAME}:9696 && \
      openstack endpoint create --region RegionOne network admin http://${HOSTNAME}:9696 
  ```

- 服务配置

  - sudoers

    ```shell
    tee /etc/sudoers.d/neutron > /dev/null <<EOF
    Defaults:neutron !requiretty
    
    neutron ALL = (root) NOPASSWD: /usr/bin/neutron-rootwrap /etc/neutron/rootwrap.conf *
    neutron ALL = (root) NOPASSWD: /usr/bin/neutron-rootwrap-daemon /etc/neutron/rootwrap.conf
    neutron ALL = (root) NOPASSWD: /opt/neutron/venv/bin/privsep-helper *
    neutron ALL=(ALL) NOPASSWD: /usr/sbin/ip netns exec qdhcp-*
    EOF
    ```

    

  - 日志

    ```shell
    tee /etc/logrotate.d/neutron > /dev/null <<EOF
    /var/log/neutron/*.log {
        rotate 14
        size 10M
        missingok
        compress
        copytruncate
    }
    
    EOF
    ```

  - 控制节点

    - neutron-server

      ```shell
      tee /usr/lib/systemd/system/neutron-server.service > /dev/null <<EOF
      [Unit]
      Description=OpenStack Neutron Server
      After=syslog.target network.target
      
      [Service]
      Type=notify
      User=neutron
      ExecStart=/usr/bin/neutron-server --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugin.ini --log-file /var/log/neutron/server.log
      PrivateTmp=true
      NotifyAccess=all
      KillMode=process
      Restart=on-failure
      TimeoutStartSec=0
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/neutron-server.service /etc/systemd/system/neutron-server.service
      ```

    - neutron-openvswitch-agent

      - /usr/bin/neutron-enable-bridge-firewall.sh

        ```shell
        tee /usr/bin/neutron-enable-bridge-firewall.sh > /dev/null <<EOF
        #!/bin/sh
        
        # This script is triggered on every ovs/linuxbridge agent start. Its intent is
        # to make sure the firewall for bridged traffic is enabled before we start an
        # agent that may atttempt to set firewall rules on a bridge (a common thing for
        # linuxbridge and ovs/hybrid backend setup).
        
        # before enabling the firewall, load the relevant module
        /usr/sbin/modprobe bridge
        
        # on newer kernels (3.18+), sysctl knobs are split into a separate module;
        # attempt to load it, but don't fail if it's missing (f.e. when running against
        # an older kernel version)
        /usr/sbin/modprobe br_netfilter 2>> /dev/null || :
        
        # now enable the firewall in case it's disabled (f.e. rhel 7.2 and earlier)
        for proto in ip ip6; do
            /usr/sbin/sysctl -w net.bridge.bridge-nf-call-\${proto}tables=1
        done
        EOF
        ```

        chmod +x /usr/bin/neutron-enable-bridge-firewall.sh

      ```shell
      tee /usr/lib/systemd/system/neutron-openvswitch-agent.service  > /dev/null <<EOF
      [Unit]
      Description=OpenStack Neutron Open vSwitch Agent
      After=syslog.target network.target network.service openvswitch.service
      PartOf=network.service
      Requires=openvswitch.service
      
      [Service]
      Type=simple
      User=neutron
      PermissionsStartOnly=true
      ExecStartPre=/usr/bin/neutron-enable-bridge-firewall.sh
      ExecStart=/usr/bin/neutron-openvswitch-agent --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/plugins/openvswitch/openvswitch_agent.ini --log-file /var/log/neutron/openvswitch-agent.log
      PrivateTmp=true
      KillMode=process
      Restart=on-failure
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/neutron-openvswitch-agent.service  /etc/systemd/system/neutron-openvswitch-agent.service
      ```

    - neutron-dhcp-agent.service

      ```shell
      tee /usr/lib/systemd/system/neutron-dhcp-agent.service  > /dev/null <<EOF
      [Unit]
      Description=OpenStack Neutron DHCP Agent
      After=syslog.target network.target
      
      [Service]
      Type=simple
      User=neutron
      ExecStart=/usr/bin/neutron-dhcp-agent --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/dhcp_agent.ini --log-file /var/log/neutron/dhcp-agent.log
      PrivateTmp=false
      KillMode=process
      Restart=on-failure
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/neutron-dhcp-agent.service /etc/systemd/system/neutron-dhcp-agent.service
      ```

    - neutron-metadata-agent.service

      ```shell
      tee /usr/lib/systemd/system/neutron-metadata-agent.service > /dev/null <<EOF
      [Unit]
      Description=OpenStack Neutron Metadata Agent
      After=syslog.target network.target
      
      [Service]
      Type=simple
      User=neutron
      ExecStart=/usr/bin/neutron-metadata-agent --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/metadata_agent.ini --log-file /var/log/neutron/metadata-agent.log
      PrivateTmp=false
      KillMode=process
      Restart=on-failure
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/neutron-metadata-agent.service /etc/systemd/system/neutron-metadata-agent.service
      ```

    - neutron-l3-agent.service

      ```shell
      tee /usr/lib/systemd/system/neutron-l3-agent.service  > /dev/null <<EOF
      [Unit]
      Description=OpenStack Neutron Layer 3 Agent
      After=syslog.target network.target
      
      [Service]
      Type=simple
      User=neutron
      ExecStart=/usr/bin/neutron-l3-agent --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/l3_agent.ini --log-file /var/log/neutron/l3-agent.log
      PrivateTmp=false
      KillMode=process
      Restart=on-failure
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/neutron-metadata-agent.service /etc/systemd/system/neutron-metadata-agent.service
      ```

  - 计算节点

    - neutron-openvswitch-agent

- 服务启动

  ```shell
  systemctl enable --now neutron-server neutron-openvswitch-agent neutron-dhcp-agent neutron-metadata-agent neutron-l3-agent
  ```

- 验证

  ```shell
  . .admin-openrc
  
  (venv) [root@controller-1 neutron]# openstack network agent list
  +--------------------------------------+--------------------+--------------+-------------------+-------+-------+---------------------------+
  | ID                                   | Agent Type         | Host         | Availability Zone | Alive | State | Binary                    |
  +--------------------------------------+--------------------+--------------+-------------------+-------+-------+---------------------------+
  | 562d9597-607d-4f65-8515-2363f84c06c9 | DHCP agent         | controller-1 | nova              | :-)   | UP    | neutron-dhcp-agent        |
  | 82290ffd-3fb2-4332-8bef-09e39ab269b0 | Metadata agent     | controller-1 | None              | :-)   | UP    | neutron-metadata-agent    |
  | 8d1fad4d-16fb-47be-8561-dcdec70c1fda | Open vSwitch agent | controller-1 | None              | :-)   | UP    | neutron-openvswitch-agent |
  | f89a2d13-70cc-4919-aa8f-20cada1d7364 | L3 agent           | controller-1 | nova              | :-)   | UP    | neutron-l3-agent          |
  +--------------------------------------+--------------------+--------------+-------------------+-------+-------+---------------------------+
  ```

#### cinder

- 依赖组件安装

  - 本地盘

    ```shell
    dnf install lvm2 device-mapper-persistent-data scsi-target-utils rpcbind nfs-utils 
    ```

    - 配置lvm卷组

      ```shell
      # 配置lvm卷组
      pvcreate /dev/sdb
      vgcreate cinder-volumes /dev/sdb
      
      # 多盘
      pvcreate /dev/sda /dev/sdb /dev/sdc /dev/sdd
      vgcreate raidVG /dev/sda /dev/sdb /dev/sdc /dev/sdd
      lvcreate -L 1000G -n vm_data raidVG
      mkfs.ext4 /dev/raidVG/vm_data
      
      mount /dev/raidVG/vm_data /vm_data/
      vi /etc/fstab
      /dev/raidVG/vm_data     /vm_data                ext4    defaults        0 0
      
      # nova 
      mkdir -p /vm_data/openstack/nova
      chown -R nova:nova /vm_data/openstack/nova
      
      # nova nova.conf
      instances_path = /vm_data/openstack/nova
      ```

  - 云盘

    待补充

    

- 创建cinder用户

  ```shell
  getent group cinder >/dev/null || groupadd -r cinder
  if ! getent passwd cinder >/dev/null; then
    useradd -r -g cinder -G cinder,nobody -d /var/lib/cinder -s /sbin/nologin -c "OpenStack Cinder Daemons" cinder
  fi
  ```

- 源代码拉取

  1. 拉取cinder代码

     ```shell
     git clone $REPO_URL/cinder.git /opt/cinder && git config --global --add safe.directory /opt/nova
     ```

  2. 切换分支

     ```shell
     cd /opt/neutron && git checkout -b stable/$BRANCH_VERSION remotes/origin/stable/$BRANCH_VERSION
     ```

     

- 文件夹配置

  1. 创建文件夹

     ```shell
     mkdir -p /var/log/cinder/ /var/lib/cinder /etc/cinder
     ```

  2. 文件夹授权

     ```shell
     chown -R cinder:cinder /var/log/cinder/ /var/lib/cinder /etc/cinder
     ```

- 虚环境创建

  1. 初始化虚环境

     ```shell
     python -m venv /opt/cinder/venv
     ```

  2. 激活虚环境

     ```shell
     source /opt/cinder/venv/bin/activate
     ```

  3. 依赖安装

     ```shell
     pip install -r requirements.txt && python /opt/nova/setup.py install && pip install python-memcached pymysql SQLAlchemy==1.4.52
     ```

  4. 移动执行文件到指定目录

     ```shell
     cp /opt/nova/venv/bin/cinder-* /usr/bin/
     ```

- 配置文件

  1. 日志配置

     ```shell
     tee /etc/logrotate.d/cinder > /dev/null <<EOF
     /var/log/cinder/*.log {
         rotate 14
         size 10M
         missingok
         compress
         copytruncate
     }
     
     EOF
     ```

  2. 配置文件

     - 基础配置文件

       ```shell
       cp -r /opt/cinder/etc/cinder/* /etc/cinder/
       ```

     - /etc/cinder/cinder.conf

       ```shell
       tee /etc/cinder/cinder.conf > /dev/null <<EOF
       
       [DEFAULT]
       transport_url = rabbit://openstack:$RABBITMQ_SERVER_OPENSTACK_PASSWD@${HOSTNAME}
       auth_strategy = keystone
       my_ip = $IPADDR
       enabled_backends = lvm
       backup_driver=cinder.backup.drivers.nfs.NFSBackupDriver
       backup_share=controller:/data/cinder/backup
       
       osapi_volume_workers = 3
       
       [database]
       connection = mysql+pymysql://cinder:$CINDER_PASS@${HOSTNAME}/cinder
       
       [keystone_authtoken]
       www_authenticate_uri = http://${HOSTNAME}:5000
       auth_url = http://${HOSTNAME}:5000
       memcached_servers = ${HOSTNAME}:11211
       auth_type = password
       project_domain_name = Default
       user_domain_name = Default
       project_name = service
       username = cinder
       password = $CINDER_PASS
       
       [oslo_concurrency]
       lock_path = /var/lib/cinder/tmp
       
       [lvm]
       volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver
       volume_group = cinder-volumes
       iscsi_protocol = iscsi
       iscsi_helper = tgtadm
       
       EOF
       ```

- 数据库配置

  1. 数据表

     ```shell
     mysql -e "\
         CREATE DATABASE cinder; \
         GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'localhost' IDENTIFIED BY '$CINDER_PASS'; \
         GRANT ALL PRIVILEGES ON cinder.* TO 'cinder'@'%' IDENTIFIED BY '$CINDER_PASS';"
     ```

  2. 同步表结构

     ```shell
     su -s /bin/sh -c "cinder-manage db sync" cinder
     ```

- 服务凭证

  ```shell
  source ~/.admin-openrc && \
      openstack user create --domain default --password "$CINDER_PASS" cinder && \
      openstack role add --project service --user cinder admin && \
      openstack service create --name cinderv2 --description "OpenStack Block Storage" volumev2 && \
      openstack service create --name cinderv3 --description "OpenStack Block Storage" volumev3 && \
      openstack endpoint create --region RegionOne volumev2 public http://${HOSTNAME}:8776/v2/%\(project_id\)s && \
      openstack endpoint create --region RegionOne volumev2 internal http://${HOSTNAME}:8776/v2/%\(project_id\)s && \
      openstack endpoint create --region RegionOne volumev2 admin http://${HOSTNAME}:8776/v2/%\(project_id\)s && \
      openstack endpoint create --region RegionOne volumev3 public http://${HOSTNAME}:8776/v3/%\(project_id\)s && \
      openstack endpoint create --region RegionOne volumev3 internal http://${HOSTNAME}:8776/v3/%\(project_id\)s && \
      openstack endpoint create --region RegionOne volumev3 admin http://${HOSTNAME}:8776/v3/%\(project_id\)s
      
  
  # HCI 需要对 volume 配置
   openstack endpoint create --region RegionOne volumev2 public http://${HOSTNAME}:8776/v2 && \
   openstack endpoint create --region RegionOne volumev2 admin http://${HOSTNAME}:8776/v2 && \
    openstack endpoint create --region RegionOne volumev3 public http://${HOSTNAME}:8776/v3 && \
   openstack endpoint create --region RegionOne volumev3 admin http://${HOSTNAME}:8776/v3
  ```

  

- 服务配置

  - sudoer

    ```shell
    tee /etc/sudoers.d/cinder > /dev/null <<EOF
    
    Defaults:cinder !requiretty
    
    cinder ALL = (root) NOPASSWD: /usr/bin/cinder-rootwrap /etc/cinder/rootwrap.conf *
    EOF
    ```

  - 服务配置

    - openstack-cinder-api

      ```shell
      tee /usr/lib/systemd/system/openstack-cinder-api.service > /dev/null <<EOF
      [Unit]
      Description=OpenStack Cinder API Server
      After=syslog.target network.target
      
      [Service]
      Type=simple
      User=cinder
      ExecStart=/usr/bin/cinder-api --config-file /etc/cinder/cinder.conf --logfile /var/log/cinder/api.log
      Restart=on-failure
      KillMode=process
      
      [Install]
      WantedBy=multi-user.target
      
      EOF
      
      ln -s /usr/lib/systemd/system/openstack-cinder-api.service /etc/systemd/system/openstack-cinder-api.service
      ```

    - openstack-cinder-scheduler

      ```shell
      tee /usr/lib/systemd/system/openstack-cinder-scheduler.service > /dev/null <<EOF
      [Unit]
      Description=OpenStack Cinder Scheduler Server
      After=syslog.target network.target
      
      [Service]
      Type=simple
      User=cinder
      ExecStart=/usr/bin/cinder-scheduler --config-file /etc/cinder/cinder.conf --logfile /var/log/cinder/scheduler.log
      Restart=on-failure
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/openstack-cinder-scheduler.service /etc/systemd/system/openstack-cinder-scheduler.service
      ```

    - openstack-cinder-volume

      ```shell
      tee /usr/lib/systemd/system/openstack-cinder-volume.service > /dev/null <<EOF
      [Unit]
      Description=OpenStack Cinder Volume Server
      After=syslog.target network.target
      
      [Service]
      LimitNOFILE=131072
      LimitNPROC=131072
      Type=simple
      User=cinder
      ExecStart=/usr/bin/cinder-volume --config-file /etc/cinder/cinder.conf --logfile /var/log/cinder/volume.log
      Restart=on-failure
      KillMode=process
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/openstack-cinder-volume.service /etc/systemd/system/openstack-cinder-volume.service
      ```

    - openstack-cinder-backup

      ```shell
      tee /usr/lib/systemd/system/openstack-cinder-backup.service > /dev/null <<EOF
      [Unit]
      Description=OpenStack Cinder Backup Server
      After=syslog.target network.target
      
      [Service]
      Type=simple
      User=cinder
      ExecStart=/usr/bin/cinder-backup --config-file /etc/cinder/cinder.conf --logfile /var/log/cinder/backup.log
      Restart=on-failure
      
      [Install]
      WantedBy=multi-user.target
      EOF
      
      ln -s /usr/lib/systemd/system/openstack-cinder-backup.service /etc/systemd/system/openstack-cinder-backup.service
      ```

- 服务启动

  ```shell
  systemctl enable --now openstack-cinder-api openstack-cinder-scheduler openstack-cinder-volume openstack-cinder-backup
  ```

- 验证

  ```shell
  # 重启服务
  systemctl restart openstack-cinder-api 
  openstack volume service list
  ```

#### neutron fwaas

待补充

#### octavia

- 依赖包安装

  ```shell
  dnf install genisoimage
  ```

- 创建用户

  ```shell
  getent group octavia >/dev/null || groupadd -r octavia
  if ! getent passwd octavia >/dev/null; then
    useradd -r -g octavia -G octavia,nobody -d /var/lib/octavia -s /sbin/nologin -c "OpenStack Octavia Daemons" octavia
  fi
  ```

- 源代码拉取

  1. 拉取octavia代码

     ```shell
     git clone $REPO_URL/octavia.git /opt/octavia
     ```

  2. 切换分支

     ```shell
     cd /opt/octavia && git checkout -b stable/$BRANCH_VERSION remotes/origin/stable/$BRANCH_VERSION
     ```

- 虚环境创建

  1. 创建目录

     ```shell
     python -m venv /opt/octavia/venv
     ```

  2. 激活虚环境

     ```shell
     source /opt/octavia/venv/bin/activate
     ```

  3. 安装依赖包

     ```shell
     pip install -r requirements.txt && python /opt/octavia/setup.py install && pip install python-memcached pymysql SQLAlchemy==1.4.52
     ```

  4. 移动可执行文件

     ```shell
     cp /opt/octavia/venv/bin/neutron-* /usr/bin/
     ```

- 文件夹配置

  ```shell
  mkdir -p /etc/octavia
  ```

- 创建数据库

  1. 创建表

     ```shell
     mysql -e "\
         CREATE DATABASE octavia; \
         GRANT ALL PRIVILEGES ON octavia.* TO 'octavia'@'localhost' IDENTIFIED BY '$OCTAVIA_PASS'; \
         GRANT ALL PRIVILEGES ON octavia.* TO 'octavia'@'%' IDENTIFIED BY '$OCTAVIA_PASS';"
     ```

  2. 同步表结构

     ```shell
     sudo octavia-db-manage --config-file /etc/octavia/octavia.conf upgrade head
     ```

- 服务凭证和端点

  ```shell
  source ~/.admin-openrc && openstack user create --domain default --password octavia $OCTAVIA_PASS && openstack role add --project service --user octavia admin && openstack service create --name octavia --description "OpenStack Octavia" load-balancer && openstack endpoint create --region RegionOne load-balancer public http://${HOSTNAME}:9876 && openstack endpoint create --region RegionOne load-balancer internal http://${HOSTNAME}:9876 && openstack endpoint create --region RegionOne load-balancer admin http://${HOSTNAME}:9876
  
  
  # HCI 额外配置
  openstack service create --name octavia --description "OpenStack Load Balancer service" loadbalancer
  
  openstack endpoint create --region RegionOne loadbalancer public http://${HOSTNAME}:9876 && openstack endpoint create --region RegionOne loadbalancer internal http://${HOSTNAME}:9876 && openstack endpoint create --region RegionOne loadbalancer admin http://${HOSTNAME}:9876
  ```

- openrc

  ```shell
  cat << EOF >> $HOME/octavia-openrc
  export OS_PROJECT_DOMAIN_NAME=Default
  export OS_USER_DOMAIN_NAME=Default
  export OS_PROJECT_NAME=service
  export OS_USERNAME=octavia
  export OS_PASSWORD=$OCTAVIA_PASS
  export OS_AUTH_URL=http://controller-1:5000
  export OS_IDENTITY_API_VERSION=3
  export OS_IMAGE_API_VERSION=2
  export OS_VOLUME_API_VERSION=3
  EOF
  ```

  

- 负载均衡镜像

  - 手动制作镜像

    ```shell
    git clone https://github.com/openstack/octavia.git /opt/octavia && cd octavia
    git checkout -b 2023.2 remotes/origin/stable/2023.2
    # 虚环境搭建
    
    python -m venv /opt/octavia/venv
    source /opt/octavia/venv/bin/activate
    
    pip install diskimage-builder
    
    cd octavia/diskimage-create/
    
    # export DIB_REPOLOCATION_amphora_agent=https://jihulab.com/james-curtis/octavia.git
    # export DIB_REPOLOCATION_octavia_lib=https://jihulab.com/james-curtis/octavia-lib.git
    export DIB_DISTRIBUTION_MIRROR=http://mirrors.ustc.edu.cn/centos-stream
    export DIB_PYPI_MIRROR_URL=https://pypi.tuna.tsinghua.edu.cn/simple
    export DIB_NO_PYPI_PIP=1
    export DIB_DEBUG_TRACE=1
    export TMPDIR=/root/
    
    ./diskimage-create.sh -a aarch64 -i centos-minimal -o amphora-aarch64-haproxy -r Kingsoft123
    ```

  - 镜像 config driver可能用不来 需要 openstack image set --property hw_scsi_model=virtio-scsi 镜像ID

    ```shell
    openstack image create --disk-format qcow2 --container-format bare --private --tag amphora --property hw_scsi_model=virtio-scsi --file amphora-aarch64-haproxy.qcow2 amphora-haproxy-aarch64
    ```

- 创建flavor

  ```shell
  openstack flavor create --id 200 --vcpus 1 --ram 1024 --disk 4 "amphora" --private
  ```

- 创建证书

  - 自动方式

    1. 进入工作目录

       ```shell
       cd /opt/octavia/bin
       ```

    2. 复制创建证书脚本

       ```shell
       cp create_dual_intermediate_CA.sh create_certs.sh
        
       # 设置一个密码
       sed -i '26i PASSPHRASE="<password>"' create_certs.sh
       sed -i 's/pass:not-secure-passphrase/pass:$PASSPHRASE/g' create_certs.sh
       
       ./create_certs.sh 
       ```

    3. 复制证书到指定目录

       ```shell
       cp -r dual_ca/etc/octavia/certs /etc/octavia/
       
       chmod 700 /etc/octavia/certs
       chmod 700 /etc/octavia/certs/server_ca.key.pem
       chmod 700 /etc/octavia/certs/client.cert-and-key.pem
       chown -R octavia.octavia /etc/octavia/certs
       ```

  - 手动方式

    1. 创建工作目录

       ```shell
       mkdir /opt/certs
       chmod 700 certs
       cd /opt/certs
       ```

    2. 创建OpenSSL 配置文件

       default_days 证书默认时间 10年

       default_bits 默认长度 2048

       ```shell
       tee /opt/certs/openssl.cnf > /dev/null << \EOF
       # OpenSSL root CA configuration file.
       
       [ ca ]
       # `man ca`
       default_ca = CA_default
       
       [ CA_default ]
       # Directory and file locations.
       dir               = ./
       certs             = $dir/certs
       crl_dir           = $dir/crl
       new_certs_dir     = $dir/newcerts
       database          = $dir/index.txt
       serial            = $dir/serial
       RANDFILE          = $dir/private/.rand
       
       # The root key and root certificate.
       private_key       = $dir/private/ca.key.pem
       certificate       = $dir/certs/ca.cert.pem
       
       # For certificate revocation lists.
       crlnumber         = $dir/crlnumber
       crl               = $dir/crl/ca.crl.pem
       crl_extensions    = crl_ext
       default_crl_days  = 30
       
       # SHA-1 is deprecated, so use SHA-2 instead.
       default_md        = sha256
       
       name_opt          = ca_default
       cert_opt          = ca_default
       default_days      = 3650
       preserve          = no
       policy            = policy_strict
       
       [ policy_strict ]
       # The root CA should only sign intermediate certificates that match.
       # See the POLICY FORMAT section of `man ca`.
       countryName             = match
       stateOrProvinceName     = match
       organizationName        = match
       organizationalUnitName  = optional
       commonName              = supplied
       emailAddress            = optional
       
       [ req ]
       # Options for the `req` tool (`man req`).
       default_bits        = 2048
       distinguished_name  = req_distinguished_name
       string_mask         = utf8only
       
       # SHA-1 is deprecated, so use SHA-2 instead.
       default_md          = sha256
       
       # Extension to add when the -x509 option is used.
       x509_extensions     = v3_ca
       
       [ req_distinguished_name ]
       # See <https://en.wikipedia.org/wiki/Certificate_signing_request>.
       countryName                     = Country Name (2 letter code)
       stateOrProvinceName             = State or Province Name
       localityName                    = Locality Name
       0.organizationName              = Organization Name
       organizationalUnitName          = Organizational Unit Name
       commonName                      = Common Name
       emailAddress                    = Email Address
       
       # Optionally, specify some defaults.
       countryName_default             = US
       stateOrProvinceName_default     = Oregon
       localityName_default            =
       0.organizationName_default      = OpenStack
       organizationalUnitName_default  = Octavia
       emailAddress_default            =
       commonName_default              = example.org
       
       [ v3_ca ]
       # Extensions for a typical CA (`man x509v3_config`).
       subjectKeyIdentifier = hash
       authorityKeyIdentifier = keyid:always,issuer
       basicConstraints = critical, CA:true
       keyUsage = critical, digitalSignature, cRLSign, keyCertSign
       
       [ usr_cert ]
       # Extensions for client certificates (`man x509v3_config`).
       basicConstraints = CA:FALSE
       nsCertType = client, email
       nsComment = "OpenSSL Generated Client Certificate"
       subjectKeyIdentifier = hash
       authorityKeyIdentifier = keyid,issuer
       keyUsage = critical, nonRepudiation, digitalSignature, keyEncipherment
       extendedKeyUsage = clientAuth, emailProtection
       
       [ server_cert ]
       # Extensions for server certificates (`man x509v3_config`).
       basicConstraints = CA:FALSE
       nsCertType = server
       nsComment = "OpenSSL Generated Server Certificate"
       subjectKeyIdentifier = hash
       authorityKeyIdentifier = keyid,issuer:always
       keyUsage = critical, digitalSignature, keyEncipherment
       extendedKeyUsage = serverAuth
       
       [ crl_ext ]
       # Extension for CRLs (`man x509v3_config`).
       authorityKeyIdentifier=keyid:always
       EOF
       ```

    3. 创建证书目录

       ```shell
       mkdir client_ca
       mkdir server_ca
       ```

    4. 配置服务器CA

       ```shell
       cd server_ca
       mkdir certs crl newcerts private
       chmod 700 private
       touch index.txt
       echo 1000 > serial
       ```

    5. 创建服务器CA密钥

       指定一个密码，后续配置文件使用

       ```shell
       openssl genpkey -algorithm RSA -out private/ca.key.pem -aes-128-cbc -pkeyopt rsa_keygen_bits:4096
       chmod 400 private/ca.key.pem
       ```

    6. 创建服务器CA证书

       ```shell
       openssl req -config ../openssl.cnf -key private/ca.key.pem -new -x509 -days 7300 -sha256 -extensions v3_ca -out certs/ca.cert.pem
       ```

    7. 移动到client_ca,准备CA

       ```shell
       cd ../client_ca
       mkdir certs crl csr newcerts private
       chmod 700 private
       touch index.txt
       echo 1000 > serial
       ```

    8. 创建客户端CA密钥

       指定一个密码

       ```shell
       openssl genpkey -algorithm RSA -out private/ca.key.pem -aes-128-cbc -pkeyopt rsa_keygen_bits:4096
       chmod 400 private/ca.key.pem
       ```

    9. 创建客户端CA证书

       ```shell
       openssl req -config ../openssl.cnf -key private/ca.key.pem -new -x509 -days 7300 -sha256 -extensions v3_ca -out certs/ca.cert.pem
       ```

    10. 创建要使用的客户端证书的密钥

        ```shell
        openssl genpkey -algorithm RSA -out private/client.key.pem -aes-128-cbc -pkeyopt rsa_keygen_bits:2048
        ```

    11. 为控制器创建证书

        ```shell
        openssl req -config ../openssl.cnf -new -sha256 -key private/client.key.pem -out csr/client.csr.pem
        ```

    12. 为客户端证书进行签名

        ```shell
        openssl ca -config ../openssl.cnf -extensions usr_cert -days 7300 -notext -md sha256 -in csr/client.csr.pem -out certs/client.cert.pem
        ```

    13. 创建连接客户端证书和密钥文件

        ```shell
        openssl rsa -in private/client.key.pem -out private/client.cert-and-key.pem
        
        cat certs/client.cert.pem >> private/client.cert-and-key.pem
        ```

    14. 配置octavia

        ```shell
        cd ..
        mkdir /etc/octavia/certs
        chmod 700 /etc/octavia/certs
        cp server_ca/private/ca.key.pem /etc/octavia/certs/server_ca.key.pem
        chmod 700 /etc/octavia/certs/server_ca.key.pem
        cp server_ca/certs/ca.cert.pem /etc/octavia/certs/server_ca.cert.pem
        cp client_ca/certs/ca.cert.pem /etc/octavia/certs/client_ca.cert.pem
        cp client_ca/private/client.cert-and-key.pem /etc/octavia/certs/client.cert-and-key.pem
        chmod 700 /etc/octavia/certs/client.cert-and-key.pem
        chown -R octavia.octavia /etc/octavia/certs
        ```

- 配置文件

  - /etc/octavia/octavia.conf

    ```shell
    tee /etc/octavia/octavia.conf > /dev/null << EOF
    
    [DEFAULT]
    transport_url = rabbit://openstack:$RABBITMQ_SERVER_OPENSTACK_PASSWD@$HOSTNAME
    log_dir = /var/log/octavia
    log_file = octavia.log
    log_level = DEBUG
    control_exchange = octavia
    default_notification_exchange = octavia
    default_rpc_exchange = octavia
    
    [api_settings]
    bind_host = $IPADDR
    bind_port = 9876
    api_handler = queue_producer
    auth_strategy = keystone
    [database]
    connection = mysql+pymysql://octavia:$OCTAVIA_PASS@$HOSTNAME/octavia
    [oslo_messaging]
    topic = octavia_prov
    [api_settings]
    bind_host = 0.0.0.0
    bind_port = 9876
    
    [keystone_authtoken]
    www_authenticate_uri = http://$HOSTNAME:5000
    auth_url = http://$HOSTNAME:5000
    memcached_servers = $HOSTNAME:11211
    auth_type = password
    project_domain_name = Default
    user_domain_name = Default
    project_name = service
    username = octavia
    password = $OCTAVIA_PASS
    
    [service_auth]
    auth_url = http://$HOSTNAME:5000
    memcached_servers = $HOSTNAME:11211
    auth_type = password
    project_domain_name = Default
    user_domain_name = Default
    project_name = service
    username = octavia
    password = $OCTAVIA_PASS
    
    [certificates]
    server_certs_key_passphrase = insecure-key-do-not-use-this-key
    ca_private_key_passphrase = Kingsoft123  #（创建证书时的密码）
    cert_generator = local_cert_generator
    ca_private_key = /etc/octavia/certs/server_ca.key.pem
    ca_certificate = /etc/octavia/certs/server_ca.cert.pem
    
    [haproxy_amphora]
    server_ca = /etc/octavia/certs/server_ca.cert.pem
    client_cert = /etc/octavia/certs/client.cert-and-key.pem
    [health_manager]
    bind_port = 5555
    bind_ip = $IPADDR
    controller_ip_port_list = $IPADDR:5555
    
    [controller_worker]
    amp_image_owner_id = 229a31ea311645f89d747df3671a51ee
    amp_image_tag = amphora
    amp_ssh_key_name = octavia_ssh_key
    amp_secgroup_list = 92f71c0d-ec73-46f2-bac3-3a43731d6bd9
    amp_boot_network_list = ff2a2c45-9cbd-4319-9431-7210c299eed4
    amp_flavor_id = 200
    network_driver = allowed_address_pairs_driver
    compute_driver = compute_nova_driver
    amphora_driver = amphora_haproxy_rest_driver
    client_ca = /etc/octavia/certs/client_ca.cert.pem
    
    [driver_agent]
    status_socket_path = /var/run/octavia/status_socket
    stats_socket_path = /var/run/octavia/stats_socket
    get_socket_path = /var/run/octavia/get_socket
    log_level = INFO
    pid_file = /var/run/octavia/driver-agent.pid
    debug = True
    
    [notifications]
    notify_on_state_change = all
    
    [oslo_messaging_notifications]
    driver = messaging
    transport_url = rabbit://openstack:$RABBITMQ_SERVER_OPENSTACK_PASSWD@$HOSTNAME:5672/
    topic = octavia
    ```

- 创建安全组

  ```shell
  openstack security group create lb-mgmt-sec-grp --project service
  openstack security group rule create --protocol udp --dst-port 5555 lb-mgmt-sec-grp
  openstack security group rule create --protocol tcp --dst-port 22 lb-mgmt-sec-grp
  openstack security group rule create --protocol tcp --dst-port 9443 lb-mgmt-sec-grp
  openstack security group rule create --protocol icmp lb-mgmt-sec-grp
  openstack security group create lb-health-mgr-sec-grp
  openstack security group rule create --protocol udp --dst-port 5555 lb-health-mgr-sec-grp
  ```

- 创建密钥对

  ```shell
  mkdir -p /etc/octavia/.ssh
  ssh-keygen -b 2048 -t rsa -N “” -f /etc/octavia/.ssh/octavia_ssh_key
  openstack keypair create --public-key /etc/octavia/.ssh/octavia_ssh_key.pub octavia_ssh_key
  ```

- 创建dhclient配置文件

  ```shell
  sudo mkdir -m755 -p /etc/dhcp/octavia
  sudo cp /opt/octavia/etc/dhcp/dhclient.conf /etc/dhcp/octavia
  ```

- 创建网络

  ```shell
  #openstack network create lb-mgmt-net
  # openstack subnet create lb-mgmt-subnet --network lb-mgmt-net --subnet-range #10.168.0.0/24 --allocation-pool start=10.168.0.2,end=10.168.0.200 --gateway 10.168.0.1
  
  OCTAVIA_MGMT_SUBNET=10.168.0.0/24
  OCTAVIA_MGMT_SUBNET_START=10.168.0.2
  OCTAVIA_MGMT_SUBNET_END=10.168.0.200
  OCTAVIA_MGMT_PORT_IP=10.168.0.3
  
  openstack network create lb-mgmt-net --project admin
  openstack subnet create --subnet-range $OCTAVIA_MGMT_SUBNET --allocation-pool \
  start=$OCTAVIA_MGMT_SUBNET_START,end=$OCTAVIA_MGMT_SUBNET_END \
  --network lb-mgmt-net lb-mgmt-subnet --project admin
  
  SUBNET_ID=$(openstack subnet show lb-mgmt-subnet -f value -c id)
  PORT_FIXED_IP="--fixed-ip subnet=$SUBNET_ID,ip-address=$OCTAVIA_MGMT_PORT_IP"
  
  MGMT_PORT_ID=$(openstack port create --security-group \
  lb-health-mgr-sec-grp --device-owner Octavia:health-mgr \
  --host=$(hostname) -c id -f value --network lb-mgmt-net \
  $PORT_FIXED_IP octavia-health-manager-listen-port)
  
  MGMT_PORT_MAC=$(openstack port show -c mac_address -f value \
  $MGMT_PORT_ID)
  
  MGMT_PORT_IP=$(openstack port show -f yaml -c fixed_ips \
  $MGMT_PORT_ID | awk'{FS=",|";gsub(",","");gsub("'\''",""); \for(line = 1; line <= NF; ++line) {if ($line ~ /^- ip_address:/) \
  {split($line, word, "");if (ENVIRON["IPV6_ENABLED"] == "" && word[3] ~ /\./) \
  print word[3];if (ENVIRON["IPV6_ENABLED"] != "" && word[3] ~ /:/) print word[3];} \
  else {split($line, word, "");for(ind in word) {if (word[ind] ~ /^ip_address=/) \
  {split(word[ind], token, "=");if (ENVIRON["IPV6_ENABLED"] == "" && token[2] ~ /\./) \
  print token[2];if (ENVIRON["IPV6_ENABLED"] != "" && token[2] ~ /:/) print token[2];}}}}}')
  
  
  ovs-vsctl --may-exist add-port br-int o-hm0 \
    -- set Interface o-hm0 type=internal \
    -- set Interface o-hm0 external-ids:iface-status=active \
    -- set Interface o-hm0 external-ids:attached-mac=$MGMT_PORT_MAC \
    -- set Interface o-hm0 external-ids:iface-id=$MGMT_PORT_ID
    
   
  vi /etc/octavia/dhcp/dhclient.conf
   request subnet-mask,broadcast-address,interface-mtu;
  do-forward-updates false;
  
  ip link set dev o-hm0 address $MGMT_PORT_MAC
  # 可能会覆盖route 导致断网
  dhclient -v o-hm0 -cf /etc/octavia/dhcp/dhclient.conf
    
  sudo ip link set dev o-hm0 address $MGMT_PORT_MAC
  sudo dhclient -v o-hm0 -cf /etc/dhcp/octavia/dhclient.conf
  ```

- 添加系统服务

  - octavia-api.service

    ```shell
    tee /usr/lib/systemd/system/octavia-api.service  > /dev/null <<EOF
    [Unit]
    Description=OpenStack Octavia API service
    After=syslog.target network.target
    
    [Service]
    Type=simple
    User=octavia
    ExecStart=/usr/bin/octavia-api --config-file /etc/octavia/octavia.conf --log-file /var/log/octavia/api.log
    PrivateTmp=true
    NotifyAccess=all
    KillMode=process
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target
    EOF
    
    ln -s /usr/lib/systemd/system/octavia-api.service /etc/systemd/system/octavia-api.service
    ```

  - octavia-worker.service

    ```shell
    tee /usr/lib/systemd/system/octavia-worker.service  > /dev/null <<EOF
    [Unit]
    Description=OpenStack Octavia Worker service
    After=syslog.target network.target
    
    [Service]
    Type=simple
    User=octavia
    ExecStart=/usr/bin/octavia-worker --config-file /etc/octavia/octavia.conf --log-file /var/log/octavia/worker.log
    PrivateTmp=true
    KillMode=process
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target
    EOF
    
    ln -s /usr/lib/systemd/system/octavia-worker.service /etc/systemd/system/octavia-worker.service
    ```

  - octavia-health-manager.service

    ```shell
    tee /usr/lib/systemd/system/octavia-health-manager.service > /dev/null <<EOF
    [Unit]
    Description=OpenStack Octavia Health-Manager service
    After=syslog.target network.target
    
    [Service]
    Type=simple
    User=octavia
    ExecStart=/usr/bin/octavia-health-manager --config-file /etc/octavia/octavia.conf --log-file /var/log/octavia/health-manager.log
    PrivateTmp=false
    KillMode=process
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target
    EOF
    
    ln -s /usr/lib/systemd/system/octavia-health-manager.service /etc/systemd/system/octavia-health-manager.service
    ```

  - octavia-housekeeping.service

    ```shell
    tee /usr/lib/systemd/system/octavia-housekeeping.service > /dev/null <<EOF
    [Unit]
    Description=OpenStack Octavia Housekeeping service
    After=syslog.target network.target
    
    [Service]
    Type=simple
    User=octavia
    ExecStart=/usr/bin/octavia-housekeeping --config-file /etc/octavia/octavia.conf --log-file /var/log/octavia/housekeeping.log
    PrivateTmp=true
    NotifyAccess=all
    KillMode=process
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target
    EOF
    
    ln -s /usr/lib/systemd/system/octavia-housekeeping.service /etc/systemd/system/octavia-housekeeping.service
    ```

  - octavia-amphora-agent

    ```shell
    tee /usr/lib/systemd/system/octavia-amphora-agent.service > /dev/null <<EOF
    [Unit]
    Description=OpenStack Octavia Amphora Agent service
    After=syslog.target network.target
    
    [Service]
    Type=simple
    User=root
    ExecStart=/usr/bin/amphora-agent --config-file /etc/octavia/octavia.conf
    KillMode=process
    Restart=on-failure
    ExecStartPost=/bin/sh -c "echo $MAINPID > /run/octavia-amphora-agent.pid"
    PIDFile=/run/octavia-amphora-agent.pid
    
    [Install]
    WantedBy=multi-user.target
    EOF
    
    tee /etc/systemd/system/octavia-amphora-agent.service > /dev/null <<EOF
    [Unit]
    Description=Octavia Amphora Agent Service
    After=network.target
    
    [Service]
    ExecStart=/usr/bin/amphora-agent --config-file /etc/octavia/octavia.conf
    Restart=always
    User=root
    Group=root
    
    
    [Install]
    WantedBy=multi-user.target
    EOF
    
    ln -s /usr/lib/systemd/system/octavia-amphora-agent.service /etc/systemd/system/octavia-amphora-agent.service
    ```

- 启动服务

  ```shell
  systemctl enable --now  octavia-api octavia-worker octavia-health-manager octavia-housekeeping octavia-amphora-agent
  
  ```

- 验证

  ```shell
  # octavia相关接口
  curl --location --request POST 'http://controller-1:9876/v2/lbaas/loadbalancers' \
  --header 'X-Auth-Token: gAAAAABnPErmDS6LD2rdTjWKJviK2DF37Wfd2PnTg9ddgdP5A01uSIki8P0Bjo8U_G1zqyeBFeCb77-y251IBKLQFxwCO3D-tuiroLUVUsKaJqwiq8095bdldFHdTBlh55a5RF1CuEqTH0IycnMJcK_BIdh1GxeZNpR5H94cjbvZjNZlgwyRcFo' \
  --header 'Content-Type: application/json' \
  --data '{
      "loadbalancer": {
          "description": "zzw-test",
          "admin_state_up": true,      
          "vip_subnet_id": "6427a86d-374d-4314-b8da-b88fe4cfcf86",
          "vip_address": "10.168.0.25",
          "provider": "octavia",
          "name": "test"    
      }
  }'
  
  curl --location --request GET http://controller-1:9876/v2/lbaas/loadbalancers' 
  --header 'X-Auth-Token: gAAAAABnPC0Zy9U2fn4JRAOL3VZjMgRXNFOxNj-72_5jAJGDwW7EiW10YtZabBduMSbhmHBzIL3CRFPiouokQ6v0MRawquVOiaeA29iZahHC4NcciZvjoaNqoq2k9A_jMSzH6g07kSZ7fyB9fIEjv0VA1npxExO5E3jeMb1oMeCzrUgROWmdk0c' --header 'Content-Type: application/json'
  
  curl --location --request DELETE 'http://controller-1:9876/v2/lbaas/loadbalancers/05be1708-2fb8-4110-87c0-f39471b1d862' --header 'X-Auth-Token: gAAAAABmxyexYcto74jwvnaVTr2K6JBvGBwec6pEwh4z4OVvhZI0sisd5xZevjrvUbcu_BWbZyCF3RzMVIufnhh1Spt3ansLtd62xmZtU8FBUNLrKlFANKvnyAhVssnMiYMWDhYzXhEVL0zB8bEv6FetvhR4vGjEPqq0akm9nORClbJbBSFMqCc' --header 'Content-Type: application/json'
  
  curl --location --request POST 'http://controller-1:9876/v2/lbaas/loadbalancers' \
  --header 'X-Auth-Token: gAAAAABm4mNdtEcJv49wZ1G55Td-vbfz58E7lq8d-GBbBdsqBdME-Treaq5iJ_dZ99s69RSeHgDDZmj6USpd5LVtvaVjMGnq5qMCnLwvrPeE0JpaEpNz4wVvxAUh4n8cO4tuyXnW5B423MT5CXEkymMqxebRFZtOsqOCqRaIo6DfC6syQPHHfwA' \
  --header 'Content-Type: application/json' \
  --data '{
    "listener": {
      "name": "my_listener",
      "protocol": "HTTP",
      "protocol_port": 80,
      "loadbalancer_id": "def5dd44-a2b4-4c16-8a90-82d2582e2d54"
    }
  }'
  ```

  



## 验证

```shell
PROJECT_ID=4877a30e870d49bc91bd63257fe321ae

external 需要和 /etc/neutron/plugins/ml2对应 

# 创建网络
openstack network create --project $PROJECT_ID --share --provider-network-type flat --external --provider-physical-network external external-net

NETWORK_ID=6e6c050d-764a-4244-9518-6074ab83bcf9

 # 创建子网    
 openstack subnet create ext_subnet --network external-net --project $PROJECT_ID --subnet-range 192.168.5.0/24 --allocation-pool start=192.168.5.70,end=192.168.5.79 --gateway 192.168.5.1 --dns-nameserver 114.114.114.114
 
 # 创建flavor
 openstack flavor create --id auto --vcpus 2 --ram 1024 --disk 50 2C1G50G
 
 # 安全组
 openstack security group create secgroup
 # 安全组相关放行
 openstack security group rule create --protocol icmp --ingress secgroup
 openstack security group rule create --protocol tcp --dst-port 22 --ingress secgroup
 
 # 创建虚拟机
 openstack server create --flavor 2C1G50G --image openEuler-22.03-LTS-SP3 --security-group secgroup --nic net-id=$NETWORK_ID --password 123 openEuler-22.03-LTS-SP3
 
```

## 问题记录

- placement

  1. `curl http://${HOSTNAME}:8778` 报错

     ```shell
     sqlalchemy.exc.ObjectNotExecutableError: Not an executable object: "SET SESSION SQL_MODE='NO_AUTO_VALUE_ON_ZERO'"
     ```

     原因：SQLAlchemy 版本太高，降级至 1.4.52

- glance

  1. `su -s /bin/sh -c "glance-manage db_sync" glance` 报错

     ```shell
     Traceback (most recent call last):
       File "/usr/bin/glance-manage", line 6, in <module>
         from glance.cmd.manage import main
       File "/opt/glance/venv/lib64/python3.11/site-packages/glance/cmd/manage.py", line 47, in <module>
         from glance.common import config
       File "/opt/glance/venv/lib64/python3.11/site-packages/glance/common/config.py", line 648, in <module>
         policy.Enforcer(CONF)
       File "/opt/glance/venv/lib64/python3.11/site-packages/oslo_policy/policy.py", line 542, in __init__
         self.policy_file = policy_file or pick_default_policy_file(
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^
       File "/opt/glance/venv/lib64/python3.11/site-packages/oslo_policy/policy.py", line 377, in pick_default_policy_file
         if conf.find_file(conf.oslo_policy.policy_file):
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
       File "/opt/glance/venv/lib64/python3.11/site-packages/oslo_config/cfg.py", line 2780, in find_file
         raise NotInitializedError()
     oslo_config.cfg.NotInitializedError: call expression on parser has not been invoked
     ```

     原因： oslo.policy 版本太高 降级至 4.3.0

     解决：重新生成`oslopolicy-policy-generator --namespace glance --output-file /etc/glance/policy.json`

  2. 上传镜像报错
  
     ```shell
     glance_store.exceptions.StoreAddDisabled: Configuration for store failed. Adding images to this store is disabled.
     ```
  
     原因：文件夹权限问题 需要改成 `glance:glance`

- neutron

  1. 启动 neutron-openvswitch-agent 失败

     ```shell
     2025-03-22 08:38:32.731 204083 ERROR neutron   File "/opt/neutron/venv/lib64/python3.11/site-packages/oslo_privsep/priv_context.py", line 261, in _wrap
     2025-03-22 08:38:32.731 204083 ERROR neutron     self.start()
     2025-03-22 08:38:32.731 204083 ERROR neutron   File "/opt/neutron/venv/lib64/python3.11/site-packages/oslo_privsep/priv_context.py", line 275, in start
     2025-03-22 08:38:32.731 204083 ERROR neutron     channel = daemon.RootwrapClientChannel(context=self)
     2025-03-22 08:38:32.731 204083 ERROR neutron               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
     2025-03-22 08:38:32.731 204083 ERROR neutron   File "/opt/neutron/venv/lib64/python3.11/site-packages/oslo_privsep/daemon.py", line 362, in __init__
     2025-03-22 08:38:32.731 204083 ERROR neutron     raise FailedToDropPrivileges(msg)
     2025-03-22 08:38:32.731 204083 ERROR neutron oslo_privsep.daemon.FailedToDropPrivileges: privsep helper command exited non-zero (1)
     ```

     原因：使用虚环境，oslo_privsep代码不兼容

     解决：

     ```shell
     # vi /opt/neutron/venv/lib/python3.11/site-packages/oslo_privsep/priv_context.py +191
     
             if self.conf.helper_command:
                 cmd = shlex.split(self.conf.helper_command)
             else:
                 if cfg.CONF.privsep.helper_command:
                     cmd = _HELPER_COMMAND_PREFIX + [cfg.CONF.privsep.helper_command.split(" ")[1]]
                 else:
                     cmd = _HELPER_COMMAND_PREFIX + ['privsep-helper']
     
     ```

     
