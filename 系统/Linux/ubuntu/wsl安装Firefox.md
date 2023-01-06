# gwsl 安装Firefox

## 准备工作

安装好 windwos wsl 版本的ubuntu

### 1. 删除本机自带的ubuntu

```shell
sudo apt remove firefox
```

### 2.添加软件源

```shell
sudo add-apt-repository ppa:mozillateam/ppa
```

### 3.更改firefox软件包的优先级

```shell
echo '
Package: *
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 1001
' | sudo tee /etc/apt/preferences.d/mozilla-firefox
```

### 4. 配置自动升级

```shell
echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' | sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox
```

### 5. 安装firefox

```shell
sudo apt install firefox
```
