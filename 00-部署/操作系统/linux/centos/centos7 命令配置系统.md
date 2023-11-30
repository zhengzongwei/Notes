# centos 7 命令配置系统

```shell

#! /bin/bash
#  Description: centos7重装系统之后初始化环境脚本
#  script_name: init_centos7.sh

# 安装软件
init_env() {
    yum -y install epel-release
    yum  -y  install  lrzsz gcc gcc-c++ make wget curl git vim* net-tools tree python-pip expect ntpdate telnet mtr unzip
}

# 关闭防火墙
dis_fwd() {
    systemctl stop firewalld  &&  systemctl disable firewalld
    setenforce 0  && sed -i '7 s/enforcing/disabled/g' /etc/selinux/config
}

# 修改主机名和固定IP地址
name_ip() {
    NETNAME=`ip ro |awk 'NR==1 {print $5}'`
    NETPATH="/etc/sysconfig/network-scripts/ifcfg-${NETNAME}"
    NETMASK="255.255.255.0"
    GATEWAY="192.168.100.1"
    DNS="114.114.114.114"
    # 修改主机名
    read -p "请输入要修改的主机名: " NAME
    /usr/bin/hostnamectl set-hostname ${NAME}

    # 修改IP地址
    read -p "请输入要修改的IP地址: " IP
    sed -i '/ONBOOT/ s/no/yes/g' ${NETPATH}
    sed -i '/BOOTPROTO/ s/dhcp/none/g' ${NETPATH}
    echo -e "IPADDR=${IP}\nNETMASK=${NETMASK}\nGATEWAY=${GATEWAY}\nDNS1=${DNS}" >> ${NETPATH}
    clear; echo "------------------------查看IP地址配置-----------------------------"
    cat ${NETPATH}

    # 重启网卡
    read -p "如果确认无误，输入y表示立即重启网卡，输入任意键退出: " SURE
    S=`echo ${SURE} |tr 'A-Z' 'a-z'`
    if [ ${S} == 'y' ];then 
        echo "正在重启网络使修改的IP生效，请用新IP地址尝试登陆……"
        systemctl restart network
    else
        echo "还没有重启网络，修改的IP地址未生效，请手动重启使其生效"
    fi
}


main() {
    set -e
    echo -e "\033[34m  1.安装centos7常用软件……  \033[0m"
    init_env
    echo -e "\033[34m  2.永久关闭防火墙和selinux服务……  \033[0m"
    dis_fwd
    echo -e "\033[34m  3.开始修改主机名称和IP地址为固定IP地址……  \033[0m"
    name_ip
}
main
```
