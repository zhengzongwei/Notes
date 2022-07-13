



#### 1. 确认一下当前zstack 默认设置的CPU模式

-   hci
    ​	x86 custom
    ​	arm host-passthrough

-   zstack
    ​	x86 未设置 默认为 custom
       arm host-passthrough
    
       numa对cpu模式的限制
    
       x86 host-model
       arm host-passthrough
       虚拟机中使用虚拟化 指定CPU model cortex-a57
    
       
    
    numa原理 需要配置 不需要配置的场景
    
    1.   numa 可以不停机升级CPU的性能
    2.   

#### 2. 整理一下当前平台cpu模式

​	当前平台支持的CPU模式有 host-model，host-passthrough，none，custom

​	x86平台默认为 custom

​	arm平台 默认为 host-passthrough

​	x86平台海光CPU 默认为 host-passthrough

#### 3. ARM 其他模式下虚拟机是否可以启动

host-model :不支持![image-20220615183019034](https://oss-typoraimages.oss-cn-hangzhou.aliyuncs.com/typora-images/202206151830159.png)

custom: 不支持

![image-20220616182214693](https://oss-typoraimages.oss-cn-hangzhou.aliyuncs.com/typora-images/202206161822798.png)

BUG链接 ： 1. [1782882 – qemu-kvm: kvm_init_vcpu failed: Function not implemented (redhat.com)](https://bugzilla.redhat.com/show_bug.cgi?id=1782882)

​                     2. [Re: [Qemu-devel\] Cubietruck: cannot create KVM guests: "kvm_init_vcpu fa (nongnu.org)](https://lists.nongnu.org/archive/html/qemu-devel/2014-12/msg01049.html)

总结BUG：ARM内核问题，内核不支持嵌套虚拟化。

#### 4. 整理几种（host-model、host-passthrough、custom）cpu_mode 区别及使用场景

| 物理CPU型号                                | 物理CPU采用的架构 | host-model          | custom            | host-passthrough |
| ------------------------------------------ | ----------------- | ------------------- | ----------------- | ---------------- |
| Intel(R)  Xeon(R) CPU E5-2630 v4 @ 2.20GHz | Broadwell E       | Broadwell-IBRS      | 用户指定cpu model | Broadwell E      |
| Intel(R)  Xeon(R) CPU E5-2620 v4 @ 2.10GHz | Broadwell EP架构  | Broadwell           | 用户指定cpu model | Broadwell EP架构 |
| Intel(R)  Xeon(R) Gold 5218 CPU @ 2.30GHz  | Skylake-SP        | Skylake-Server-IBRS | 用户指定cpu model | Skylake-SP       |
| Hygon C86 7265  24-core Processor          | Zen               | EPYC-IBPB(基于Zen)  | 用户指定cpu model | Zen              |
| Intel(R)  Xeon(R) CPU E5-2650 v2 @ 2.60GHz | lvy Bridge EP     | IvyBridge           | 用户指定cpu model | lvy Bridge EP    |

-    custom

    可以自定义qemu支持的CPU型号，可以模拟不同CPU型号，该模式下虚拟机CPU指令集最少，导致性能相对较差，它在热迁移时跨不同型号CPU的能力最强。支持用户添加额外的指令集，且必须配置cpu_model选项。

​		该模式在未配置mode时为默认选项，在多种不同型号的CPU中，该类型显示的CPU类型是相同的。

​		使用场景：
​      	1. 不同物理CPU场景，需要进行热迁移时，可以使用此模式
​      	2. 未配置mode时，默认使用该模式。该模式为默认配置（libvirt中默认未设置为此模式）

-   host-model
    libvirt 根据当前宿主机 CPU 指令集从配置文件 /usr/share/libvirt/cpu_map.xml 选择一种最相配的 CPU 型号。根据物理CPU的架构选择一种最匹配物理CPU架构的CPU型号
    
    这种模式相当于 配置为 custom 然后model与物理CPU类似的架构，相当于custom起的一个别名
    

​		使用场景：
​          1. 当前模式下虚拟机CPU的指令集比宿主机CPU少，热迁移时对目标节点CPU的兼容性好一些
​          2. 该模式的性能介于custom和host-passthrough之间，且热迁移的兼容性会比host-passthrough好，没有特殊要求，一般默认使用该模式

-   host-passthrough
   
	该模式是将物理CPU直接透传给虚拟机使用，可以最大限度使用宿主机CPU指令集，虚拟机可以获得物理CPU的性能。
	使用场景：
    1. 这种模式在三种模式中性能最好，对云主机性能要求高的场景，计算密集型
    2. 需要使用到的CPU特性只有物理CPU支持，其他方式模拟的CPU不支持的特性
    3. 该模式对虚拟机热迁移的目标节点CPU要求高，需要CPU架构一致，或者型号相同相近的CPU

-   none

​		不对CPU进行检查，可能会出现qemu无法支持该CPU，导致虚拟机无法启动

​		使用场景：

​			1.虚拟化类型为 qemu和kvm时，不支持该模式

​			2.在使用其他虚拟化类型 Hyper-V，VMware等虚拟机时使用该模式

#### 5. 各种模式下物理 CPU 不同的时验证是否支持热迁移，x86和arm 都要验证
总结：

​	1. 不同物理CPU下，enable_compare_cpu=False时，相同CPU模式下 custom 和host-passthrough热迁移模式正常(windows系统卡住，RH7.3forhygon正常)

​	2. 相同物理CPU（都是海光CPU）下，三种模式都可以成功（host-model 模式 windwos不支持）

#### 6. 调研，容器升级QEMU版本4.2.0

​	待补充

#### 7. 验证 arm 支持虚拟机嵌套虚拟化

arm 中支持虚拟机嵌套虚拟化，报错同问题3

-   [ ] 升级 QEMU 4.2.0 试试ARM嵌套虚拟化



(cpu, 'model', 'cortex-a57')

a7a2-9edf-8673-96bc-a07d-4845-3134-5697

```xml
<cpu mode='custom' match='exact' check='partial'>
  <model fallback='allow'>cortex-a57</model>
```

#### 8.   设置host-passthrough 设置model 后 是否生效

只有 custom 支持设置 model，其他模式不支持设置CPU model

![image-20220620173904783](https://oss-typoraimages.oss-cn-hangzhou.aliyuncs.com/typora-images/202206201740720.png)

#### 9.   镜像安装问题

1.   基于ISO 安装
     
        -   windows 使用镜像安装无问题
        -    redhat for hygon 从镜像安装无问题
        -   直接使用镜像安装有问题（发行版镜像内核版本低于4.20，Linux内核支持海光CPU版本为4.20以上的版本  https://blog.csdn.net/weixin_39607836/article/details/116680408）
                1.   centos8.5(内核版本 4.18)安装过程中会卡住，导致安装不成功
                2.   centos7(内核版本3.10)安装会卡住，导致安装不成功
                3.   ubuntu 2204 镜像安装（内核版本 5.15）成功
                4.   openeuler 2203 镜像安装（内核版本5.10）成功
    
2.   基于RAW创建虚拟机

     使用raw 创建虚拟机没有问题

#### 10.   迁移后，对比XML文件的区别，查看windwos 系统卡住的原因

​	热迁移
​	1. 相同CPU，不同CPU模式
​		xml配置与原主机保持一致。CPU模式以及feture未改变，热迁移保持CPU的模式 feture 等信息
​		CPU mode 在热迁移后不会改变，在硬重启后CPU mode 会变为当前节点上配置的cpu Mode模式

​	2. 不同CPU
​	   热迁移失败，回滚

