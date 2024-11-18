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
