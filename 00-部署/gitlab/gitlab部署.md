# gitlab部署

## 环境信息

- 系统 `openEuler release 22.03 (LTS-SP2)`
- 内核 `5.10.0-153.28.0.105.oe2203sp2.aarch64`
- 配置  4C4G

## 软件编译

由于gitlab未提供aarch的docker镜像，需要自己手动编译一下，具体可以参考 [zengxs/gitlab-arm64: GitLab docker image (CE & EE) for arm64 (github.com)](https://github.com/zengxs/gitlab-arm64)

### 部署docker

```bash
dnf install docker.io

# 创建docker 组
sudo groupadd docker

# 将当前用户加入docker组
# sudo usermod -aG docker ${USER}
sudo gpasswd -a ${USER} docker

# 刷新docker组
newgrp docker
```

## 配置gitlab

### 设置gitlab工作目录

```bash
export GITLAB_HOME=/opt/gitlab
```

```bash
sudo docker run --detach \
  --hostname git.dev.com \
  --publish 443:443 --publish 80:80 --publish 22:22 \
  --name gitlab \
  --restart always \
  --volume $GITLAB_HOME/config:/etc/gitlab \
  --volume $GITLAB_HOME/logs:/var/log/gitlab \
  --volume $GITLAB_HOME/data:/var/opt/gitlab \
  --shm-size 256m \
  gitlab-ce:16.4.1-ce.0
```





## 参考链接

1. 部署gitlab [GitLab Docker images | GitLab](https://docs.gitlab.com/ee/install/docker.html)





