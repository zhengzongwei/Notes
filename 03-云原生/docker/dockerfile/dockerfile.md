## 系统镜像

### ubuntu

#### dockerfile

```dockerfile
FROM ubuntu
MAINTAINER zhengzongwei<zhengzongwei@foxmail.com>

WORKDIR /root

# 更换源
RUN cp -a /etc/apt/sources.list /etc/apt/sources.list.bak \
  && sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list \
  && sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list \
  && apt-get -y update \
  # 
  && DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata \
  && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/timezone && echo 'Asia/Shanghai' >/etc/timezone \
  && dpkg-reconfigure -f noninteractive tzdata \
  # 安装软件
  && DEBIAN_FRONTEND=noninteractive apt-get -y install vim sudo golang git wget curl

# clean 
RUN rm -rf /root/var \
  && rm -rf /var/cache/apt

```

### debian
#### dockerfile

```dockerfile
FROM debian:11
MAINTAINER zhengzongwei<zhengzongwei@foxmail.com>

RUN cp -a /etc/apt/sources.list /etc/apt/sources.list.bak \
  && sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
  && sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list
```



### openeuler

#### dockerfile

```dockerfile
FROM openeuler/openeuler:latest
MAINTAINER zhengzongwei<zhengzongwei@foxmail.com>

WORKDIR /

# RUN dnf update  -y \
#     dnf install sudo unzip golang gcc g++ git vim tmux -y

# 配置文件
RUN sed -i "s@TMOUT=300@TMOUT=0@g" /etc/bashrc \
  && source ~/.bashrc

# clean 
RUN dnf clean all
# clean 
RUN rm -rf /root/var \
  && rm -rf /var/cache/apt



# FROM openeuler/openeuler:latest
# MAINTAINER zhengzongwei<zhengzongwei@foxmail.com>

# WORKDIR /

# RUN dnf update  -y \
#     dnf install sudo unzip golang gcc g++ git vim tmux -y

# # clean 
# RUN rm -rf /root/var \
#     && rm -rf /var/cache/apt
```

## 应用镜像

### gitea

#### dockerfile

```dockerfile
version: "3"

networks:
gitea:
external: false

services:
serveer:
image: gitea/gitea:1.17.0
container_name: gitea
environment:
- USER_UID=1000
- USER_GID=1000
restart: always
networks:
- gitea
volumes:
- ./gitea:/data
- /etc/timezone:/etc/timezone:ro
- /etc/localtime:/etc/localtime:ro
ports:
- "3000:3000"
- "222:22"


# # Edit `docker-compose.yml` to update the version, if you have one specified
# Pull new images
# docker-compose pull
# Start a new container, automatically removes old one
# docker-compose up -d

```

### mariadb

#### dockerfile

```dockerfile
ARG UBUNTU_VERSION

FROM ubuntu:$UBUNTU_VERSION
MAINTAINER zhengzongwei<zhengzongwei@foxmail.com>


# 更换源
RUN cp -a /etc/apt/sources.list /etc/apt/sources.list.bak \
  && sed -i "s@http://.*ports.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list \
  && sed -i "s@http://.*ports.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list \
  && apt-get -y update \
  && DEBIAN_FRONTEND=noninteractive apt-get -y install mariadb-server




VOLUME ["/etc/mysql", "/var/lib/mysql"]

EXPOSE 3306

HEALTHCHECK --start-period=5m \
  CMD mariadb -e 'SELECT @@datadir;' || exit 1

CMD ["mysqld"]


# docker build -f ./mariadb.dockerfile  --build-arg UBUNTU_VERSION=22.04 . -t mariadb:develop
```

#### docker-compose

```dockerfile
version: '3.1'
services:
mariadb:
image: mariadb:latest
container_name: "db"
restart: always
environment:
MYSQL_USER: "root"
MYSQL_PASSWORD: "zhengzongwei"
MYSQL_ROOT_PASSWORD: "zhengzongwei"
TZ: "Asia/Shanghai"
ports:
- "3306:3306"
volumes:
- ./data:/var/lib/mysql
- ./log:/var/log/mysql
# docker-compose up -d
```



