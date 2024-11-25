# OpenEuler 2203 loongarch 系统适配

## maturin 包编译

rusts cargo 版本为 1.60 编译提示版本滴 ，升级rust 







## rust 升级



## glibc升级

默认版本glibc为2.34，rust 升级需要依赖的版本是2.36

- 依赖包安装

  ```bash
  dnf install make bison kernel-devel-$(uname -r)
  ```

- glibc 源码包下载

  ```bash
  wget http://ftp.gnu.org/gnu/libc/glibc-2.36.tar.gz
  
  tar -xzvf glibc-2.36.tar.gz
  mv glibc-2.36 /opt/glibc-2.36
  
  cd /opt/glibc-2.36
  
  mkdir build
  cd build
  
  ```

- 构建

  ```bash
  ../configure --prefix=/opt/glibc-2.36
  ```

- 编译

  ```bash
  make -j$(nproc)
  ```

  



