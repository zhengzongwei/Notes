# RabbitMQ基础

## 简介

1. RabbitMQ是一个开源的消息队列服务器，用来通过普通协议在完全不同的应用之间共享数据

2. 是使用Erlang语言编写的，基于AMQP协议

   Erlang语言在数据交互方面性能优秀，有着和原生Socket一样的延迟，这也是RabbitMQ高性能的原因所在

   AMQP：Advanced Message Queue，高级消息队列协议。它是应用层协议的一个开放标准，为面向消息的中间件设计，基于此协议的客户端与消息中间件可传递消息，并不受产品、开发语言等条件的限制。消息中间件主要用于组件之间的解耦，消息的发送者无需知道消息使用者的存在，反之亦然。

## 特点

　　1、可靠性：RabbitMQ 使用一些机制来保证可靠性，如持久化、传输确认、发布确认。

　　2、灵活的路由：在消息进入队列之前，通过 Exchange 来路由消息的。对于典型的路由功能，RabbitMQ 已经提供了一些内置的 Exchange 来实现。针对更复杂的路由功能，可以将多个 Exchange 绑定在一起，也通过插件机制实现自己的 Exchange。

　　3、消息集群：多个 RabbitMQ 服务器可以组成一个集群，形成一个逻辑 Broker 。

　　4、高可用：队列可以在集群中的机器上进行镜像，使得在部分节点出问题的情况下队列仍然可用。

　　5、多种协议：RabbitMQ 支持多种消息队列协议，比如 STOMP、MQTT 等等。

　　6、多语言客户端：RabbitMQ 几乎支持所有常用语言，比如 Java、.NET、Ruby 等等。

　　7、管理界面：RabbitMQ 提供了一个易用的用户界面，使得用户可以监控和管理消息 Broker 的许多方面。

　　8、跟踪机制：如果消息异常，RabbitMQ 提供了消息跟踪机制，使用者可以找出发生了什么。

　　9、插件机制：RabbitMQ 提供了许多插件，来从多方面进行扩展，也可以编写自己的插件。

## 消息模型

　　所有 MQ 产品从模型抽象上来说都是一样的过程，如下：

　　 消费者（consumer）订阅某个队列。生产者（producer）创建消息，然后发布到队列（queue）中，最后将消息发送到监听的消费者。

 

![img](./rabbitmq/images/999593-20210427064620336-1513832581.png)

### **RabbitMQ核心概念**





## RabbitMQ实践

### 安装

- openeuler

  ```bash
  dnf install rabbitmq-server
  ```

### 配置

- 启用插件

  ```bash
  # 启用 rabbit网页管理插件
  rabbitmq-plugins enable rabbitmq_management
  
  # 关闭 rabbit网页管理插件
  rabbitmq-plugins disable rabbitmq_management
  ```

- 添加用户

  ```bash
  # 创建账户
  rabbitmqctl add_user 用户名 密码
  
  # 授予用户为管理员角色
  rabbitmqctl set_user_tags 用户名 administrator
  
  # 给用户授权
  # "/"表示虚拟机
  # ".*" ".*" ".*" 表示完整权限
  rabbitmqctl set_permissions -p "/" 用户名 ".*" ".*" ".*"
  
  
  rabbitmqctl add)user admin 12345
  rabbtitmqctl set_user_tags admin administrator
  ```
  

### firewall 开放/关闭端口

```bash
firewall-cmd --zone=public --add-port=15672/tcp --permanent
firewall-cmd --zone=public --add-port=5672/tcp --permanent

firewall-cmd --zone=public --query-port=15672

firewall-cmd --zone=public --remove-port=15672/tcp

# 批量放开/或关闭端口
批量开放或关闭端口：
firewall-cmd --zone=public --add-port=40000-45000/tcp --permanent #批量开放端口，打开从40000到45000之间的所有端口
firewall-cmd --zone=public --list-ports #查看系统所有开放的端口
firewall-cmd --zone=public --remove-port=40000-45000/tcp --permanent #批量关闭端口，关闭从40000到45000之间的所有端口

sudo firewall-cmd --reload
```
