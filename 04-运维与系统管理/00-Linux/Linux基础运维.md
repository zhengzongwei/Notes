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

   