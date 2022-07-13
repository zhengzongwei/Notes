## API参数

```json
# 创建 flavors
URL: https://192.168.86.34/portal/api/instances/bfc/flavors
POST
{
  "name": "BAIDU1C1G", // 名称
  "vcpus": 1,  // CPU
  "ram": 1024, // 内存
  "cpu_percent": 1, // CPU利用率
  "flavor_type": "gpu_instances", // 计算类型
          
  // "dev_class": "gpu",  // GPU类型
  // "dev_type": "BAIDU_XPU", // GPU型号
  // "dev_num": 1,  // GPU数量
  // "label_name": "BAIDU_XPU（undefined）" // GPU名称
  
  "gpu_info":[
    {
        
  			"dev_class": "gpu",  // GPU类型
  			"dev_type": "BAIDU_XPU", // GPU型号
  			"dev_num": 1,  // GPU数量
  			"label_name": "BAIDU_XPU（undefined）" // GPU名称
    },
    {
        "dev_class": "gpu",
    		"dev_type": "HUAWEI_NPU",
    		"dev_num": 1,
    		"label_name": "HUAWEI_NPU（undefined）"
    }
  ]
}


{
    "name": "tt",
    "vcpus": 1,
    "ram": 1024,
    "cpu_percent": 1,
    "flavor_type": "gpu_instances",
    "dev_class": "gpu",
    "dev_type": "HUAWEI_NPU",
    "dev_num": 1,
    "label_name": "HUAWEI_NPU（undefined）"
}
// 普通计算规格

{
    "name": "1C1G",
    "vcpus": 1,
    "ram": 1024,
    "cpu_percent": 1,
    "flavor_type": "instance"
}


```



## 请求返回参数

```
{
    "message": null,
    "code": 0,
    "data": {
        "total": 2,
        "result": [
            {
                "name": "test",
                "cpu_percent": null,
                "ram": 1024,
                "ephemeral": 0,
                "vcpus": 1,
                "meta_data": {
                    "quota:cpu_quota": "100000",
                    "capabilities:hypervisor_type": "QEMU",
                    "dev_type": "AMD_S7150",
                    "quota:cpu_period": "100000",
                    "filter:gpu_instances_tag": "True",
                    "label_name": "AMD_S7150（8190 M）",
                    "hw:numa_nodes": "1",
                    "quota:soft_limit": "1024",
                    "dev_class": "gpu",
                    "dev_num": "1",
                    "pci_passthrough:alias": "AMD_S7150:1",
                    "hw:nochk_numa": "True"
                },
                "swap": 0,
                "is_used": false,
                "disk": 0,
                "id": "7bbbaa8d-f9e7-4ca7-a7d6-1a3a8610d77b"
            },
            {
                "name": "BAIDU1C1G",
                "cpu_percent": null,
                "ram": 1024,
                "ephemeral": 0,
                "vcpus": 1,
                "meta_data": {},
                "swap": 0,
                "is_used": false,
                "disk": 0,
                "id": "dc7f77e9-e3f6-4221-b0c7-c818206ac3ae"
            }
        ]
    }
}
```

