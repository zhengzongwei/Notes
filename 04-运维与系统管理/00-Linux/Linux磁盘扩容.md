# Linux 磁盘扩容

## 背景

在默认安装linux发行版的时候，有时候会发现默认的分区不对，导致磁盘容量小，导致编译内核的时候空间不够，需要手动对根分区扩容



## 扩容

- xfs

  1. 检查当前的lvm逻辑卷

     ```bash
     sudo lvdisplay
     ```

  2. 检查物理卷和卷组信息

     ```bash
     sudo pvdisplay
     sudo vgdisplay
     ```

  3. 增加卷组的空间

     如果卷组没有足够的空间，你可以先添加新的物理卷到卷组中。

     ```bash
     sudo pvcreate /dev/sdX
     sudo vgextend fedora /dev/sdX
     ```

  4. 扩展逻辑卷

     ```bash
     sudo lvextend -L +10G /dev/mapper/fedora-root
     
     sudo lvextend -l +100%FREE /dev/mapper/fedora-root
     ```

  5. 扩展XFS文件系统

     ```bash
     sudo xfs_growfs /dev/mapper/fedora-root
     ```

  6. 检查结果

     ```bash
     df -h
     sudo lvdisplay
     ```

     

