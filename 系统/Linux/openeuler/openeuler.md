# 修改dnf 配置文件
/etc/dnf/dnf.conf
[main]
gpgcheck=1
installonly_limit=3
clean_requirements_on_remove=True
best=True
skip_if_unavailable=False
keepcache=1


dnf -y upgrade --downloadonly --downloaddir=.