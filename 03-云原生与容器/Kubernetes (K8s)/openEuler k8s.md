# openEuler K8S部署

## 环境信息

## 系统配置

```
# 关闭防火墙
systemctl stop firewalld
systemctl disable firewalld


# vi /etc/sysctl.conf
net.ipv4.ip_forward = 1


# 关闭 selinux
sed -i 's/enforcing/disabled/' /etc/selinux/config 
setenforce 0


# 关闭swap
swapoff -a # 临时关闭
sed -ri 's/.*swap.*/#&/' /etc/fstab  #永久关闭

# 修改hostname
hostnamectl set-hostname 名字

# 桥接的IPv4流量传递到iptables的链
 cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

sysctl -p

# 配置源
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.32/rpm/repodata/repomd.xml.key
EOF

# 内核模块加载
modprobe overlay
modprobe br_netfilter
echo -e overlay\\nbr_netfilter > /etc/modules-load.d/k8s.conf


# 管理节点
dnf -y install kubectl kubeadm kubelet cri-tools iproute-tc container-selinux


echo "KUBELET_CGROUP_ARGS=--cgroup-driver=systemd" >> /etc/sysconfig/kubelet
# 二选其一 cri-o 或者 containerd
dnf install cri-o
# dnf install containerd

# crio
vi /etc/sysconfig/crio
CRIO_CONFIG_OPTIONS="--config /etc/crio/crio.conf"
sudo systemctl daemon-reload


crio config --default > /etc/crio/crio.conf

vi /etc/crio/crio.conf


# containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml

# 修改containerd配置
$ sudo vi /etc/containerd/config.toml
# 1、找到[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]并将值更改SystemdCgroup为true
# 2、找到sandbox_image = "k8s.gcr.io/pause:3.6"并改为sandbox_image = "registry.aliyuncs.com/google_containers/pause:3.6"


systemctl restart containerd


systemctl enable --now crio
systemctl enable --now containerd
systemctl enable --now kubelet


kubeadm init \
--apiserver-advertise-address=10.211.55.51 \
--image-repository registry.aliyuncs.com/google_containers \
--kubernetes-version v1.32.0 \
--pod-network-cidr=10.244.0.0/16


  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

vi /etc/containerd/config.toml
      [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."docker.io"]
          endpoint = ["https://docker.1ms.run","https://docker.wanpeng.top"]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."gcr.io"]
          endpoint = ["https://gcr.m.daocloud.io"]
        [plugins."io.containerd.grpc.v1.cri".registry.mirrors."quay.io"]
          endpoint = ["https://quay-mirror.qiniu.com"]
systemctl restart containerd


kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml


helm-v3.16.4-linux-arm64.tar.gz

cp helm /usr/local/bin/


# dashboard
# 添加源信息
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/

helm install kubernetes-dashboard ./ --create-namespace --namespace kube-dashboard

helm uninstall kubernetes-dashboard
# 默认参数安装
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kube-dashboard

# 我的集群使用默认参数安装 kubernetes-dashboard-kong 出现异常 8444 端口占用
# 使用下面的命令进行安装，在安装时关闭kong.tls功能
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --namespace kube-system --set kong.admin.tls.enabled=false


kubectl create serviceaccount -n kube-dashboard admin-user

[root@ctrl ~]# vi rbac.yml
# create new
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-dashboard
  
kubectl apply -f rbac.yml
kubectl -n kubernetes-dashboard create token admin-user


# run kube-proxy
[root@ctrl ~]# kubectl proxy
Starting to serve on 127.0.0.1:8001
# if access from other client hosts, not from Manage node local, set port-forwarding
[root@ctrl ~]# kubectl port-forward -n kube-dashboard svc/kubernetes-dashboard-kong-proxy --address 0.0.0.0 443:443
Forwarding from 0.0.0.0:443 -> 8443

```



## 部署

### 安装kubctl

```bash
dnf install install cri-o
dnf -y install kubectl kubeadm kubelet cri-tools iproute-tc container-selinux

dnf install containerd

systemctl enable kubelet

systemctl start containerd
systemctl enable containerd

vi /etc/crictl.yaml

runtime-endpoint: unix:///run/containerd/containerd.sock

kubeadm init \
--apiserver-advertise-address=10.211.55.51 \
--image-repository registry.aliyuncs.com/google_containers \
--kubernetes-version v1.32.0 \
--pod-network-cidr=10.244.0.0/16


mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
  
kubectl taint nodes --all node-role.kubernetes.io/control-plane-

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

sed -i 's|docker.io|swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io|g' kube-flannel.yml

kubectl rollout restart daemonset kube-flannel-ds -n kube-flannel

kubectl rollout restart deployment coredns -n kube-system
```

## 参考链接

1. [kubeadm部署Kubernetes（k8s）完整版详细教程 - 南宫乘风 - 博客园](https://www.cnblogs.com/heian99/p/12173599.html)





```bash
认证地址：OpenStack管理平台的认证地址，如http://host:port/v3。
账号：OpenStack平台的管理员用户名，如admin。
密码：OpenStack平台管理员用户的密码。
项目：OpenStack平台上的项目，如admin项目。
Domain Name：OpenStack平台上的Domain name，如default。


认证地址 http://106.54.39.146:5000/v3
账号：OpenStack平台的管理员用户名 admin
密码：OpenStack平台管理员用户的密码 admin
项目:	OpenStack平台上的项目 Default
Domain Name：OpenStack平台上的Domain name,Default

示例:
curl --location --request POST 'http://106.54.39.146:5000/v3/auth/tokens' \
--header 'Content-Type: application/json' \
--data '{
  "auth": {
    "identity": {
      "methods": ["password"],
      "password": {
        "user": {
          "name": "admin",
          "domain": { "name": "Default" },
          "password": "admin"
        }
      }
    },
    "scope": {
      "project": {
        "name": "admin",
        "domain": { "name": "Default" }
      }
    }
  }
}'

.admin-openrc

export OS_PROJECT_DOMAIN_NAME=Default
export OS_USER_DOMAIN_NAME=Default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=admin
export OS_AUTH_URL=http://controller-1:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
```

