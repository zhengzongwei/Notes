# Building Octavia Amphora Images

```

# 

# docker 环境
dnf install qemu-img sudo policycoreutils-python-utils

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



./diskimage-create.sh -a aarch64 -i centos-minimal -o amphora-aarch64-haproxy -r Kingsoft123

## 参考链接

1. [Building Octavia Amphora Images — octavia 14.1.0.dev85 documentation (openstack.org)](https://docs.openstack.org/octavia/latest/admin/amphora-image-build.html)