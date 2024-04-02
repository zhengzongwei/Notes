# OpenStack Python虚拟环境搭建

虚拟环境创建

openstack 源码默认放置在opt 目录下，以keystone为例

```bash

cd /opt/
# 克隆 keystone 源码
git clone https://opendev.org/openstack/keystone.git /opt/组件名

# 创建虚拟环境
python3 -m venv /opt/{组件名}/venv

# 进入虚拟环境
source /opt/{组件名}/venv/bin/active

# 安装依赖
pip install -r requirement.txt

# 安装源码
python /opt/{组件名}/setup.py install
```

