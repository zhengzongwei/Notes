# Linux 基础运维

1. 非root用户免密

   ```shell
   vi /etc/sudoers
   your_username ALL=(ALL) NOPASSWD:ALL
   ```

   

2. 非root用户添加docker权限

   ```shell
   sudo usermod -aG docker user_name
   newgrp docker
   
   sudo systemctl restart docker
   ```


3. /var/run 下文件被删除

   近期发现在重启宿主机后，有些服务报错起不来，查看报错发现是由于 /var/run/ 下有个目录不存在

   原因：由于 /var/run 是一个tmpfs 内存文件系统，在机器重启后，文件夹会丢失，导致服务起不来

   解决：

   ```shell
   文件可以放置在/etc/tmpfiles.d、/run/tmpfiles.d或/usr/lib/tmpfiles.d中
   
   创建相关的服务文件
   
   # d代表目录，旁边是路径，权限，所有者和组。重启，会在/var/run/目录下创建hdfs-sockets
   d /var/run/hdfs-sockets 0755 root root
   
   
   echo -e "d /var/run/neutron 0755 root root -" > /usr/lib/tmpfiles.d/neutron.conf
   ```

   