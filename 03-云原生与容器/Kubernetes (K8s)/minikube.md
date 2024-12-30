

```bash
dnf install conntrack crictl podman crio

podman info | grep "cgroupManager"


vi /etc/containers/containers.conf
[engine]
cgroup_manager = "cgroupfs"

podman info | grep "cgroupManager"


export MINIKUBE_IMAGE_REPO="registry.cn-hangzhou.aliyuncs.com/k8s-minikube"
minikube start --driver=podman --container-runtime=containerd
```

