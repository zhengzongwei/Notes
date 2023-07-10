# GL-iNet SF1200 官方SDK编译固件指北

## 系统环境

系统 debian 11 

## 安装必要工具

```shell
# debian 12 
sudo apt install build-essential clang flex bison g++ gawk gcc-multilib g++-multilib \
gettext git libncurses-dev libssl-dev python3-distutils rsync unzip zlib1g-dev \
file wget python2

```

## 拉取源码

```shell
git clone  https://github.com/gl-inet/gl-infra-builder.git && cd gl-infra-builder


python3 setup.py -c configs/config-siflower-18.x.yml && cd openwrt-18.06/siflower/openwrt-18.06

./scripts/gen_config.py target_siflower_gl-sft1200 luci

make V=s -j5
```

