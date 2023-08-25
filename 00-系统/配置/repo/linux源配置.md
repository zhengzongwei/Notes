

## 国内源推荐

- mirrors.tuna.tsinghua.edu.cn
- mirrors.ustc.edu.cn
- mirror.nju.edu.cn
- repo.huaweicloud.com



## Ubuntu

1. 备份配置文件

   ```shell
   sudo cp -a /etc/apt/sources.list /etc/apt/sources.list.bak
   ```

2. 修改配置文件

   ```shell
   # x86_64
   sudo sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
   sudo sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
   
   # aarch64
   sudo sed -i 's@//.*ports.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list
   ```

3. 更新索引

   ```shell
   apt-get update
   ```

## Debian

1. 备份配置文件

   ```shell
   sudo cp -a /etc/apt/sources.list /etc/apt/sources.list.bak
   ```

2. 修改配置文件

   ```shell
   sudo sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
   
   # debian 12
   sudo sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources
   
   sudo sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list
   
   ```

3. 更新索引

   ```shell
   apt-get update
   ```

## CentOS

待补充





