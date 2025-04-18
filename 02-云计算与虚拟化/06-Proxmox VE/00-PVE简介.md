# PVE 相关概念

## 系统

###  SCSI 控制器

- LSI 53C895A

  **类型：**模拟的SCSI控制器

  **特点：**

  - 兼容性高，支持大多数的操作系统（包括较旧的Windows和Linux版本）
  - 性能较低

  **使用场景：**

  - 需要高兼容性的场景（Windows XP或较老旧的Linux发行版）
  - 对性能要求不高的虚拟机

- LSI 53C810

  **类型：**模拟的SCSI控制器

  **特点：**

  - 兼容性高，但不如LSI 53C895A
  - 性能较低，适合轻量级任务

  **使用场景：**

  - 需要兼容性的场景，但是对性能要求较低

- MegaRAID SAS 8708EM2

  **类型：**模拟的RAID控制器

  **特点：**

  - 支持RAID功能，适合需要磁盘冗余的场景
  - 兼容性较好，性能较低

  **使用场景：**

  - 需要RAID功能的虚拟机
  - 对性能要求不高的场景

- Virtio SCSI single

  **类型：**基于Virtio的SCSI控制器

  **特点：**

  - 高性能，专为虚拟化环境优化
  - 需要虚拟机操作系统支持Virtio驱动
  - 支持多队列(Multi-Queue)，适合高并发场景

  **使用场景：**

  - Linux虚拟机（默认支持Virtio驱动）
  - Windows虚拟机
  - 需要高性能和低延迟的场景

- VMware PVSCSI

  **类型：**VMware的准虚拟化SCSI控制器

  **特点：**

  - 高性能，专为VMware环境优化
  - 需要虚拟机操作系统支持VMware Tools
  - 支持多队列(Multi-Queue)，适合高并发场景

  **使用场景：**

  - VMware环境中的虚拟机
  - 需要高性能和低延迟的场景

#### 总结

- **兼容性优先**：选择 LSI 53C895A 或 LSI 53C810。
- **性能优先**：选择 Virtio SCSI single 或 VMware PVSCSI。
- **RAID 功能**：选择 MegaRAID SAS 8708EM2。

| 控制器类型           | 兼容性 | 性能 | 使用场景                                    |
| -------------------- | ------ | ---- | ------------------------------------------- |
| LSI 53C895A          | 高     | 低   | 需要高兼容性的场景（如 Windows XP）         |
| LSI 53C810           | 较高   | 低   | 需要兼容性的场景，对性能要求较低            |
| MegaRAID SAS 8708EM2 | 较高   | 低   | 需要 RAID 功能的场景                        |
| Virtio SCSI single   | 较高   | 高   | 需要高性能的场景（如 Linux 或较新 Windows） |
| VMware PVSCSI        | 较高   | 高   | VMware 环境中需要高性能的场景               |

## 磁盘

### 总线

- IDE

  **类型：**模拟的IDE控制器

  **特点：**

  - 兼容性极高，支持几乎所有的操作系统
  - 性能较低
  - 最多支持4个设备(2主2从)

  **使用场景：**

  - 需要高兼容性的场景
  - 对性能不高的虚拟机

- SATA

  **类型：** 模拟的SATA控制器

  **特点：**

  - 兼容性较高，支持大多数操作系统
  - 性能优于IDE，但不如Virtio Block
  - 支持热插拔功能

  **使用场景：**

  - 需要兼容性和中等性能的场景

- Virtio Block

  **类型：**基于Virtio的块设备控制器

  **特点：**

  - 高性能，专为虚拟化环境优化
  - 需要虚拟机操作系统支持Virtio驱动
  - 低延迟，适合高I/O负载的场景

  **使用场景：**

  - 需要高性能和低延迟的场景

- SCSI

  **类型：**模拟的SCSI控制器

  **特点：**

  - 兼容性较高，支持大多数操作系统
  - 性能优于 IDE 和 SATA，但不如 Virtio Block
  - 支持 SCSI 命令队列等高级功能

  **使用场景：**

  - 需要兼容性和较高性能的场景
  - 支持 SCSI 高级功能的应用场景

|  控制器类型  | 兼容性 | 性能 |                   使用场景                    |
| :----------: | :----: | :--: | :-------------------------------------------: |
|     IDE      |  极高  |  低  |     需要高兼容性的场景（如 Windows XP）。     |
|     SATA     |  较高  |  中  |         需要兼容性和中等性能的场景。          |
| Virtio Block |  较高  |  高  | 需要高性能的场景（如 Linux 或较新 Windows）。 |
|     SCSI     |  较高  | 中高 |          需要兼容性和较高性能的场景           |

### 磁盘缓存模式

- Direct sync

  **特点：**

  - 数据直接写入磁盘，绕过宿主机的缓存
  - 数据一致性高，但性能较低

  **使用场景：**

  - 对数据一致性要求极高的场景（数据库或关键业务应用）
  - 性能要求不高的场景

- Write through

  **特点：**

  - 数据写入宿主机的缓存，并同时写入磁盘
  - 数据一致性高，但性能中等

  **使用场景：**

  - 对数据一致性要求较高的场景
  - 性能要求中等的场景

- Write back

  **特点：**

  - 数据写入宿主机的缓存，稍后异步写入磁盘
  - 性能高，但存在数据丢失的风险（如宿主机突然断电）

  **使用场景：**

  - 对性能要求高的场景
  - 数据丢失风险可接受的场景（如测试环境或非关键业务应用）

