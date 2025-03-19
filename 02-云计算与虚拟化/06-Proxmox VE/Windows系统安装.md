# PVE windows系统安装

## 背景

在尝试PVE的过程中发现了一些问题，包括但不限于自定义性不足，不支持软盘（Floppy）引导等等，



## 过程记录

- 镜像下载

  分享一个镜像站，收录了很多网上难找的旧系统、软件等：[WinWorld](https://winworldpc.com/home)

### PVE安装系统

1. 上传软盘镜像

   由于 PVE 不支持 img 文件，我们可以用 `scp` 或 `sftp` 将镜像上传到 PVE 系统上。

   在 PVE 系统中，`/var/lib/vz/template/iso` 文件夹是 PVE 镜像模版的默认存储位置，建议统一存储在同一位置。

   ```bash
   # SCP
   scp -O /path/to/file/xxx.img username@remote_ip:/var/lib/vz/template/iso
   
   # SFTP
   sftp username@remote_ip
   
   sftp> lcd /path/to/file
   sftp> put -r xxx.img /var/lib/vz/template/iso
   sftp> exit
   
   ```

2. 创建虚拟机

   ```bash
   ```

   

3. PVE Shell 基本操作

   ```bash
   # 显示虚拟机启动指令
   qm showcmd <vmid> [options]
   
   # 进入虚拟机 kvm 控制台
   qm monitor <vmid> [options]
   
   # 显示虚拟机列表（包含虚拟机PID等基本信息）
   qm list 
   ```

4. 挂载软盘并引导

   使用 `qm list` 指令，查看刚刚创建的虚拟机的VMID

   ```bash
   root@truenas[~]# qm list
      VMID NAME                 STATUS     MEM(MB)    BOOTDISK(GB) PID       
       100 HAOS                 running    2048              32.00 1853288   
       101 xenix                stopped    256                0.00 0         
       102 MSDOS7.1             stopped    512                2.00 0         
       103 PureDarwin           running    2048              32.00 139604    
       104 pdxmas               stopped    2048              32.00 0         
   ```

   使用 `qm showcmd <vmid>` 查看 kvm 命令

   ```bash
   root@truenas[~]# qm showcmd 102
   
   /usr/bin/kvm -id 102 -name 'MSDOS7.1,debug-threads=on' -no-shutdown -chardev 'socket,id=qmp,path=/var/run/qemu-server/102.qmp,server=on,wait=off' -mon 'chardev=qmp,mode=control' -chardev 'socket,id=qmp-event,path=/var/run/qmeventd.sock,reconnect=5' -mon 'chardev=qmp-event,mode=control' -pidfile /var/run/qemu-server/102.pid -daemonize -smbios 'type=1,uuid=464448a0-979e-4af4-9cb6-bf4755594c7b' -smp '2,sockets=1,cores=2,maxcpus=2' -nodefaults -boot 'menu=on,strict=on,reboot-timeout=1000,splash=/usr/share/qemu-server/bootsplash.jpg' -vnc 'unix:/var/run/qemu-server/102.vnc,password=on' -cpu qemu64,+aes,enforce,+kvm_pv_eoi,+kvm_pv_unhalt,+pni,+popcnt,+sse4.1,+sse4.2,+ssse3 -m 512 -device 'pci-bridge,id=pci.1,chassis_nr=1,bus=pci.0,addr=0x1e' -device 'pci-bridge,id=pci.2,chassis_nr=2,bus=pci.0,addr=0x1f' -device 'pci-bridge,id=pci.3,chassis_nr=3,bus=pci.0,addr=0x5' -device 'vmgenid,guid=4c87b94b-3216-480b-8308-6c5f5ed9c435' -device 'piix3-usb-uhci,id=uhci,bus=pci.0,addr=0x1.0x2' -device 'usb-tablet,id=tablet,bus=uhci.0,port=1' -device 'VGA,id=vga,bus=pci.0,addr=0x2' -device 'virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x3,free-page-reporting=on' -iscsi 'initiator-name=iqn.1993-08.org.debian:01:33a44c1b79b' -drive 'file=/dev/zvol/Hack1n-Disk/vm-102-disk-0,if=none,id=drive-ide0,format=raw,cache=none,aio=io_uring,detect-zeroes=on' -device 'ide-hd,bus=ide.0,unit=0,drive=drive-ide0,id=ide0,bootindex=100' -drive 'if=none,id=drive-ide2,media=cdrom,aio=io_uring' -device 'ide-cd,bus=ide.1,unit=0,drive=drive-ide2,id=ide2,bootindex=101' -machine 'type=pc+pve0'
   ```

   windows 挂载软盘

   ```bash
   /usr/bin/kvm -id 102 -name 'MSDOS7.1,debug-threads=on' -no-shutdown -chardev 'socket,id=qmp,path=/var/run/qemu-server/102.qmp,server=on,wait=off' -mon 'chardev=qmp,mode=control' -chardev 'socket,id=qmp-event,path=/var/run/qmeventd.sock,reconnect=5' -mon 'chardev=qmp-event,mode=control' -pidfile /var/run/qemu-server/102.pid -daemonize -smbios 'type=1,uuid=464448a0-979e-4af4-9cb6-bf4755594c7b' -smp '2,sockets=1,cores=2,maxcpus=2' -nodefaults -boot 'menu=on,strict=on,reboot-timeout=1000,splash=/usr/share/qemu-server/bootsplash.jpg' -vnc 'unix:/var/run/qemu-server/102.vnc,password=on' -cpu qemu64,+aes,enforce,+kvm_pv_eoi,+kvm_pv_unhalt,+pni,+popcnt,+sse4.1,+sse4.2,+ssse3 -m 512 -device 'pci-bridge,id=pci.1,chassis_nr=1,bus=pci.0,addr=0x1e' -device 'pci-bridge,id=pci.2,chassis_nr=2,bus=pci.0,addr=0x1f' -device 'pci-bridge,id=pci.3,chassis_nr=3,bus=pci.0,addr=0x5' -device 'vmgenid,guid=4c87b94b-3216-480b-8308-6c5f5ed9c435' -device 'piix3-usb-uhci,id=uhci,bus=pci.0,addr=0x1.0x2' -device 'usb-tablet,id=tablet,bus=uhci.0,port=1' -device 'VGA,id=vga,bus=pci.0,addr=0x2' -device 'virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x3,free-page-reporting=on' -iscsi 'initiator-name=iqn.1993-08.org.debian:01:33a44c1b79b' -drive 'file=/dev/zvol/Hack1n-Disk/vm-102-disk-0,if=none,id=drive-ide0,format=raw,cache=none,aio=io_uring,detect-zeroes=on' -device 'ide-hd,bus=ide.0,unit=0,drive=drive-ide0,id=ide0,bootindex=100' -drive 'if=none,id=drive-ide2,media=cdrom,aio=io_uring' -device 'ide-cd,bus=ide.1,unit=0,drive=drive-ide2,id=ide2,bootindex=101' -machine 'type=pc+pve0' -fda /var/lib/vz/template/iso/msdos/disk01.img
   
   
   
   /usr/bin/kvm -id 102 -name 'windowsXP,debug-threads=on' -no-shutdown -chardev 'socket,id=qmp,path=/var/run/qemu-server/102.qmp,server=on,wait=off' -mon 'chardev=qmp,mode=control' -chardev 'socket,id=qmp-event,path=/var/run/qmeventd.sock,reconnect=5' -mon 'chardev=qmp-event,mode=control' -pidfile /var/run/qemu-server/102.pid -daemonize -smbios 'type=1,uuid=20b70559-184d-4795-8798-c34e3dc2a90a' -smp '1,sockets=1,cores=1,maxcpus=1' -nodefaults -boot 'menu=on,strict=on,reboot-timeout=1000,splash=/usr/share/qemu-server/bootsplash.jpg' -vnc 'unix:/var/run/qemu-server/102.vnc,password=on' -cpu qemu64,+aes,enforce,+kvm_pv_eoi,+kvm_pv_unhalt,+pni,+popcnt,+sse4.1,+sse4.2,+ssse3 -m 2048 -object 'iothread,id=iothread-virtio0' -device 'pci-bridge,id=pci.1,chassis_nr=1,bus=pci.0,addr=0x1e' -device 'pci-bridge,id=pci.2,chassis_nr=2,bus=pci.0,addr=0x1f' -device 'vmgenid,guid=920e59e5-0776-40c1-a26e-f46ff76d1559' -device 'piix3-usb-uhci,id=uhci,bus=pci.0,addr=0x1.0x2' -device 'usb-tablet,id=tablet,bus=uhci.0,port=1' -device 'cirrus-vga,id=vga,bus=pci.0,addr=0x2' -chardev 'socket,path=/var/run/qemu-server/102.qga,server=on,wait=off,id=qga0' -device 'virtio-serial,id=qga0,bus=pci.0,addr=0x8' -device 'virtserialport,chardev=qga0,name=org.qemu.guest_agent.0' -device 'virtio-balloon-pci,id=balloon0,bus=pci.0,addr=0x3,free-page-reporting=on' -iscsi 'initiator-name=iqn.1993-08.org.debian:01:4033ca112394' -drive 'file=/var/lib/vz/template/iso/virtio-win-0.1.173.iso,if=none,id=drive-ide0,media=cdrom,aio=io_uring' -device 'ide-cd,bus=ide.0,unit=0,drive=drive-ide0,id=ide0,bootindex=100' -drive 'file=/var/lib/vz/template/iso/zh-hans_windows_xp_professional_with_service_pack_3_x86_cd_vl_x14-74070.iso,if=none,id=drive-ide2,media=cdrom,aio=io_uring' -device 'ide-cd,bus=ide.1,unit=0,drive=drive-ide2,id=ide2,bootindex=101' -drive 'file=/dev/pve/vm-102-disk-0,if=none,id=drive-virtio0,format=raw,cache=none,aio=io_uring,detect-zeroes=on' -device 'virtio-blk-pci,drive=drive-virtio0,id=virtio0,bus=pci.0,addr=0xa,iothread=iothread-virtio0,bootindex=102' -netdev 'type=tap,id=net0,ifname=tap102i0,script=/var/lib/qemu-server/pve-bridge,downscript=/var/lib/qemu-server/pve-bridgedown,vhost=on' -device 'virtio-net-pci,mac=BC:24:11:A6:2A:EC,netdev=net0,bus=pci.0,addr=0x12,id=net0,rx_queue_size=1024,tx_queue_size=256,bootindex=103' -rtc 'driftfix=slew,base=localtime' -machine 'type=pc-i440fx-9.0+pve0' -fda /var/lib/vz/template/iso/virtio-win-0.1.173_x86.vfd
   ```

   



## 参考链接

- [PVE软盘安装系统Tips | 迷失的小K](https://blog.kclub.tech/2023/12/03/PVE软盘安装系统Tips/)

  