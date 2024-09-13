# kernel构建开发指南

## 环境信息

**系统版本**：Fedora release 40 (Forty)

**内核版本**：6.8.5-301.fc40.aarch64



## 开发工具和库

```shell
dnf groupinstall "Development Tools" dwarves
```



## 内核编译

### 下载内核源码

Kernel 内核网站 [The Linux Kernel Archives](https://www.kernel.org/)

1. [linux-6.6.42](https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.6.42.tar.xz)

2. [linux-6.10.1](https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.10.1.tar.xz)





```shell
xz -dk linux-6.6.42.tar.xz
tar -xvf linux-6.6.42.tar
```



### 校验tar文件完整性

```shell
gpg2 --locate-keys torvalds@kernel.org gregkh@kernel.org

gpg -v --keyserver hkps://keys.openpgp.org --locate-keys torvalds@kernel.org gregkh@kernel.org

gpg2 --verify linux-*.tar.sign

cd linux-*

cp /boot/config-"$(uname -r)" .config

./scripts/config --file .config --set-str LOCALVERSION "-ksyun"


# arm64
make Image

# x86
zstd ncurses-devel
make bzImage


grub2-mkconfig -o /boot/grub2/grub.cfg
```

## 如何添加一个新驱动模块

1. 构建测试模块

   ```
   cd linux-6.6-63/drivers/
   mkdir hello
   ```

2. 在 hello 创建hello.c、Makefile、kconfig三个文件

   - hello.c

     ```c
     #include <linux/module.h> //所有模块都需要的头文件
     #include <linux/init.h>   // init&exit相关宏
     #include <linux/kernel.h>
      
     MODULE_LICENSE("GPL");
     MODULE_AUTHOR("baoli");
     MODULE_DESCRIPTION("hello world module");
      
     static int __init hello_init(void)
     {
           printk(KERN_WARNING "hello world.\n");
           return 0;
     }
     static void __exit hello_exit(void)
     {
           printk(KERN_WARNING "hello exit!\n");
     }
      
     module_init(hello_init);
     module_exit(hello_exit);
     ```

   - Makefile

     ```makefile
     obj-$(CONFIG_HELLO) += hello.o
     ```

   - Kconfig

     ```bash
     menu "HELLO TEST Driver "
     comment "HELLO TEST Driver Config"
      
     config HELLO
     	tristate "hello module test"
     	default m
     	help
     	This is the hello test driver 
      
     endmenu
     ```

3. 修改上一级目录的Kconfig和Makefile

   ```bash
   cd linux-6.6-63/drivers/
   vim Makefile
   obj-$(CONFIG_HELLO) += hello/
   
   
   vim Kconfig
   source "drivers/hello/Kconfig"
   ```

4. make menuconfig
   - 执行 make menuconfig ARCH=arm
   - Device Drivers选项

5. 单独编译内核驱动

   ```bash
    make -C /home/kernel/linux-6.6.42 M=$(pwd)/drivers/hello modules
   ```

6. 加载编译内核

   ```bash
   cd linux-6.6.42/drivers/hello
   lsmod |grep hello
   
   root@localhost:~/linux-6.6.42/drivers/hello# modinfo hello.ko
   filename:       /root/linux-6.6.42/drivers/hello/hello.ko
   description:    hello world module
   author:         zhengzongwei
   license:        GPL
   depends:
   name:           hello
   vermagic:       6.6.42-ksyun SMP preempt mod_unload aarch64
   root@localhost:~/linux-6.6.42/drivers/hello#
   
   insmod ../hello.ko
   
   ```

7. 打成rpm包

   ```bash
   sudo dnf install rpm-build make gcc bc bison flex elfutils-libelf-devel openssl-devel rpmdevtools perl
   
   构建需要的包
   sudo dnf install asciidoc audit-libs-devel binutils-devel clang fuse-devel glibc-static java-devel kernel-rpm-macros libbabeltrace-devel libbpf-devel libcap-devel libcap-ng-devel libmnl-devel libtraceevent-devel libtracefs-devel llvm-devel newt-devel numactl-devel opencsd-devel pciutils-devel perl-generators python3-devel python3-docutils systemd-boot-unsigned tpm2-tools xmlto gtk2-devel java-1.8.0-openjdk-devel libpfm-devel libunwind-devel  java-1.8.0-openjdk
   ```

   
