# windows 根盘扩容

您需要删除恢复分区后, 才可以将后面的空间留给系统分区, 因为这需要是紧接着的空闲空间.
请您以管理员权限打开cmd, 输入

```shell
diskpart
lis dis
sel dis #
lis par
sel par #
del par override
```


其中#是您上一步得到的数字, 请务必准确选择硬盘和分区.
删除后, 请您右键系统分区, 点击扩展卷即可