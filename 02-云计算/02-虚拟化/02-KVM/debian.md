```shell
<domain type='kvm'>  //如果是Xen，则type=‘xen’
  <name>vm0</name> //虚拟机名称，同一物理机唯一
  <uuid>fd3535db-2558-43e9-b067-314f48211343</uuid>  //同一物理机唯一，可用uuidgen生成
  <memory>524288</memory>
  <currentMemory>524288</currentMemory>  //memory这两个值最好设成一样
  <vcpu>2</vcpu>            //虚拟机可使用的cpu个数，查看物理机可用CPU个数：cat /proc/cpuinfo |grep processor | wc -l 
  <os>
   <type arch='x86_64' machine='pc-i440fx-vivid'>hvm</type> //arch指出系统架构类型，machine 则是机器类型，查看机器类型：qemu-system-x86_64 -M ?
   <boot dev='hd'/>  //启动介质，第一次需要装系统可以选择cdrom光盘启动
   <bootmenu enable='yes'/>  //表示启动按F12进入启动菜单
  </os>
  <features>
   <acpi/>  //Advanced Configuration and Power Interface,高级配置与电源接口
   <apic/>  //Advanced Programmable Interrupt Controller,高级可编程中断控制器
   <pae/>   //Physical Address Extension,物理地址扩展
  </features>
  <clock offset='localtime'/>  //虚拟机时钟设置，这里表示本地本机时间
  <on_poweroff>destroy</on_poweroff>  //突发事件动作
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
  <devices>   //设备配置
   <emulator>/usr/bin/kvm</emulator> //如果是Xen则是/usr/lib/xen/binqemu-dm
   <disk type='file' device='disk'> //硬盘
      <driver name='qemu' type='raw'/>
      <source file='/opt/vm/vmdev/fdisk.img'/>
      <target dev='vda' bus='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/> //域、总线、槽、功能号，slot值同一虚拟机上唯一
   </disk>
   <disk type='file' device='disk'>  
      <driver name='qemu' type='raw'/> 
      <source file='/opt/vm/vmdev/fdisk2.img'/>
      <target dev='vdb' bus='virtio'/>  
   </disk>
   <disk type='file' device='cdrom'>//光盘
      <driver name='qemu' type='raw'/>
      <source file='/opt/vm/vmiso/ubuntu-15.10-server-amd64.iso'/>
      <target dev='hdc' bus='ide'/>
      <readonly/>
   </disk>

   /* 利用Linux网桥连接网络 */
   <interface type='bridge'>   
      <mac address='fa:92:01:33:d4:fa'/> 
      <source bridge='br100'/>  //配置的网桥网卡名称
      <target dev='vnet0'/>     //同一网桥下相同
      <alias name='net0'/>      //别名，同一网桥下相同
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>  //注意slot值唯一
   </interface>

   /* 利用ovs网桥连接网络 */
   <interface type='bridge'>  
      <source bridge='br-ovs0'/>  
      <virtualport type='openvswitch'/>
      <target dev='tap0'/>     
      <model type='virtio'/>  
   </interface>

    /* 配置成pci直通虚拟机连接网络，SR-IOV网卡的VF场景 */
   <hostdev mode='subsystem' type='pci' managed='yes'>
     <source>
       <address domain='0x0000' bus='0x03' slot='0x00' function='0x0'/>
     </source>
   </hostdev>

   /* 利用vhostuser连接ovs端口 */
   <interface type='vhostuser'>   
      <mac address='fa:92:01:33:d4:fa'/> 
      <source type='unix' path='/var/run/vhost-user/tap0' mode='client'/>  
      <model type='virtio'/>     
      <driver vringbuf='2048'/>     
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>  
   </interface>

   <interface type='network'>   //基于虚拟局域网的网络
     <mac address='52:54:4a:e1:1c:84'/>  //可用命令生成，见下面的补充
     <source network='default'/> //默认
     <target dev='vnet1'/>  //同一虚拟局域网的值相同
     <alias name='net1'/>
     <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>  //注意slot值
   </interface>
  <graphics type='vnc' port='5900' autoport='yes' listen='0.0.0.0' keymap='en-us'/>  //配置vnc，windows下可以使用vncviewer登录，获取vnc端口号：virsh vncdisplay vm0
   <listen type='address' address='0.0.0.0'/>
  </graphics>
  </devices>
</domain>








<domain type='kvm'> 
  <name>test</name> 
  <uuid>fd3535db-2558-43e9-b067-314f48211343</uuid>
  <memory>524288</memory>
  <currentMemory>524288</currentMemory>  
  <vcpu>2</vcpu>           
  <os>
   <type arch='x86_64' machine='pc-i440fx-vivid'>hvm</type> 
   <boot dev='hd'/>  
   <bootmenu enable='yes'/> 
  </os>
  <features>
   <acpi/> 
   <apic/> 
   <pae/> 
  </features>
  <clock offset='localtime'/> 
  <on_poweroff>destroy</on_poweroff> 
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
  <devices> 
   <emulator>/usr/libexec/qemu-kvm</emulator> 
   <disk type='file' device='disk'>
      <driver name='qemu' type='raw'/>
      <source file='/opt/vm/fdisk.img'/>
      <target dev='vda' bus='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/> 
   </disk>
   <disk type='file' device='disk'>  
      <driver name='qemu' type='raw'/> 
      <source file=''/>
      <target dev='vdb' bus='virtio'/>  
   </disk>
   <disk type='file' device='cdrom'>
      <driver name='qemu' type='raw'/>
      <source file=''/>
      <target dev='hdc' bus='ide'/>
      <readonly/>
   </disk>
   
   

  <graphics type='vnc' port='5900' autoport='yes' listen='0.0.0.0' keymap='en-us'>  
   <listen type='address' address='0.0.0.0'/>
  </graphics>
  </devices>
</domain>
```
