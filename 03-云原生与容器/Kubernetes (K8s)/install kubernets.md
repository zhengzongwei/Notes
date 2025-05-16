# kubernets 部署指南

> 本文档是 zhengzongwei 编写 openEuler 24.03 LTS SP1的kubernets部署指南

## 环境准备

| 主机名 |  role  | IP地址 | CPU  | 内存 | 组件 |
| :----: | :----: | :--: | :--: | :--: | :--: |
| k8s-01 | master |  192.168.248.137  |  4  | 4 | kubeadm, kubelet, kubectl, containerd |
| k8s-02 | node01 | 192.168.248.138 |  4   | 8 | kubeadm, kubelet, kubectl, containerd |
| k8s-03 | node02 | 192.168.248.139 |  4   | 8 | kubeadm, kubelet, kubectl, containerd |

## 环境配置

### 0.hostname

```shell
 hostnamectl set-hostname k8s-con-01
 
 vi /etc/hosts
 
```



### 1. 关闭SeLinux

```shell
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=disabled/' /etc/selinux/config
```

### 2. 关闭防火墙

```shell
systemctl disable --now firewalld
```

### 3. 禁用swap

```shell
swapoff -a

sed -ri 's/.*swap.*/#&/' /etc/fstab 
```

### 4. 修改内核模块

```shell
#开启内核路由转发
sed -i 's/net.ipv4.ip_forward=0/net.ipv4.ip_forward=1/g' /etc/sysctl.conf

cat <<EOF > /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

# sysctl --system
 
# 内核模块加载
modprobe overlay
modprobe br_netfilter
echo -e overlay\\nbr_netfilter > /etc/modules-load.d/k8s.conf

# modprobe br_netfilter
# lsmod | grep br_netfilter
```

### 5. 配置k8s repo

```shell
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/repodata/repomd.xml.key
EOF
```





## 安装k8s

```shell
dnf -y install kubelet kubeadm kubectl

# 查看需要的镜像版本
kubeadm config images list

```

## 安装 containerd

```shell
dnf install containerd containernetworking-plugins

mkdir -p /opt/cni/bin
cp /usr/libexec/cni/* /opt/cni/bin/

# 生成容器配置文件
containerd config default  >> /etc/containerd/config.toml


vi /etc/containerd/config.toml

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  ...
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
  
    SystemdCgroup = true
    
    
[plugins."io.containerd.grpc.v1.cri"]
  sandbox_image = "registry.aliyuncs.com/google_containers/pause:3.10"
  
  
  systemctl start containerd
```

## 初始化k8s和网络

```shell
kubeadm init \
--apiserver-advertise-address=192.168.248.137 \
--image-repository registry.aliyuncs.com/google_containers \
--kubernetes-version v1.32.3 \
--pod-network-cidr=10.100.0.0/16 --service-cidr=10.1.0.0/16


mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

- 安装 flannel

  github https://github.com/flannel-io/flannel

  yaml文件下载  https://github.com/flannel-io/flannel/releases/download/v0.26.6/kube-flannel.yml

  修改 net-conf.json

  网段和--pod-network-cidr 对应

## Worker 节点加入集群

在控制平面执行

```shell
kubeadm token create --print-join-command
```

在worker节点执行控制平面的命令

```shell
kubeadm join 192.168.248.137:6443 --token vqj8ea.acvu39y33mbd33hz --discovery-token-ca-cert-hash sha256:5ca15322edb9cf23245d956ddb079f44c531490d81a6926d8c54c5b6b3b3d667
```





## HELM安装

github [Releases · helm/helm](https://github.com/helm/helm/releases)

## 安装k8s-dashboard

单节点测试 

```shell
[root@k8s-con-01 ~]# kubectl describe nodes | grep Taints
Taints:             node-role.kubernetes.io/control-plane:NoSchedule

kubectl taint nodes --all node-role.kubernetes.io/control-plane-
```



```shell
wget https://github.com/kubernetes/dashboard/releases/download/kubernetes-dashboard-7.11.1/kubernetes-dashboard-7.11.1.tgz

helm install kubernetes-dashboard ./kubernetes-dashboard-7.11.1.tgz \
  --namespace kubernetes-dashboard \
  --create-namespace
```

## 安装kubevirt

- 获取当前kubevirt最新版本

  ```shell
  KUBEVIRT_VERSION=$(curl -s https://api.github.com/repos/kubevirt/kubevirt/releases/latest | jq -r .tag_name)
  
  KUBEVIRT_VERSION=v1.5.0
  
  
  
  wget https://github.com/kubevirt/kubevirt/releases/download/${KUBEVIRT_VERSION}/kubevirt-operator.yaml
  
  wget https://github.com/kubevirt/kubevirt/releases/download/${KUBEVIRT_VERSION}/kubevirt-cr.yaml
  ```

  - 安装 virtctl

    ```shell
    wget -O virtctl https://github.com/kubevirt/kubevirt/releases/download/${KUBEVIRT_VERSION}/virtctl-${KUBEVIRT_VERSION}-linux-amd64
    
    chmod +x virtctl
    
    sudo mv virtctl /usr/local/bin/
    
    virtctl version
    ```

## 问题解决

1. 默认k8s的master节点是不能跑pod的业务，需要执行以下命令解除限制

   ```shell
   # kubectl taint nodes --all node-role.kubernetes.io/master-s
   kubectl taint node k8s-2 node-role.kubernetes.io/master-
   ```

   

## 参考链接

1. kubevirt安装参考 [KubeVirt 02：部署 KubeVirt – 小菜园](https://www.imxcai.com/k8s/kubevirt/kubevirt-02-deploy-kubevirt.html)
2. [KubeVirt 03：部署一个简单的 VM – 小菜园](https://www.imxcai.com/k8s/kubevirt/kubevirt-03-deploy-simple-vm.html)





`````
openstack image create --name=centos-76-fix-repo --container-format=ovf --disk-format=qcow2 --file=centos-76-fix-repo --is-public=True --property os_version=centos-7.6 --min-disk=20 --min-ram=0 --property is_online=True --property invisible=0 --property is_npe=true --property image_user_defined_category=common --progress --property image_openstack_defined_live_upgrade=true
`````

