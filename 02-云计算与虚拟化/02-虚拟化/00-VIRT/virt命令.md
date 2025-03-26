# virt-tools命令指南

## 背景

本文档介绍的是`libguestfs`和`virt-tools`的相关命令，适用于 KVM/QEMU、Xen、VMware等虚拟化环境

## 主要工具分类

|        **类别**        |                         **相关命令**                         |               **用途**               |
| :--------------------: | :----------------------------------------------------------: | :----------------------------------: |
|   **虚拟机磁盘操作**   | `virt-df`, `virt-cat`, `virt-edit`, `virt-ls`, `virt-copy-in`, `virt-copy-out` |       查看/修改虚拟机磁盘文件        |
|  **虚拟机创建/转换**   | `virt-builder`, `virt-v2v`, `virt-p2v-make-*`, `virt-resize`, `virt-sparsify` |        构建、转换、调整虚拟机        |
|  **虚拟机调试/修复**   | `virt-rescue`, `virt-inspector`, `virt-log`, `virt-host-validate` |     进入虚拟机救援模式、检查日志     |
|  **虚拟机优化/清理**   |       `virt-sysprep`, `virt-sparsify`, `virt-make-fs`        |         清理、压缩、优化磁盘         |
| **Windows 虚拟机工具** |           `virt-win-reg`, `virt-v2v-copy-to-local`           | 操作 Windows 注册表、转换 Windows VM |
|      **格式验证**      | `virt-pki-validate`, `virt-xml-validate`, `virt-index-validate` |         检查 XML、证书等格式         |

## 常用命令详解

1. 查看/修改虚拟机磁盘

   |        命令         |          用途          |                     示例                      |
   | :-----------------: | :--------------------: | :-------------------------------------------: |
   |    **`virt-df`**    | 查看虚拟机磁盘使用情况 | `virt-df -h /var/lib/libvirt/images/vm.qcow2` |
   |   **`virt-cat`**    |   查看虚拟机内的文件   |        `virt-cat -d myvm /etc/passwd`         |
   |   **`virt-edit`**   |   编辑虚拟机内的文件   |        `virt-edit -d myvm /etc/fstab`         |
   |    **`virt-ls`**    |   列出虚拟机内的文件   |        `virt-ls -l -d myvm /var/log/`         |
   | **`virt-copy-in`**  |    向虚拟机复制文件    |  `virt-copy-in -d myvm file.txt /home/user/`  |
   | **`virt-copy-out`** |    从虚拟机复制文件    |  `virt-copy-out -d myvm /var/log/messages .`  |

2. 创建/转换虚拟机

   |        命令         |             用途              |                             示例                             |
   | :-----------------: | :---------------------------: | :----------------------------------------------------------: |
   | **`virt-builder`**  |        快速构建虚拟机         |    `virt-builder fedora-38 -o fedora.img --format qcow2`     |
   |   **`virt-v2v`**    | 转换虚拟机（如 VMware → KVM） | `virt-v2v -i ova vmware.ova -o qemu -os /var/lib/libvirt/images/` |
   |  **`virt-resize`**  |      调整虚拟机磁盘大小       |    `virt-resize --expand /dev/sda1 input.img output.img`     |
   | **`virt-sparsify`** |   优化磁盘（减少占用空间）    |     `virt-sparsify --compress vm.qcow2 vm-sparse.qcow2`      |

3. 调试/修复虚拟机

   |           命令           |                用途                |             示例             |
   | :----------------------: | :--------------------------------: | :--------------------------: |
   |    **`virt-rescue`**     | 进入虚拟机救援模式（类似 Live CD） |  `virt-rescue -a vm.qcow2`   |
   |   **`virt-inspector`**   |    检查虚拟机信息（OS、分区等）    | `virt-inspector -a vm.qcow2` |
   |      **`virt-log`**      |           查看虚拟机日志           |      `virt-log -d myvm`      |
   | **`virt-host-validate`** |        检查宿主机虚拟化支持        |  `virt-host-validate qemu`   |

4. 清理/优化虚拟机

  |        命令        |                用途                |                     示例                      |
  | :----------------: | :--------------------------------: | :-------------------------------------------: |
  | **`virt-sysprep`** | 清理虚拟机（删除缓存、历史记录等） |            `virt-sysprep -d myvm`             |
  | **`virt-make-fs`** |        创建虚拟磁盘文件系统        | `virt-make-fs --type=ext4 disk.img disk.ext4` |

5. Windows虚拟机专用工具

   |             命令             |            用途            |                        示例                        |
   | :--------------------------: | :------------------------: | :------------------------------------------------: |
   |      **`virt-win-reg`**      |    修改 Windows 注册表     |    `virt-win-reg --merge winvm.reg win10.qcow2`    |
   | **`virt-v2v-copy-to-local`** | 转换远程 Windows VM 到本地 | `virt-v2v-copy-to-local -ic vpx://user@esxi/win10` |

## 参考链接

1. https://libguestfs.org
2. https://www.virt-tools.org