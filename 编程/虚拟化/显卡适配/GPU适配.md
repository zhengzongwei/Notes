# NVIDIA A10 GPU适配

## 查看BIOS 相关配置是否已启用

- VT-D

- SRV_IO

  ![image-20221108180806277](./images/image-20221108180806277-8046578.png)



##  内核加载ko文件

将 ko文件复制到 `/lib/modules/3.10.0-1160.45.1.el7.x86_64/kernel/drivers/pci`

重启主机





```shell


    <hostdev mode='subsystem' type='mdev' managed='yes' model='vfio-pci' display='off'>
      <source>
        <address uuid='3d355e58-8744-4fc3-8bfb-7001648b4a9a'/>
      </source>
      <alias name='hostdev0'/>
    </hostdev>

    <hostdev mode='subsystem' type='mdev' managed='yes' model='vfio-pci' display='off'>
      <source>
        <address uuid='3d8cebfd-7d49-48d7-b2b2-285387d775ad'/>
      </source>
    </hostdev>

0fd6c6e9-b590-409a-b4b7-d22a733cb67e

3d8cebfd-7d49-48d7-b2b2-285387d775ad

3d355e58-8744-4fc3-8bfb-7001648b4a9a
```





