# Ubuntu 系统配置

## 换源

```shell
sudo sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list



deb https://mirrors.ustc.edu.cn/ubuntu/ impish main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ impish main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ impish-security main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ impish-security main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ impish-updates main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ impish-updates main restricted universe multiverse

deb https://mirrors.ustc.edu.cn/ubuntu/ impish-backports main restricted universe multiverse
deb-src https://mirrors.ustc.edu.cn/ubuntu/ impish-backports main restricted universe multiverse

## Not recommended
# deb https://mirrors.ustc.edu.cn/ubuntu/ impish-proposed main restricted universe multiverse
# deb-src https://mirrors.ustc.edu.cn/ubuntu/ impish-proposed main restricted universe multiverse
```