- Write back(不安全)

  **特点：**

  - 类似于 Write back，但数据一致性更差
  - 性能最高，但数据丢失的风险更大

  **使用场景：**

  - 对性能要求极高的场景
  - 数据丢失风险完全可接受的场景（如临时测试环境）

- 无缓存

  **特点：**

  - 完全禁用宿主机的缓存，数据直接写入磁盘
  - 数据一致性最高，但性能最低

  **使用场景：**

  - 对数据一致性要求极高的场景

  - 性能要求极低的场景

    |      缓存模式       | 数据一致性 | 性能 |                  使用场景                  |
    | :-----------------: | :--------: | :--: | :----------------------------------------: |
    |     Direct sync     |     高     |  低  |        对数据一致性要求极高的场景。        |
    |    Write through    |     高     |  中  |        对数据一致性要求较高的场景。        |
    |     Write back      |     中     |  高  |  对性能要求高的场景，数据丢失风险可接受。  |
    | Write back (不安全) |     低     | 极高 | 对性能要求极高的场景，数据丢失风险可接受。 |
    |       无缓存        |    最高    | 最低 |        对数据一致性要求极高的场景。        |

### I/O 处理模式

- io_uring

  **特点：**

  - 基于 Linux 内核的高性能异步 I/O 框架
  - 减少了系统调用的开销，适合高并发和高吞吐量的场景
  - 支持批量提交和完成 I/O 请求

  **使用场景：**

  - 需要高性能和低延迟的场景（如数据库、高并发 Web 服务）
  - 现代 Linux 内核（5.1 及更高版本）支持

- native

  **特点：**

  - 使用操作系统的原生 I/O 接口（如 `read`/`write`）
  - 简单易用，但性能较低
  - 适合轻量级任务

  **使用场景：**

  - 对性能要求不高的场景
  - 简单的应用程序或测试环境

- threads

  **特点：**

  - 使用多线程处理 I/O 请求
  - 通过并发提高性能，但线程管理开销较大
  - 适合多核 CPU 环境

  **使用场景：**

  - 需要并发处理的场景（如多用户文件服务器）

  - 对性能要求较高的场景，但无法使用更高级的 I/O 框架（如 `io_uring`）

    | I/O 处理模式 |               特点               |                  使用场景                  |
    | :----------: | :------------------------------: | :----------------------------------------: |
    |   io_uring   |  高性能，异步，减少系统调用开销  | 高性能和低延迟场景（如数据库、Web 服务）。 |
    |    native    |        简单易用，性能较低        |           对性能要求不高的场景。           |
    |   threads    | 多线程并发，性能较高，但开销较大 |    需要并发处理的场景（如文件服务器）。    |

## 网络

### 虚拟网络适配器类型

- intel E1000

  **类型**：模拟的 Intel 82545EM 千兆网卡

  **特点：**

  - 兼容性高，支持大多数操作系统（包括较旧的 Windows 和 Linux 版本）
  - 性能较低，因为它是模拟设备

  **使用场景：**

  - 需要高兼容性的场景（如 Windows XP 或较旧的 Linux 发行版）
  - 对性能要求不高的虚拟机

- intel E1000E

  **类型**：模拟的 Intel 82574L 千兆网卡

  

  **特点：**

  - 兼容性较高，支持大多数现代操作系统
  - 性能优于 E1000，但不如 Virtio

  **使用场景：**

  - 需要兼容性和中等性能的场景
  - 现代操作系统（如 Windows 7 及更高版本、Linux）

- Virtio

  **类型**：基于 Virtio 的准虚拟化网络适配器

  **特点：**

  - 高性能，专为虚拟化环境优化
  - 需要虚拟机操作系统支持 Virtio 驱动
  - 低延迟，适合高网络负载的场景

  **使用场景：**

  - Linux 虚拟机（默认支持 Virtio 驱动）
  - 较新的 Windows 虚拟机（Windows 2008 及更高版本默认支持 Virtio 驱动）
  - 需要高性能和低延迟的场景

- Realtek RTL8139

  **类型**：模拟的 Realtek 8139 百兆网卡。

  **特点：**

  - 兼容性极高，支持几乎所有操作系统
  - 性能较低，适合轻量级任务

  **使用场景**：

  - 需要高兼容性的场景（如 Windows XP 或较旧的 Linux 发行版）
  - 对性能要求不高的虚拟机

- Vmware vmxnel3

  **类型**：VMware 的准虚拟化网络适配器

  **特点：**

  - 高性能，专为 VMware 环境优化
  - 需要虚拟机操作系统支持 VMware Tools
  - 支持多队列（Multi-Queue），适合高并发场景

  **使用场景：**

  - VMware 环境中的虚拟机
  - 需要高性能和低延迟的场景。

  | 网络适配器类型  | 兼容性 | 性能 |                   使用场景                    |
  | :-------------: | :----: | :--: | :-------------------------------------------: |
  |   Intel E1000   |   高   |  低  |     需要高兼容性的场景（如 Windows XP）。     |
  |  Intel E1000e   |  较高  |  中  |         需要兼容性和中等性能的场景。          |
  |     Virtio      |  较高  |  高  | 需要高性能的场景（如 Linux 或较新 Windows）。 |
  | Realtek RTL8139 |  极高  |  低  |     需要高兼容性的场景（如 Windows XP）。     |
  | VMware vmxnet3  |  较高  |  高  |        VMware 环境中需要高性能的场景。        |

  