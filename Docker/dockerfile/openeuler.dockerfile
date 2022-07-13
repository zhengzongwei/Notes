FROM openeuler/openeuler:latest
MAINTAINER zhengzongwei<zhengzongwei@foxmail.com>

WORKDIR /

RUN dnf update  -y \
    dnf install sudo unzip golang gcc g++ git vim tmux -y

# clean 
RUN rm -rf /root/var \
    && rm -rf /var/cache/apt