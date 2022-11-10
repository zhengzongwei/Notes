# NVIDIA A10 GPU适配

## 查看BIOS 相关配置是否已启用

- VT-D

- SRV_IO

  ![image-20221108180806277](./images/image-20221108180806277-8046578.png)



##  内核加载ko文件

将 ko文件复制到 `/lib/modules/3.10.0-1160.45.1.el7.x86_64/kernel/drivers/pci`

重启主机





