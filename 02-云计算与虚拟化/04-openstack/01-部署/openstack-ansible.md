# 待定

## 初始化系统

1. 关闭SELINUX
    ```bash
    setenforce 0 
    
    sed -i 's/SELINUX=enfircing/SELINUX=disabled/g' /etc/selinux/config
    ```
    
2. 关闭防火墙

   ```bash
   systemctl stop firewalld && systemctl disable firewalld
   ```

## open stack-ansible

```bash
git clone https://opendev.org/openstack/openstack-ansible /opt/openstack-ansible
```

```bash

export PIP_OPTS="-i https://pypi.tuna.tsinghua.edu.cn/simple"


cd /opt/openstack-ansible

./script/bootstrap-ansible.sh

lsblk

export BOOTSTRAP_OPTS="bootstrap_host_data_disk_device=nvme0n2"
export BOOTSTRAP_OPTS="bootstrap_host_public_interface=ens192"

cd /opt/openstack-ansible/
cp etc/openstack_deploy/conf.d/{aodh,gnocchi,ceilometer}.yml.aio /etc/openstack_deploy/conf.d/
for f in $(ls -1 /etc/openstack_deploy/conf.d/*.aio); do mv -v ${f} ${f%.*}; done

scripts/bootstrap-aio.sh


cd /opt/openstack-ansible/playbooks
openstack-ansible setup-hosts.yml
openstack-ansible setup-infrastructure.yml
openstack-ansible setup-openstack.yml

```

