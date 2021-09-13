# NextCloud API 

## 分享

1. 显示分享信息列表

   ```shell
   # 显示分享信息根目录列表
   curl -u Pr6Ke6BnQxQzczk: -X PROPFIND http://192.168.10.130:8080/nextcloud/public.php/webdav/
   
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

   

