# firewall-cmd

> Linux上新用的防火墙软件，跟iptables差不多的工具

## firewall 开放/关闭端口

```bash
firewall-cmd --zone=public --add-port=15672/tcp --permanent

firewall-cmd --zone=public --query-port=15672

firewall-cmd --zone=public --remove-port=15672/tcp

# 批量放开/或关闭端口
批量开放或关闭端口：
firewall-cmd --zone=public --add-port=40000-45000/tcp --permanent #批量开放端口，打开从40000到45000之间的所有端口
firewall-cmd --zone=public --list-ports #查看系统所有开放的端口
firewall-cmd --zone=public --remove-port=40000-45000/tcp --permanent #批量关闭端口，关闭从40000到45000之间的所有端口

sudo firewall-cmd --reload
```

