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