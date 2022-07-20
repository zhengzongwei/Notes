# Ubuntu 配置

## 更换默认源

1. 备份配置文件

   ```shell
   sudo cp -a /etc/apt/sources.list /etc/apt/sources.list.bak
   ```

2. 修改配置文件

   ```shell
   sudo sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
   sudo sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
   ```

3. 更新索引

   ```shell
   apt-get update
   ```

   

