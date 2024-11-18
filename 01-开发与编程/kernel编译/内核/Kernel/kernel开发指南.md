# kernel 开发指南

## 背景

> [!NOTE]
>
> 我们在进行驱动开发时，首先将驱动编译为模块(.ko),使用insmod和rmmod进行挂载和卸载。待驱动功能测试稳定后，将其添加到内核中，随内核一起编译。

### 开发环境

- **OS**：centos/ubuntu



## 添加自定义模块

### 新建目录

在kernel-src-dir/drivers 目录下新建hello目录

```bash
cd drivers
mkdir hello
```

### 添加文件

```bash
cd hello

touch Kconfig Makefile hello.c
```

- Kconfig

  ```bash
  menu "hello KM"
  comment "hello kernel module"
  
  config HELLO
      tristate "hello module"
      default y
      help
      hello kernel module test
  endmenu
  ```

- Makefile

  ```bash
  obj-${CONFIG_HELLO} += hello.o
  ```

- hello.c

  ```bash
  #include <linux/module.h>
  #include <linux/kernel.h>
  #include <linux/init.h>
  #include <linux/ktime.h>
  #include <linux/kthread.h>
  #include <linux/delay.h>
  
  static struct task_struct *ht = NULL;
  
  static int thread_hello(void *para)
  {
      int i = 0;
  
      while(!kthread_should_stop())
      {
          printk(KERN_DEBUG "hkm thread run, %d, %lu\n", i++, ktime_get_seconds());
          msleep(1000);
      }
  
      return 0;
  }
  
  static int __init hello_init(void)
  {
      printk(KERN_DEBUG "hello, sdc\n");
  
      ht = kthread_run(thread_hello, NULL, "hello_thread");
      if(NULL == ht)
      {
          printk(KERN_ERR "kernel thread create failed\n");
          return -1;
      }
  
      return 0;
  }
  
  static void __exit hello_exit(void)
  {
      printk(KERN_DEBUG "bye, sdc\n");
      if(NULL != ht)
      {
          kthread_stop(ht);
      }
  }
  
  module_init(hello_init);
  module_exit(hello_exit);
  
  MODULE_LICENSE("GPL");
  MODULE_AUTHOR("sdc");
  MODULE_DESCRIPTION("KM in kernel source");
  ```

### 修改drivers/Koncifg 和drivers/Makefile

- drivers/Kconfig

  ```bash
  source "drivers/hello/Kconfig
  ```

- Makefile

  ```bash
  obj-${CONFIG_HELLO} += hello/
  ```

  | 目录           | 内容                                                         |
  | -------------- | ------------------------------------------------------------ |
  | arch/          | 体系结构相关的代码，如arch/i386、arch/arm、arch/ppc          |
  | crypto         | 常用加密和散列算法（如AES、SHA等），以及一些压缩和CRC校验算法 |
  | drivers/       | 各种设备驱动程序，如drivers/char、drivers/block……            |
  | documentation/ | 内核文档                                                     |
  | fs/            | 文件系统，如fs/ext3、fs/jffs2……                              |
  | include/       | 内核头文件：include/asm是体系结构相关的头文件，它是include/asm-arm、include/asm-i386等目录的链接；include/linux是Linux内核基本的头文件 |
  | init/          | Linux初始化，如main.c                                        |
  | ipc/           | 进程间通信的代码                                             |
  | kernel/        | Linux内核核心代码（这部分比较小）                            |
  | lib/           | 各种库子程序，如zlib、crc32                                  |
  | mm/            | 内存管理代码                                                 |
  | net/           | 网络支持代码，主要是网络协议                                 |
  | sound          | 声音驱动的支持                                               |
  | scripts/       | 内部或者外部使用的脚本                                       |
  | usr/           | 用户的代码                                                   |
  
  
