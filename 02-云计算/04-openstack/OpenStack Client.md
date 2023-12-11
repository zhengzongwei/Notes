# OpenStack 命令

```shell
openstack-service restart    #重启openstack服务
openstack endpoint list     #查看openstack的端口
openstack catalog list   #列出认证服务目录
openstack project list   # 查看项目列表                                                                             
openstack user list      # 查看用户列表                                                                               
openstack role list      # 查看角色列表

# 以下三条命令，把project换作user、role同样的作用

openstack project create --description 'demo project ' demo  #创建项目                         
openstack project set  ID  --disable/enable/  #设置项目id禁用或开机自启                             
openstack project delete  ID   #删除项目

# ----------------------------------------
openstack service list  #查询openstack服务列表

openstack domain list  #查询openstack domain列表

openstack host list  #查看openstack环境主机列表

openstack port list   #查看port信息

openstack compute service list    #查询计算节点

openstack server list   #查询当前用户vm列表
openstack server list -all  #查询所有vm列表

openstack server show $vmName  #查看vm的详细信息

openstack server start NAME  #启动vm
openstack server stop NAME  #关闭vm
openstack server reboot SERVER   #软重启,软重启试图优雅的关机并重启实例
openstack server reboot --hard SERVER  #硬重启,硬重启则是直接对实例实施电源的拔插
openstack server delete NAME   #删除vm


openstack network list  #查询可用网络信息

openstack flavor list   #查询可用的实例规格

openstack flavor create --ram 512 --disk 1 --vcpus 1 m1.tiny   #创建flavor规格m1.tiny

openstack image list  #查询可用镜像

openstack security group list   #查询可用的安全组

openstack security group rule list default  #查询default安全组的规则

openstack keypair list  #查询可用的秘钥对

openstack volume list   #查询可用的卷组

# ----------------------------------------------------
### nova 常用命令 ###

nova list       #列举当前用户所有虚拟机
nova list --all-t   #查询所有虚拟机
nova list --host <hostname> --all-tenants   #查看此节点所有虚机

nova host-list  #查询计算节点
nova show ID   #列举某个虚机的详细信息
nova delete ID   #直接删除某个虚机

nova service-list      #获取所有服务列表
nova flavor-list      #查看当前可以创建的实例类型
nova secgroup-list  #查看当前存在的安全组
nova keypair-list   #查看当前存在的密钥

nova console-log cirros #查看实例cirros的启动日志信息

nova volume-create      #创建云硬盘
nova volume-delete      #删除云硬盘
nova volume-snapshot-create    #创建云硬盘快照
nova volume-snapshot-delete    #删除云硬盘快照

nova live-migration ID node    #热迁移
nova migrate ID node    #冷迁移
nova migration-list  

nova get-vnc-console ID novnc     #获取虚机的vnc地址
nova reset-state --active ID      # 重置虚拟机状态

nova delete <serverName-Or-Id> # 删除一个虚拟机
nova stop <serverName-Or-Id> # 关闭虚拟机
nova reboot <serverName-Or-Id> # 软重启虚拟机
nova reboot --hard <serverName-Or-Id> # 硬重启虚拟机


nova-manage vm list  #查看实例位置
nova-manage service list  #查询当前启动的Compute服务状态
nova-manage version    #查询当前安装软件的版本
nova-manage vm list    #列出所有的实例状态,可以看到实例所在的计算节点和实例状态
nova-manage host list  #列出当前主机的信息

# ---------------------------------------------
### neutron 常用命令###

neutron agent-list      #列举所有的agent
neutron agent-show  ID     #显示指定agent信息

neutron port-list      #查看端口列表
neutron port-show ID #查看该端口详细信息

neutron net-list      #列出当前租户所有网络
neutron net-list --all-tenants     #列出所有租户所有网络
neutron net-show  ID       #查看一个网络的详细信息
neutron net-delete ID       #删除一个网络

neutron subnet-list #查询子网

neutron security-group-list    #查询安全组

neutron security-group-rule-list   #查询安全组规则

# ----------------------------------------------------
### cinder 常用命令 ###

cinder list   #显示存储卷列表                                                                                 
cinder type-list     #显示存储卷类型列表    
cinder delete ID    #删除卷
cinder force-delete ID  #强制删除卷
cinder show ID # 显示存储卷信息

# ------------------------------------------------------
### IP netns 命令 ###

ip netns  #查看命名空间
ip netsn exec haproxy ip a  #查看haproxy的ip
ip netns exec NETNS_NAME ssh USER@SERVER
ip netns exec qdhcp-6021a3b4-8587-4f9c-8064-0103885dfba2 ssh cirros@10.0.0.2                                                     

# ------------------------------------------------------
### 创建 VM 命令

nova flavor-list  #获取到可用的flavor名称
nova image-list   #获取到可用的image名称
nova network-list 或neutron net-list   #获取到可用的网络id

nova secgroup-list  #获取到可用的安全组id
nova keypair-list #获取到可用的秘钥keypair名称
nova service-list #获取到可用的获取coompute的主机名和zone名称


```
