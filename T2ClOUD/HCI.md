

## 部署

-   新安装HCI包

```shell
hc*i>ZSmm@123

yum -y remove  agent falcon-plus-cloud-agent

# 解除安全加固 
bash /opt/kolla-ansible-deploy/kolla-ansible/tools/rhel_unsec2021_6-2_LL.sh
```



## 更新证书命令

```
ssh 192.168.103.17
source /usr/loy/license-server/venv/bin/activate
cd /usr/loy/gen-license/
./gen-license 4898-0e81-9ace-b5a6-cb19-2a25-c7d2-9725 --days 365 --size 20480000 --num 6
下载证书，更新证书

192.168.103.17:8888
```