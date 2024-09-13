# Nova Cell架构模式

## 什么是cell？为什么有cell？

当openstack nova集群的规模变大时，所有的nova compute节点全部连接到同一个MQ，在有大量定时任务通过MQ上报给Nova-Conducor服务的情况下，数据库和消息队列服务就会出现瓶颈，而此时nova为提高水平扩张方式，大规模的部署能力，同时又不增加数据库和消息中间件的复杂服，引入了Cell 概念

如下图大量数据上报给DB数据库

![AA750B6F-4C7A-42B7-BB92-DA09805E515C_cropped_enhanced](./nova%20cell%E6%9E%B6%E6%9E%84%E6%A8%A1%E5%BC%8F/images/AA750B6F-4C7A-42B7-BB92-DA09805E515C_cropped_enhanced.png)



[OpenStack中 Nova的Cell架构模式介绍-CSDN博客](https://blog.csdn.net/Lihuihui006/article/details/112035435)