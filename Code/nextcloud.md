#   NextCloud API 

## 用户API

1. 添加用户

   ```shell
   curl  -X POST -u admin:zzw123456 " http://192.168.14.184:8080/ocs/v1.php/cloud/users?format=json -d userid='Frank' -d password='frankspassword' -H 'OCS-APIRequest: true'
   ```

2. 获取用户列表

   ```shell
   # 管理员获取所有用户
   curl -u admin:zzw123456 -X GET " http://192.168.14.184:8080/ocs/v1.php/cloud/users" -H 'OCS-APIRequest: true'
   # 查询指定用户
   curl -u admin:zzw123456 -X GET " http://192.168.14.184:8080/ocs/v1.php/cloud/users?search=zzw" -H 'OCS-APIRequest: true'
   ```

3. 查询用户信息

   ```shell
   curl -u admin:zzw123456 -X GET " http://192.168.14.184:8080/ocs/v1.php/cloud/users/zzw" -H 'OCS-APIRequest: true'
   ```

4. 编辑用户信息

   ```shell
   PUT argument: key, the field to edit:
       email
       quota
       displayname
       display (deprecated use displayname instead)
       phone
       address
       website
       twitter
       password
       
   curl -u _ -X PUT " http://127.0.0.1：8080/nextcloud/ocs/v1.php/cloud/users/zzw" -d key="email" -d value="franksnewemail@example.org" -H 'OCS-APIRequest: true'
   ```

5. 禁用用户

   ```shell
     curl -u admin:zzw123456 -X PUT " http://192.168.14.184:8080/ocs/v1.php/cloud/users/zzw/disable" -H 'OCS-APIRequest: true'
   ```

6. 启用用户

   ```shell
     curl -u admin:zzw123456 -X PUT " http://192.168.14.184:8080/ocs/v1.php/cloud/users/zzw/enable" -H 'OCS-APIRequest: true'
   ```

7. 删除用户

   ```shell
        curl -u admin:zzw123456 -X DELETE " http://192.168.14.184:8080/ocs/v1.php/cloud/users/zzw" -H 'OCS-APIRequest: true'
   ```


## 用户组API

1. 获取用户组

   ```shell
    curl -u admin:zzw123456 -X POST " http://192.168.14.184:8080/ocs/v1.php/cloud/users/zzw/groups" -d groupid="newgroup" -H 'OCS-APIRequest: true'
   ```

2. 添加用户到用户组

   ```shell
     curl -u admin:zzw123456 -X POST " http://192.168.14.184:8080/ocs/v1.php/cloud/users/zzw/groups" -d groupid="newgroup" -H 'OCS-APIRequest: true'
     
   
   ```

3. 从用户组中移除用户

   ```shell
    curl -u admin:zzw123456 -X DELETE " http://192.168.14.184:8080/ocs/v1.php/cloud/users/zzw/groups" -d groupid="newgroup" -H 'OCS-APIRequest: true'
   ```

4. 将用户提升为组管理员

   ```shell
   curl -u admin:zzw123456 -X POST " http://192.168.14.184:8080/ocs/v1.php/cloud/users/zzw/subadmins"  -d groupid="group" -H 'OCS-APIRequest: true'
   ```

5. 将组管理员降级为普通用户

   ```shell
   curl -u admin:zzw123456 -X DELETE " http://192.168.14.184:8080/ocs/v1.php/cloud/users/zzw/subadmins"  -d groupid="group" -H 'OCS-APIRequest: true'
   ```

6. 获取用户管理的组

   ```shell
     curl -u admin:zzw123456 -X GET " http://192.168.14.184:8080/ocs/v1.php/cloud/users/zzw/subadmins" -H 'OCS-APIRequest: true'
   ```

7.  发送欢迎邮件

   ```shell
   curl -u admin:zzw123456 -X POST " http://192.168.14.184:8080/ocs/v1.php/cloud/users/zzw/welcome" -H 'OCS-APIRequest: true'
   ```

8. 获取所有组

   ```shell
   curl -u admin:zzw123456 -X GET " http://192.168.14.184:8080/ocs/v1.php/cloud/groups" -H 'OCS-APIRequest: true'
   ```

9. 查找指定组

   ```shell
   curl -u admin:zzw123456 -X GET " http://192.168.14.184:8080/ocs/v1.php/cloud/groups?search=admin" -H 'OCS-APIRequest: true'
   ```

10. 创建组

    ```shell
    curl -u admin:zzw123456 -X POST " http://192.168.14.184:8080/ocs/v1.php/cloud/groups"  -d groupid="newgroup" -H 'OCS-APIRequest: true'
    ```

