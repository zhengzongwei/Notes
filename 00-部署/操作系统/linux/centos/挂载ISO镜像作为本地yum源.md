# 将ISO镜像当作本地yum源

## 备份系统 repo

```shell
# 进入repo 路径
cd /etc/yum.repo.d/

# 创建备份文件家
mkdir bak

# 将本地 repo移动到bak文件家
mv *.repo bak

# 检查 yum.config 是否开启 keepcache

# 创建本地repo文件
vi /etc/yum.repos.d/rhel-local.repo
[rhel-local]
name=rhel-local
baseurl=file:///mnt 
enabled=1
gpgcheck=0

```
