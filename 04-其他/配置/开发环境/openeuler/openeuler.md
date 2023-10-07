# openeuler 系统配置

## 修改dnf 配置文件

```shell
/etc/dnf/dnf.conf
[main]
gpgcheck=1
installonly_limit=3
clean_requirements_on_remove=True
best=True
skip_if_unavailable=False
keepcache=1


dnf -y upgrade --downloadonly --downloaddir=.
```

## 配置rpm编译环境

```shell
dnf install rpmdevtools*
```

## 环境初始化

```shell
#!/usr/bin/env bash
# 环境初始化设置

USER_LIST=("zhengzongwei" "nieantai" "hujinyong")

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

create_user(){
  for USER in ${USER_LIST[*]};do
    tips "create user ${USER}"

    useradd -d /home/$USER -s /bin/bash -m $USER
    echo "$USER:$USER" | chpasswd
    success "create user ${USER} success!"
  done

}

add_docker_group(){
    for USER in ${USER_LIST[*]};do
        tips "add user ${USER} to docker group"
        gpasswd -a $USER docker
        success "add user ${USER} to docker group success!"
    done
    newgrp docker
}

main(){
    create_user
    add_docker_group
}

main


```

## 系统升级配置

```shell
# 22.03-LTS 升级到 22.03-LTS-SP2
sed -i 's/22.03-LTS/22.03-LTS-SP2/g' /etc/yum.repos.d/openEuler.repo

# 22.03-LTS-SP1 升级到 22.03-LTS-SP2
sed -i 's/22.03-LTS-SP1/22.03-LTS-SP2/g' /etc/yum.repos.d/openEuler.repo

dnf update -y
```

## vscode ssh-remote

dnf install tar vim tmux

- 修改ssh配置文件

  ```bash
  vim /etc/ssh/sshd_config
  
  AllowTcpForwarding yes
  AllowAgentForwarding yes
  GatewayPorts yes
  ```

  重启 ssh 服务 `systemctl restart sshd`

