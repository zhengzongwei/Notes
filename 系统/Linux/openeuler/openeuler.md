# openeuler 系统配置

## 修改dnf 配置文件

```shell
/etc/dnf/dnf.conf
[main]
gpgcheck=1
installonly_limit=3
clean_requirements_on_remove=True
best=True
skip_if_unavailable=False
keepcache=1


dnf -y upgrade --downloadonly --downloaddir=.
```

## 配置rpm编译环境

```shell
dnf install rpmdevtools*
```