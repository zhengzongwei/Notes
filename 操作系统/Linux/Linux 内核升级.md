# CentOS 7 内核升级

## 编译环境准备

1. 安装开发库

   ```shell
    yum install rpm-build redhat-rpm-config asciidoc hmaccalc perl-ExtUtils-Embed pesign xmlto
    
    yum install audit-libs-devel binutils-devel elfutils-devel elfutils-libelf-devel
    
    yum install ncurses-devel newt-devel numactl-devel pciutils-devel python-devel zlib-devel
   ```

2. 新建普通用户 `useradd <username>`

3. 目录准备

   ```shell
   mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
   echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros
   ```

4. 安装源码组件

5. 解压源码并生成源码

## 编译内核



## 安装和启动

1. 使用root用户 ` yum localinstall ~/rpmbuild/RPMS/`uname -m`/kernel*.rpm`

2. 重启主机











# 参考链接



https://www.mail-archive.com/linux-kernel@vger.kernel.org/msg1636132.html



https://www.jianshu.com/p/28cbb310bb8a





```xml
<hostdev mode='subsystem' type='pci' managed='yes'>
  <source>
    <address domain='0x0000' bus='0x5e' slot='0x04' function='0x2'/>
  </source>
</hostdev>
```