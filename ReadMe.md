```shell
.
├── 00-部署
│   ├── gitlab
│   │   └── gitlab部署.md
│   ├── jellyfin
│   │   └── jellyfin.md
│   ├── proxmox
│   │   └── proxmox.md
│   └── 操作系统
│       ├── esxi
│       │   └── esxi8.md
│       ├── linux
│       │   ├── arch
│       │   │   ├── arch
│       │   │   │   └── images
│       │   │   │       ├── arch-2023-02-04-12-22-24.png
│       │   │   │       ├── arch-2023-02-04-12-25-00.png
│       │   │   │       ├── arch-2023-02-04-16-04-59.png
│       │   │   │       ├── arch-2023-02-04-16-20-27.png
│       │   │   │       ├── arch-2023-02-04-16-21-56.png
│       │   │   │       ├── arch-2023-02-04-16-25-41-1675499259666-7.png
│       │   │   │       ├── arch-2023-02-04-16-25-41.png
│       │   │   │       ├── arch-2023-02-04-16-27-31.png
│       │   │   │       ├── arch-2023-02-04-16-33-07.png
│       │   │   │       └── image-20230204161742384.png
│       │   │   ├── arch (bios)
│       │   │   │   └── images
│       │   │   │       └── arch-0204-2023-02-04-21-00-09.png
│       │   │   └── arch (bios).md
│       │   ├── centos
│       │   │   ├── centos7 命令配置系统.md
│       │   │   └── 挂载ISO镜像作为本地yum源.md
│       │   └── debian
│       │       └── debian安装指南.md
│       └── 树莓派
│           ├── images
│           │   └── 烧录系统.png
│           └── 树莓派安装openueler.md
├── 01-开发与编程
│   ├── git
│   │   ├── git 项目配置.md
│   │   ├── github不能pull.md
│   │   ├── git提交规范.md
│   │   └── git操作.md
│   ├── golang
│   │   ├── gin.md
│   │   ├── go操作.md
│   │   └── go规范.md
│   ├── javascript
│   │   ├── js.md
│   │   └── vite+element3.md
│   ├── kernel编译
│   │   └── 内核
│   │       ├── Kernel
│   │       │   ├── kernel 构建指南.md
│   │       │   ├── kernel开发指南.md
│   │       │   └── kernel编译指南.md
│   │       └── 编译内核.md
│   ├── python
│   │   ├── Python定时器归纳.md
│   │   ├── fastapi.md
│   │   ├── 单例模式.md
│   │   ├── 归档
│   │   │   ├── django
│   │   │   │   ├── DJANGO.md
│   │   │   │   ├── REST.images
│   │   │   │   │   ├── 前后端不分离.png
│   │   │   │   │   └── 前后端分离.png
│   │   │   │   └── REST.md
│   │   │   ├── flask
│   │   │   │   ├── Flask_数据库_.md
│   │   │   │   ├── Flask模板_.md
│   │   │   │   ├── Flask环境搭建_.md
│   │   │   │   ├── Flask视图_.images
│   │   │   │   │   ├── JSON-4759866.png
│   │   │   │   │   └── JSON.png
│   │   │   │   ├── Flask视图_.md
│   │   │   │   ├── cookie和session区别.md
│   │   │   │   ├── flask_session总结_.md
│   │   │   │   ├── 项目流程.md
│   │   │   │   └── 项目部署的步骤.md
│   │   │   └── 基础
│   │   │       ├── 代码规范.md
│   │   │       ├── 列表List.md
│   │   │       ├── 列表、字典、集合.md
│   │   │       ├── 字符串Str.md
│   │   │       ├── 正则表达式.md
│   │   │       └── 面向对象.md
│   │   ├── 模块
│   │   │   ├── PySnooper
│   │   │   │   ├── PySnooper-1.2.0-py2.py3-none-any.whl
│   │   │   │   └── PySnooper-1.2.0.tar.gz
│   │   │   ├── click
│   │   │   │   └── click.md
│   │   │   └── terminaltables.md
│   │   ├── 装饰器.md
│   │   └── 远程调试.md
│   ├── shell
│   │   ├── create_user.md
│   │   ├── file.md
│   │   ├── pip.sh
│   │   ├── pipconf.sh
│   │   ├── system init.md
│   │   └── system_config.sh
│   └── swift
│       └── String.swift
├── 02-云计算与虚拟化
│   ├── 01-基础服务
│   │   ├── DNS
│   │   │   └── DNS解析.md
│   │   ├── NTP
│   │   │   └── NTP.md
│   │   └── 消息队列
│   │       ├── rabbitmq
│   │       │   └── images
│   │       │       └── 999593-20210427064620336-1513832581.png
│   │       └── rabbitmq.md
│   ├── 02-虚拟化
│   │   ├── 00-VIRT
│   │   │   └── virt命令.md
│   │   ├── 01-虚拟化概念
│   │   │   ├── 00-虚拟化基础
│   │   │   │   ├── images
│   │   │   │   │   ├── 135199189-f8ca013b-c21b-40e4-9cbb-1b16c6a11806.png
│   │   │   │   │   ├── 135199939-f6a6a6aa-fad4-4419-93b2-fc4eab4d90ed.png
│   │   │   │   │   ├── 135200115-d03732b9-d26e-4aa6-928f-e852a5891a43.png
│   │   │   │   │   ├── 135200207-0556db7e-dce4-49b5-a14f-6104a0f9e28f.png
│   │   │   │   │   └── 135200286-d21ccfcb-9b08-4ce7-bb22-80534d399738.png
│   │   │   │   ├── 网络模型.md
│   │   │   │   └── 虚拟化基础.md
│   │   │   ├── 01-CPU虚拟化
│   │   │   │   ├── CPU虚拟化.md
│   │   │   │   └── images
│   │   │   │       ├── 134466367-8c6ec4cf-cb71-4c9d-95f2-a0f177eef1e4.png
│   │   │   │       ├── 134466413-87122124-2cc4-4195-80e0-05316d8494ea.png
│   │   │   │       ├── 134466479-8f7b5aa3-6a36-42fa-b1d2-7ec66ca1f756.png
│   │   │   │       ├── 134466527-4eb1f3a0-bb69-48a2-bde0-d8a958e5f95e.png
│   │   │   │       ├── 134468695-2f476685-f3ad-47be-9e70-8278f9323a4d.png
│   │   │   │       ├── 134468707-d0eee613-14ee-4e4e-8339-6391b736f41b.png
│   │   │   │       ├── 134468726-2e42cdfe-e882-4820-97c8-881429e8db49.png
│   │   │   │       ├── 134468871-5218e35f-b23f-4eda-826a-466d84b4a6be.png
│   │   │   │       ├── 134468913-c7f945fd-c5a0-4ec5-b9a8-fd3d8a940038.png
│   │   │   │       ├── 134468980-da374074-db59-46fe-8b74-e9aafbc998fc.png
│   │   │   │       ├── 134469166-9b773566-9c8b-457d-8952-0666dbdcd5a6-1689928640564-32.png
│   │   │   │       ├── 134469182-37ddccb2-580f-4a97-bf08-2b69a72ec409.png
│   │   │   │       ├── 134469286-91fb211f-1e1e-4f03-aa11-02048265a8b1.png
│   │   │   │       ├── 134469403-f100f316-26e3-4fc1-a871-f748ca7c7b69.png
│   │   │   │       ├── 134469475-152425be-3c5a-4024-85af-0fd044db82bc.png
│   │   │   │       ├── 134469507-61189300-0c49-4f7f-8f50-f760230efd5f.png
│   │   │   │       ├── 134469527-cd408820-df84-408b-a8b8-087e3980967f.png
│   │   │   │       ├── 134469548-160ae515-c7ea-4ef3-b5d0-a6e5ed871ee3.png
│   │   │   │       ├── 134469568-44e7505b-d3ee-4c6a-916d-28e8997b8882.png
│   │   │   │       ├── 134469613-4b9cf68c-aaa8-4d30-8ef7-858e6700cd75.png
│   │   │   │       ├── 134469849-282bd67f-3211-4250-8541-eef131096246.png
│   │   │   │       ├── 134469968-cda6aea1-ca3a-4377-b5c3-d88bfccece2b.png
│   │   │   │       ├── 134470065-5f2f6954-b650-41d9-b7a6-fe1f139a88dc.png
│   │   │   │       ├── 134470120-75dc60c6-d78e-44d5-9ce0-98df12c3a6f6.png
│   │   │   │       └── 134470198-e7faf3ba-4de4-4efc-a899-fda3f654a35b.png
│   │   │   └── 02-内存虚拟化
│   │   │       ├── images
│   │   │       │   ├── 134480313-641d3a30-2a30-4075-80e4-366962cb3dae-1690183857140-5.png
│   │   │       │   ├── 134480313-641d3a30-2a30-4075-80e4-366962cb3dae.png
│   │   │       │   ├── 134480449-879a1ea7-dd7c-4a38-809a-379af7906663-1690183881120-10.png
│   │   │       │   ├── 134480449-879a1ea7-dd7c-4a38-809a-379af7906663.png
│   │   │       │   ├── 134481325-923f5684-7b8b-431a-86e8-b875ef4a6615.png
│   │   │       │   ├── 134481680-f15a6f30-a80f-4c6e-8798-184030c5e19d.png
│   │   │       │   ├── 134481932-d9fbe9a5-f33a-4f60-a555-164bd1a925fc.png
│   │   │       │   ├── 134481967-70fc93a3-edf7-4eb1-aad6-e9296a7da41f-1690183986508-20.png
│   │   │       │   ├── 134481967-70fc93a3-edf7-4eb1-aad6-e9296a7da41f.png
│   │   │       │   ├── 134481997-aed9d48c-a7e4-4092-b348-716509b73aec-1690183996867-21.png
│   │   │       │   ├── 134482070-f016dcb5-8f7b-45d8-9261-2d57f2f17240-1690184024255-23.png
│   │   │       │   ├── 134482099-3ab07df5-919e-438a-b724-10c3fcef0ca5-1690184036918-24.png
│   │   │       │   ├── 134482524-90caea91-77e3-4a9d-a63b-cb0cd2c659f7.png
│   │   │       │   ├── 134482796-f8c0f8e9-621e-4411-8e61-ac65c47e4a82.png
│   │   │       │   ├── 134482834-d7317132-d737-4448-a124-ff203096dd73.png
│   │   │       │   ├── 134482914-1c8ebc1f-2236-442b-8e16-601f5b0843ab.png
│   │   │       │   ├── 134482998-082002da-1385-4953-8ec9-0b4c449a4d86-1690184385609-31.png
│   │   │       │   ├── 134483197-ec89d15e-e44a-4b22-80ce-9688702668ce.png
│   │   │       │   ├── 134483230-1cead6d2-af31-4710-9280-52ac9af0972c.png
│   │   │       │   ├── 134483260-b69643da-e7e1-4cf8-97f1-5509f39b4b87.png
│   │   │       │   ├── 134485867-e8844ca2-ffea-4a8f-ad19-79b7c29897c4-1690185687048-40.png
│   │   │       │   ├── 134485938-38645885-a43e-47e5-975f-5751966fdded-1690185698722-41.png
│   │   │       │   ├── 134485938-38645885-a43e-47e5-975f-5751966fdded-1690185706901-42.png
│   │   │       │   ├── 134486023-3a8e0196-287e-4b18-960b-cc3eb136bc7d-1690185725810-43.png
│   │   │       │   ├── 134486327-e7bb4e02-e67e-4d7f-8ecf-e1b7e007fc67-1690185884967-44.png
│   │   │       │   ├── 134486442-fc55c334-ec83-4115-afbd-9f17714a13b6-1690185916083-45.png
│   │   │       │   ├── 134486663-c1b51d45-fd2e-4675-b731-ad91ae9c5537-1690185935305-46.png
│   │   │       │   └── 134489019-744beb81-317e-4ecd-a4ec-a2b6af43c684.png
│   │   │       └── 内存虚拟化.md
│   │   ├── 02-KVM
│   │   │   └── debian.md
│   │   ├── 03-虚拟机问题
│   │   │   ├── centos 6.md
│   │   │   ├── images
│   │   │   │   ├── 0fd21e70-a76c-4697-8592-0980a5b3e988.jpeg
│   │   │   │   └── image-20230705170900927.png
│   │   │   ├── windows
│   │   │   │   └── windows 根盘扩容.md
│   │   │   └── 终端连接虚拟机的几种方式.md
│   │   └── 04-显卡适配
│   │       ├── GPU适配.md
│   │       ├── deployment-guide-vgpu-Ampere-GPU.pdf
│   │       └── images
│   │           └── image-20221108180806277-8046578.png
│   ├── 03-kolla
│   │   └── kolla.md
│   ├── 04-openstack
│   │   ├── 00-oslo
│   │   │   └── oslo.privsep.md
│   │   ├── 01-部署
│   │   │   ├── DevStack部署.md
│   │   │   ├── Kolla-ansible部署.md
│   │   │   ├── OpenEuler OpenStack Bobcat 部署指南.md
│   │   │   ├── OpenEuler 部署.md
│   │   │   ├── OpenStack Python虚拟环境搭建.md
│   │   │   ├── openstack-ansible.md
│   │   │   └── 环境搭建.md
│   │   ├── 02-nova
│   │   │   ├── alembic.md
│   │   │   ├── images
│   │   │   │   ├── 1610676-20200523163017957-1184132094.png
│   │   │   │   ├── 1610676-20200523163457553-667114280.png
│   │   │   │   ├── 1610676-20200523163544656-759104690.png
│   │   │   │   ├── 1610676-20200523163721463-1878179074.png
│   │   │   │   ├── 1610676-20200523191854485-507945733.png
│   │   │   │   ├── 1610676-20200523194306671-1231306966.png
│   │   │   │   ├── 1610676-20200523194336180-1065575782.png
│   │   │   │   ├── 1610676-20200523194404325-1737146179.png
│   │   │   │   └── 30894282-6c4a59c0-a375-11e7-8396-c3faad0a683d.png
│   │   │   ├── nova cell架构模式
│   │   │   │   └── images
│   │   │   │       └── AA750B6F-4C7A-42B7-BB92-DA09805E515C_cropped_enhanced.png
│   │   │   ├── nova cell架构模式.md
│   │   │   ├── nova 创建虚拟机流程解析.md
│   │   │   ├── nova 功能解析
│   │   │   │   ├── 更改密码.md
│   │   │   │   └── 绑定密钥.md
│   │   │   ├── nova 迁移流程分析.md
│   │   │   ├── nova基础知识.md
│   │   │   └── 计算节点开启嵌套虚拟化.md
│   │   ├── 03-neutron
│   │   │   ├── images
│   │   │   │   ├── 1610676-20200525092906395-1030045008-20230814140923681.png
│   │   │   │   ├── 1610676-20200525093950627-1900725545.png
│   │   │   │   ├── 1610676-20200525093957562-1310557337.png
│   │   │   │   ├── 1610676-20200525094034213-1407022783.png
│   │   │   │   ├── 1610676-20200525094259973-1005671677.png
│   │   │   │   ├── 1610676-20200525100542425-1239541323.png
│   │   │   │   ├── 1610676-20200525101517751-1475447877.png
│   │   │   │   ├── 1610676-20200525105900232-1062723879.png
│   │   │   │   ├── 1610676-20200525111039385-1641360813.png
│   │   │   │   ├── 1610676-20200525113549109-238189231.png
│   │   │   │   ├── 1610676-20200525113712106-1528421796.png
│   │   │   │   ├── 1610676-20200525113722453-45392241.png
│   │   │   │   ├── 1610676-20200525141304100-1703728165.png
│   │   │   │   ├── 1610676-20200525142502610-225384625.png
│   │   │   │   └── 1610676-20200525151257686-2035246993.png
│   │   │   ├── linuxbridge 切换ovs.md
│   │   │   ├── 基础概念.md
│   │   │   ├── 源码学习
│   │   │   │   └── images
│   │   │   │       ├── image-20240116152655020.png
│   │   │   │       ├── image-20240116160346566.png
│   │   │   │       ├── image-20240116163105963.png
│   │   │   │       ├── modb_20211105_0a2920ce-3e1b-11ec-aa56-fa163eb4f6be.png
│   │   │   │       ├── neutron-api.png
│   │   │   │       ├── neutron-architecture.jpeg
│   │   │   │       └── neutron-ml2-plugin.png
│   │   │   └── 源码学习.md
│   │   ├── 05-glance
│   │   │   ├── images
│   │   │   │   ├── 1610676-20200523145052836-69025679.png
│   │   │   │   ├── 1610676-20200523150905292-596687303.png
│   │   │   │   ├── 1610676-20200523154140443-1817766473.png
│   │   │   │   └── 1610676-20200523154443765-1655498412.png
│   │   │   └── 基础概念.md
│   │   ├── 06-octavia
│   │   │   ├── octavia调研
│   │   │   │   └── images
│   │   │   │       ├── image-20241121152751432.png
│   │   │   │       ├── image-20241121152839488.png
│   │   │   │       ├── image-20241121153911969.png
│   │   │   │       ├── image-20241121155454415.png
│   │   │   │       └── octavia-component-overview.svg
│   │   │   └── octavia调研.md
│   │   ├── 07-ironic
│   │   │   ├── deployment_steps.dot
│   │   │   ├── ironic
│   │   │   │   └── images
│   │   │   │       ├── conceptual_architecture.png
│   │   │   │       ├── deployment_steps.png
│   │   │   │       ├── direct-deploy.svg
│   │   │   │       ├── image-20250108144422996.png
│   │   │   │       └── image-20250114104258863.png
│   │   │   └── ironic.md
│   │   ├── Build Octavia Amphora Images.md
│   │   └── OpenStack Client.md
│   ├── 05-images
│   │   └── images.md
│   └── 06-Proxmox VE
│       ├── 00-PVE简介.md
│       ├── Windows系统安装.md
│       └── 虚拟机镜像管理.md
├── 03-云原生与容器
│   ├── Kubernetes (K8s)
│   │   ├── install kubernets.md
│   │   └── kubernets 命令.md
│   ├── docker
│   │   ├── docker registry.md
│   │   ├── docker 基本操作.md
│   │   ├── docker-compose
│   │   │   ├── mariadb
│   │   │   │   └── mariadb.md
│   │   │   └── nginx
│   │   │       └── nginx.md
│   │   ├── dockerfile
│   │   │   ├── centos.dockerfile
│   │   │   ├── dockerfile.md
│   │   │   ├── gitea.yml
│   │   │   └── openeuler.dockerfile
│   │   ├── docker配置.md
│   │   └── gitea.md
│   ├── harbor
│   │   └── harbor 安装.md
│   └── kubevirt
│       └── kubevirt.md
├── 04-运维与系统管理
│   ├── 00-Linux
│   │   ├── Linux 双网卡服务器选择默认路由.md
│   │   ├── Linux命令详解
│   │   │   ├── brctl.md
│   │   │   └── firewall-cmd.md
│   │   ├── Linux基础运维.md
│   │   ├── Linux磁盘扩容.md
│   │   ├── mirrors.md
│   │   ├── openeuler
│   │   │   └── openeuler.md
│   │   ├── repo
│   │   │   └── linux源配置.md
│   │   ├── 内网穿透.md
│   │   ├── 网卡改名.md
│   │   ├── 证书生成.md
│   │   └── 防火墙配置.md
│   ├── 01-Windows
│   │   └── windwos11 问题.md
│   ├── 02-Mac
│   │   └── mac快捷键值北.md
│   ├── 03-硬件配置
│   │   ├── GL.iNet
│   │   │   └── 编译openwrt固件.md
│   │   ├── K2 键盘.md
│   │   └── ikbc w210.pdf
│   └── 04-软件配置
│       ├── Office的安装与配置.md
│       ├── brew
│       │   ├── homebrew.md
│       │   ├── init_mac.sh
│       │   ├── install.sh
│       │   └── lrzsz
│       │       ├── iterm2-recv-zmodem.sh
│       │       ├── iterm2-send-zmodem.sh
│       │       └── rzsz.md
│       ├── iterm2
│       │   ├── iterm2.json
│       │   └── iterm2配置.md
│       ├── msys2
│       │   └── 环境配置.md
│       ├── tmux
│       │   ├── tmux 快捷键指北.md
│       │   ├── tmux.conf
│       │   ├── tmux.conf.md
│       │   └── tmux.md
│       ├── vim
│       │   ├── images
│       │   │   └── vim键盘图.webp
│       │   └── vim.md
│       ├── virtual studio
│       │   ├── images
│       │   │   ├── image-20221113181839739.png
│       │   │   └── image-20221113182232347.png
│       │   └── virtual studio.md
│       └── zsh
│           └── zsh.md
├── 05-数据库
│   ├── mysql
│   │   ├── mysql.md
│   │   └── 完全卸载数据库.md
│   └── redis
│       └── redis.md
├── 06-笔记与文档
│   ├── dashDoc 制作指南.md
│   ├── 提效技巧
│   │   └── images
│   │       └── image-20250326185143957.png
│   ├── 提效技巧.md
│   ├── 画图示例.md
│   ├── 隧道登陆方式
│   │   └── images
│   │       ├── image-20250310111528450.png
│   │       ├── image-20250310111616612.png
│   │       ├── image-20250310111702890.png
│   │       ├── image-20250310111907532.png
│   │       ├── image-20250310112620746.png
│   │       ├── image-20250310112747694.png
│   │       ├── image-20250310112807105.png
│   │       └── image-20250310112826439.png
│   └── 隧道登陆方式.md
├── ReadMe.md
└── gen.sh

118 directories, 291 files
```
