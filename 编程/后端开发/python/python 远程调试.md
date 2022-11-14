# Python 远程调试

```python
# 语法
# 设置断点
from remote_pdb import RemotePdb;RemotePdb('127.0.0.1', 14444).set_trace()

# 项目启动之后，在终端使用socat进入调试模式，使用Ctrl+C退出调试模式
socat readline tcp:127.0.0.1:14444

sudo nova-rootwrap /etc/nova/rootwrap.conf chmod 202 /sys/class/mdev_bus/0000:5e:01.4/mdev_supported_types/nvidia-588/create && echo 0726b12b-5c6a-4c0b-b942-baed76152158 > /sys/class/mdev_bus/0000:5e:01.4/mdev_supported_types/nvidia-588/create
```

|  命令           |     说明    |
|  ----          |     ---     |
|  break 或 b    |     设置断点 |
|  continue 或 c |     继续执行程序 |
|  list 或 l     |     查看当前行的代码段 |
|  step 或 s   |     	进入函数 	|
|  return 或 r   |     执行代码直到从当前函数返回 |
|  exit 或 q     |     中止并退出 |
|  next 或 n     |     执行下一行 |
|  pp            |     打印变量的值 |
|  help          |     帮助 |