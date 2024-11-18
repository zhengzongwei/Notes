#!/usr/bin/env bash
# 新系统一键配置脚本



msg() {
  printf '%b\n' "$1" >&2
}

tips() {
  msg "\33[36m[*]\33[0m ${1}${2}"
}

success() {
  msg "\33[32m[✔]\33[0m ${1}${2}"
}

error() {
  msg "\33[31m[✘]\33[0m ${1}${2}"
  exit 1
}


check_network_status(){
    # 超时时间
    timeout=5
    # 目标域名
    target=www.baidu.com
    # 获取响应状态码
    status_code=`curl -I -s --connect-timeout $timeout $target -w %{http_code} | tail -n1`
    if [ "x$status_code" = "x200" ]; then
        success "网络正常"
    else
        error "网络不正常，请检查网络连接！"
    fi
}

check_os_version(){
    # 检查当前执行的系统版本

    if [ -f /etc/os-release ];then
        source /etc/os-release
    fi

    if [[ $ID =~ "openEuler" || $PRETTY_NAME =~ "openEuler" ]];then
        tips "this system is $ID"
    elif [[ $lsb =~ "Debian" || $PRETTY_NAME =~ "Debian" ]]; then
        echo "debian_enable_cron"   kill_unknown_firewall
    elif [[ $lsb =~ "SUSE" || $PRETTY_NAME =~ "SUSE" ]]; then
        echo "suse_enable_cron"     kill_unknown_firewall
    elif [[ $lsb =~ "NeoKylin" || $PRETTY_NAME =~ "NeoKylin" ]]; then
        echo "中标麒麟：redhat_enable_cron"   kill_redhat_firewall
    elif [[ $lsb =~ "Kylin" || $PRETTY_NAME =~ "Kylin" ]]; then
        echo "银河麒麟：ubuntu_enable_cron"   kill_ubuntu_firewall
    else
        echo "Warn: Bypass system check"
    fi

}

function update_ubutnu_mirrors(){
    # 通过系统版本配置软件源
    sudo cp -a /etc/apt/sources.list /etc/apt/sources.list.bak

    sudo sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
    sudo sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list

    apt-get update

    # arm 64
    sudo sed -i 's@//.*ports.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list
}

function update_debian_mirrors(){
    cp -a /etc/apt/sources.list /etc/apt/sources.list.bak

    sed -i "s@http://ftp.debian.org@https://repo.huaweicloud.com@g" /etc/apt/sources.list
    sed -i "s@http://security.debian.org@https://repo.huaweicloud.com@g" /etc/apt/sources.list
    apt-get install apt-transport-https ca-certificates
    # if [ $? -]
    apt-get update

}

function update_centos_mirrors(){
    cp -a /etc/apt/sources.list /etc/apt/sources.list.bak

    sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
    sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list

}

function config_pip_mirrors(){
# 配置 pip源
pip_config="
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
"
mkdir -p ~/.pip/
    tee > ~/.pip/pip.conf <<EOF
$pip_config
EOF

}

function config_golang_mirror(){

}

function main(){
    # 入口函数


    check_network_status
    check_os_version
}

main