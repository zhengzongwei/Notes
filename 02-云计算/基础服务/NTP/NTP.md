# NTP Server

1. **安装NTP软件包:**

   打开终端并以管理员身份执行以下命令，使用`dnf`包管理器安装NTP软件包：

   ```
   sudo dnf install ntp
   ```

2. **配置NTP:**

   NTP的主要配置文件是`/etc/ntp.conf`。你可以使用文本编辑器打开该文件进行配置。例如，使用`vi`编辑器：

   ```bash
   sudo vi /etc/ntp.conf
   ```

   在文件中，你可以配置NTP服务器、允许的客户端等。以下是一个简单的例子：

   ```bash
   # 允许所有客户端
   restrict default kod nomodify notrap nopeer noquery
   
   # 允许本地网络的客户端
   restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap
   ```

   这个例子配置允许所有客户端，但限制了本地网络的客户端。

3. **启动和启用NTP服务:**

   启动NTP服务并设置为开机启动：

   ```bash
   sudo systemctl start ntpd
   sudo systemctl enable ntpd
   ```

   这将启动NTP服务，并将其配置为在系统启动时自动启动。

4. **检查NTP状态:**

   使用以下命令检查NTP服务的状态：

   ```bash
   sudo systemctl status ntpd
   ```

   如果一切正常，你应该看到NTP服务正在运行。

5. **防火墙配置（可选）:**

   如果系统上启用了防火墙，确保允许NTP流量通过。可以使用`firewalld`来配置防火墙规则：

   ```bash
   sudo firewall-cmd --add-service=ntp --permanent
   sudo firewall-cmd --reload
   ```

   这将允许NTP服务的流量通过防火墙。