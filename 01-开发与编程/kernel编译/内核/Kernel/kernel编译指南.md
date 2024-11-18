# kernel 编译指南

## 前置准备

1. 源代码
2. 构建依赖

### Linux版本导览

1. **linux-next 树：** 所有准备合并到 Linux 代码库的代码首先被合并到 linux-next 树。它代表的是 Linux 内核最新也是“最不稳定”的状态。大多数 Linux 内核开发者和测试人员使用这个来提高代码质量，为 Linus Torvalds 的后续提取做准备。**请谨慎使用！**
2. **发布候选版（RC） / 主线版：** Linus 从 linux-next 树抽取代码并创建一个初始发布版本。这个初始发布版本的测试版称为 RC（发布候选Release Candidate）版本。一旦 RC 版本发布，Linus 只会接受对它的错误修复和性能退化相关的补丁。基础这些反馈，Linus 会每周发布一个 RC 内核，直到他对代码感到满意。RC 发行版本的标识是 `-rc` 后缀，后面跟一个数字。
3. **稳定版：** 当 Linus 觉得最新的 RC 版本已稳定时，他会发布最终的“公开”版本。稳定发布版将会维护几周时间。像 Arch Linux 和 Fedora Linux 这样的前沿 Linux 发行版会使用此类版本。**我建议你在试用 linux-next 或任何 RC 版本之前，先试一试此版本。**
4. **LTS 版本：** 每年最后一个稳定版将会再维护 [几年](https://news.itsfoss.com/linux-kernel-support/)。这通常是一个较旧的版本，但它会 **会积极地维护并提供安全修复**。Debian 的稳定版本会使用 Linux 内核的 LTS 版版本

## 系统准备

### 依赖安装

- Arch Linux

  ```bash
  sudo pacman -S base-devel bc coreutils cpio gettext initramfs kmod libelf ncurses pahole perl python rsync tar xz
  ```

- Debian

  ```bash
  sudo apt install bc binutils bison dwarves flex gcc git gnupg2 gzip libelf-dev libncurses5-dev libssl-dev make openssl pahole perl-base rsync tar xz-utils
  ```

- Fedora

  ```bash
  sudo yum group install "Development Tools"
  sudo dnf install openssl openssl-devel dwarves rpm-build libelf-devel elfutils-libelf-devel ncurses rsync
  
  dnf install wget gcc gc bc gd make perl ncurses-devel xz rpm-build xmlto asciidoc hmaccalc python-devel newt-devel pesign binutils-devel audit-libs-devel numactl-devel pciutils-devel perl-ExtUtils-Embed -y
  ```

### 下载内核源码

> [!TIP]
>
> 访问 [kernel.org](https://kernel.org/)，在页面中寻找第一个 稳定Stable 版本
>
> 下载tar包和.tar.sign文件

#### 校验Tar文件的完整性

```bash
# 解压xz文件
xz -dk linux-*.tar.xz

# 获取 Linus Torvalds 和 Greg KH 使用的 GPG 公开密钥，对 Tar 文件进行签名
gpg2 --locate-keys torvalds@kernel.org gregkh@kernel.org

# 校验tar文件的完整性
gpg2 --verify linux-*.tar.sign

ubuntu@ubuntu:~/work$ gpg2 --verify linux-6.1.73.tar
linux-6.1.73.tar       linux-6.1.73.tar.sign  linux-6.1.73.tar.xz
ubuntu@ubuntu:~/work$ gpg2 --verify linux-6.1.73.tar.sign
gpg: assuming signed data in 'linux-6.1.73.tar'
gpg: Signature made Mon 15 Jan 2024 05:56:11 PM UTC
gpg:                using RSA key 647F28654894E3BD457199BE38DBBDC86092693E
gpg: Good signature from "Greg Kroah-Hartman <gregkh@kernel.org>" [unknown]
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 647F 2865 4894 E3BD 4571  99BE 38DB BDC8 6092 693E
```

#### 解压tar文件

```bash
tar -xf linux-*.tar
```

## 配置Linux内核

### 使用发行版提供的配置

> [!TIP]
>
> 大多数 Linux 发行版，如 Debian 和 Fedora 及其衍生版，将会把它存在 `/boot/config-$(uname -r)`
>
> 一些 Linux 发行版，比如 Arch Linux 将它整合在了 Linux 内核中。所以，可以在 `/proc/config.gz` 找到

```bash
cd linux-*/

### Debian 和 Fedora 及其衍生版：
$ cp /boot/config-"$(uname -r)" .config
### Arch Linux 及其衍生版：
$ zcat /proc/config.gz > .config
```
#### 更新配置文件

```bash
# 原来的 .config 文件将被重命名为 .config.old 进行备份，并将新的更改写入至 .config 文件
make olddefconfig
```

> [!NOTE]
>
> Debian 及其衍生版为内核模块使用一个签名证书。默认情况下，你的计算机并不包含这个证书

```bash
./scripts/config --file .config --set-str SYSTEM_TRUSTED_KEYS ''
./scripts/config --file .config --set-str SYSTEM_REVOCATION_KEYS ''
```

> [!NOTE]
>
> Centos及其衍生版为内核模块使用一个签名证书,默认情况下，你的计算机并不包含这个证书。

```bash
./scripts/config --file .config --set-str CONFIG_SYSTEM_TRUSTED_KEYS ""

./scripts/config --file .config --set-str CONFIG_DEBUG_INFO_BTF ""
./scripts/config --file .config --set-str CONFIG_ARCH_TEGRA_186_SOC ""
```

### 使用自定义配置

> [!CAUTION]
>
> **请注意，偏离你的 Linux 发行版的配置可能无法在实体硬件上“正常”工作。**问题可能是特定硬件无法工作、Linux 内核无法启动等

通过查看 [make help 的输出](https://www.kernel.org/doc/makehelp.txt) 来查看 *所有* 可用的选项，但我们主要关注三个 `make` 目标：

- `defconfig`: 默认配置
- `allmodconfig`: 根据当前系统状态，尽可能地把项目构建为可加载模块（而非内建）
- `tinyconfig`: 极简的 Linux 内核

由于 `tinyconfig` 目标只会构建少数项目，构建时间将会缩短。我个人选择它的原因主要有：

1. 检查我在代码/工具链中做的修改是否正确，以及代码是否可以编译。
2. 在虚拟机中只进行少数选项的测试。

> [!NOTE]
>
> 在为 ARM 或 RISC-V 机器构建 Linux 内核时，你可能需要 DTB（设备树的二进制文件）。**使用 `tinyconfig` 目标将不会启用构建 DTB 的选项，你的内核很可能无法启动。**

### 修改配置

无论你是使用 Linux 发行版的配置并更新它，还是使用 `defconfig` 目标创建新的 `.config` 文件，你都可能希望熟悉如何修改这个配置文件。**最可靠的修改方式是使用 `menuconfig` 或 `nconfig` 目标。**

```bash
make menuconfig
```

## 构建 Linux 内核

```bash
# 版本对应为 6.5.5-ksyun
./scripts/config --file .config --set-str LOCALVERSION "-ksyun"
```

- debian

  ```bash
  make -j$(nproc) 2>&1 | tee log
  
  # 查询编译错误
  grep Error log
  ```

- centos

  ```bash
  make rpm-pkg
  ```

  


```bash
# 版本对应为 6.5.5-ksyun
./scripts/config --file .config --set-str LOCALVERSION "-ksyun"

# 编译
make -j$(nproc) 2>&1 | tee log

# CentOS 编译成 rpm包 生成位置 /usr/src/redhat/RPMS/
make rpm-pkg

# 查询编译错误
grep Error log
```

### 自定义make目标

> [!NOTE]
>
> 在 Linux 内核的源文件夹中，`make` 命令有一些自定义的目标可供执行各种操作。这些主要作为开发者的参考

#### 构建目标

作为一名开发者，你可能只想构建 Linux 内核，或者只想构建模块，或者只想构建设备树二进制（DTB）。在这种情况下，你可以指定一个构建目标，然后 `make` 命令只会构建指定的项目，而不会构建其他的。

以下是一些构建目标：

- `vmlinux`：纯粹的 Linux 内核。
- `modules`：可加载模块。
- `dtbs`：设备树二进制文件（主要用于 ARM 和 RISC-V 架构）。
- `all`：构建所有被标记了星号 `*` 的项目（从 `make help` 的输出中可以查看）。

```bash
# 构建引导所需的 Linux 内核
### 对于 x86_64
$ make bzImage


### x86_64
$ make -s image_name
arch/x86/boot/bzImage
### AArch64
$ make -s image_name
arch/arm64/boot/Image.gz
### RISC-V
$ make -s image_name
arch/riscv/boot/Image.gz

make $(make -s image_name | awk -F '/' '{print $4}')
```

#### 清理目标

如果你需要清理构建产生的文件，你可以用以下的目标来实现你的需求：

- `clean`：除了 `.config` 文件外，删除几乎所有其他内容。
- `mrproper`：执行了 `make clean` 的所有操作外，还会删除 `.config` 文件。
- `distclean`：除了执行 `make mrproper` 的所有操作外，还会清理任何补丁文件。

## 安装

### 安装内核模块

> [!NOTE]
>
> Linux 内核有部分在系统启动时并非必需的。这些部分被构建为可加载模块，即在需要时才进行加载和卸载

首先需要安装这些模块。这可以通过 `modules_install` 目标完成。**必须使用 `sudo`**，因为模块会被安装在 `/lib/modules/<kernel_release>-<localversion>` 这个需要 `root` 权限的路径下

```bash
sudo make modules_install -j$(nproc)

# 可以通过设定 INSTALL_MOD_PATH 变量来指定一个不同的路径存放 Linux 模块，而不用默认的 /lib/modules/<kernel_release>-<localversion
# INSTALL_MOD_STRIP 变量来决定是否需要剥离模块的调试符号。如果未设定该变量，调试符号不会被剥离。当设为 1 时，符号信息将会被使用 --strip-debug 选项剥离，随后该选项会传递给 strip（或者在使用 Clang 的时候传递给 llvm-strip）工具

sudo make modules_install INSTALL_MOD_PATH=<path>
```

### 安装 Linux 内核头文件(可选)

如果你打算使用这个内核来支持树外模块，比如 ZFS 或英伟达 DKMS，或者打算尝试自行编写模块，你可能会需要 Linux 内核提供的头文件

```bash
# 安装Linux内核头文件
sudo make headers_install
```

### 安装 DTB（只针对 ARM 和 RISC-V）

```bash
### 对于 AArch32
$ find arch/arm/boot/dts -name "*.dtb" -type f | head -n 1 > /dev/null && echo "DTBs for ARM32 were built"
### 对于 AArch64
$ find arch/arm64/boot/dts -name "*.dtb" -type f | head -n 1 > /dev/null && echo "DTBs for ARM64 were built"
### 对于 RISC-V
$ find arch/riscv/boot/dts -name "*.dtb" -type f | head -n 1 > /dev/null && echo "DTBs for RISC-V were built"

sudo make dtbs_install
```

### 安装 Linux 内核

```bash
sudo make install
```

### 卸载Linux 内核

```bash
### 删除内核模块
$ rm -rf /lib/modules/<kernel_release>-<localversion>
### 删除设备树二进制文件
$ rm -rf /boot/dtb-<kernel_release>-<localversion>
### 删除 Linux 内核本身
$ rm -vf /boot/{config,System,vmlinuz}-<kernel_release>-<localversion>
```



## 遇到问题

1. 报错 #include <gelf.h>

```bash
User
/root/work/linux-6.6.12/tools/objtool/include/objtool/elf.h:10:10: fatal error: gelf.h: No such file or directory
 #include <gelf.h>
          ^~~~~~~~
```

缺失Elfutils 库

```bash
apt-get install elfutils

dnf install elfutils-libelf-devel
```

2. make[4]: *** [scripts/Makefile.build:243: net/wireless/nl80211.o] Error 1
   make[3]: *** [scripts/Makefile.build:480: net/wireless] Error 2
   make[2]: *** [scripts/Makefile.build:480: net] Error 2
   make[1]: *** [/root/work/linux-6.6.12/Makefile:1913: .] Error 2
   make: *** [Makefile:234: __sub-make] Error 2

3. make[2]: *** 没有规则可制作目标“certs/rhel.pem”，由“certs/x509_certificate_list” 需求。 停止。 make[2]: *** 正在等待未完成的任务.... make[1]: *** [scripts/Makefile.build:500：certs] 错误 2 make[1]: *** 正在等待未完成的任务....

   ```bash
   .config CONFIG_SYSTEM_TRUSTED_KEY=""
   ```

4. ERROR: modpost: "vchan_dma_desc_free_list" [drivers/dma/tegra186-gpc-dma.ko] undefined!
   ERROR: modpost: "vchan_init" [drivers/dma/tegra186-gpc-dma.ko] undefined!
   ERROR: modpost: "vchan_tx_submit" [drivers/dma/tegra186-gpc-dma.ko] undefined!
   ERROR: modpost: "vchan_tx_desc_free" [drivers/dma/tegra186-gpc-dma.ko] undefined!
   ERROR: modpost: "vchan_find_desc" [drivers/dma/tegra186-gpc-dma.ko] undefined!
   make[3]: *** [scripts/Makefile.modpost:126: Module.symvers] Error 1

​	去掉 .config 中 关于tegra的选项，即可编译成功

5. BTF: .tmp_vmlinux.btf: pahole (pahole) is not available
   Failed to generate BTF for vmlinux
   Try to disable CONFIG_DEBUG_INFO_BTF
   make[3]: *** [scripts/Makefile.vmlinux:34: vmlinux] Error 1
   make[2]: *** [Makefile:1255: vmlinux] Error 2
   错误：/var/tmp/rpm-tmp.rBrhTz (%build) 退出状态不好

```bash
sudo yum install dwarves
```

## centos 内核编译

```bash
dnf install rpmdevtools tmux vim

rpmdev-setuptree

# 安装 epel
sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm

sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-next-release-latest-9.noarch.rpm

dnf remove epel-release
dnf remove epel-next-release


dnf install asciidoc audit-libs-devel bc binutils-devel bpftool dwarves elfutils-devel gcc-c++ gcc-plugin-devel glibc-static java-devel kernel-rpm-macros libbabeltrace-devel libbpf-devel libcap-devel libcap-ng-devel libnl3-devel libtraceevent-devel ncurses-devel newt-devel numactl-devel pciutils-devel "perl(ExtUtils::Embed)" perl-devel perl-generators python3-devel python3-docutils rsync xmlto xz-devel

git clone https://git.centos.org/rpms/kernel.git

cd kernel

git checkout -b c9 remotes/origin/c9


```