11. 获取组成员

    ```shell
    curl -u admin:zzw123456 -X GET " http://192.168.14.184:8080/ocs/v1.php/cloud/groups/admin"  -H 'OCS-APIRequest: true'
    ```

12. 获取指定组的组管理员

    ```shell
    curl -u admin:zzw123456 -X GET " http://192.168.14.184:8080/ocs/v1.php/cloud/groups/admin/subadmins"  -H 'OCS-APIRequest: true'
    ```

13. 删除组

    ```shell
    curl -u admin:zzw123456 -X DELETE " http://192.168.14.184:8080/ocs/v1.php/cloud/groups/admin/"  -H 'OCS-APIRequest: true'
    ```


## 文件API

1. 创建目录

   ```shell
   curl -u admin:zzw123456 -X MKCOL ' http://192.168.14.184:8080/remote.php/dav/files/admin/test2/' 
   
   ```

2. 删除文件或文件夹

   ```shell
   curl -u admin:zzw123456 -X DELETE ' http://192.168.14.184:8080/remote.php/dav/files/admin/test2/' 
   
   ```

3. 上传文件

   ```shell
   curl -u admin:zzw123456 -X P ' http://192.168.14.184:8080/remote.php/dav/files/admin/test2/' 
   ```

4. 下载文件

   ```shell
   curl -u admin:zzw123456 -X GET ' http://192.168.14.184:8080remote.php/dav/files/admin/test/1.md'  -o test.md
   ```

5. 移动文件

   ```shell
   curl -u admin:admin -X MOVE " http://192.168.14.104:8080/remote.php/dav/files/admin/zzw" -H "Destination:http://192.168.14.104:8080/remote.php/dav/files/admin/ss"
   ```

6. 复制文件

   ```shell
   curl -u admin:zzw123456 -X COPY " http://192.168.14.184:8080/remote.php/dav/files/admin/ff.ff" -H "Destination:http://192.168.14.184:8080/remote.php/dav/files/admin/ss"
   ```

7. 搜索文件

   ```shell
   curl -u admin:zzw123456 -X SEARCH ' http://192.168.14.184:8080/remote.php/dav/' -H "content-Type: text/xml" --data '<?xml version="1.0" encoding="UTF-8"?>
   ```

8. 获取文件列表

   ```shell
         curl -u admin:admin -X GET "http://192.168.14.184:8080/ocs/v1.php/cloud/apps/files"  -H 'OCS-APIRequest: true'
    
   ```

## 回收站API

1. 显示回收站

   ```shell
   curl -u admin:admin -X PROPFIND "http://192.168.10.160:8080//nextcloud/remote.php/dav/trashbin/admin/trash"
   ```

   

2. 恢复回收站文件

   ```shell
   curl -u admin:admin -X MOVE " http://192.168.14.104:8080/nextcloud/remote.php/dav/trashbin/zzw/ss.php" -H "Destination:http://192.168.14.104:8080/remote.php/dav/files/admin/ss".php
   ```

3. 删除回收站文件

   ```shell
   curl -u admin:admin -X DELETE "http://192.168.14.184:8080//nextcloud/remote.php/dav/trashbin/admin/trash/ss.config"
   ```

   

4. 清空回收站

   ```shell
   curl -u admin:admin -X DELETE "http://192.168.14.184:8080//nextcloud/remote.php/dav/trashbin/admin/trash"
   ```

   

## 分享API

1. 显示分享信息列表

   ```shell
   # 显示分享信息根目录列表
   curl -u k3GeMHHPJQi9w42: -X PROPFIND http://192.168.14.104:8080/nextcloud/public.php/webdav/
   
   # 显示指定目录信息
   curl -u Pr6Ke6BnQxQzczk: -X PROPFIND http://192.168.10.130:8080/nextcloud/public.php/webdav/gg/
   ```

2. 移动文件

   ```shell
   curl -u Pr6Ke6BnQxQzczk: -X MOVE http://192.168.10.130:8080/nextcloud/public.php/webdav/ll.tx
   t -H "Destination:http://192.168.10.130:8080/nextcloud/public.php/webdav/gg/kkss.txt"
   ```

3. 复制文件

   ```shell
   curl -u Pr6Ke6BnQxQzczk: -X MOVE http://192.168.10.130:8080/nextcloud/public.php/webdav/ll.tx
   t -H "Destination:http://192.168.10.130:8080/nextcloud/public.php/webdav/gg/kkss.txt"
   ```

4. 删除文件

   ```shell
   # 删除指定目录信息
   curl -u Pr6Ke6BnQxQzczk: -X DELETE http://192.168.10.130:8080/nextcloud/public.php/webdav/gg.config
   ```

   

