在没有TMP的电脑上安装windwos11 会提示`该电脑不支持此系统`

解决方案

```powershell
# shift + F10 打开 命令行界面
regedit

# 定位到如下位置 HKEY_LOCAL_MACHINE\SYSTEM\Setup
```

创建一个名为“LabConfig”的项，接着在“LabConfig”下创建两个DWORD值：

键名“BypassTPMCheck”，赋值“00000001”

键名“BypassSecureBootCheck”，赋值“00000001”

保存退出后，无法安装的提示就消失了。
