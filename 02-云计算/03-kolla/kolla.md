# kolla镜像构建

## 环境准备

```bash
git clone https://github.com/openstack/kolla.git

cd kolla
python3 -m venv .venv

source .venv/bin/activate

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

pip install kolla docker


git checkout -b 2023.1 origin/stable/2023.1

pip install tox
tox -e genconfig
```

## 配置

```bash
# kolla/etc/kolla/kolla-build.conf

[DEFAULT]
base = centos
base_tag = 7.4.1708

#tarballs_base = http://tarballs.openstack.org
install_type = sourc
tag = queens
logs_dir = /home/hl/kolla_build/kolla/log

[ceilometer-base]
location = http://127.0.0.1/tars/ceilometer-10.0.0.tar.gz

[cinder-base]
location = http://127.0.0.1/tars/cinder-12.0.1.tar.gz

[horizon]
location = http://127.0.0.1/tars/horizon-13.0.0.tar.gz

[horizon-plugin-fwaas-dashboard]
#location = $tarballs_base/neutron-fwaas-dashboard/neutron-fwaas-dashboard-1.3.0.tar.gz
location = http://127.0.0.1/tars/neutron-fwaas-dashboard-1.3.0.tar.gz

[horizon-plugin-neutron-lbaas-dashboard]
location = http://192.168.110.12/tars/neutron-lbaas-dashboard-4.0.0.tar.gz

[horizon-plugin-trove-dashboard]
location = http://192.168.110.12/tars/trove-dashboard-10.0.0.tar.gz

[neutron-base]
location = http://192.168.110.12/tars/neutron-12.0.4.tar.gz

[nova-base]
location = http://192.168.110.12/tars/nova-17.0.2.tar.gz
```

# 相关链接

[kolla部署openstack](../04-openstack/01-部署/Kolla-ansible部署.md)
