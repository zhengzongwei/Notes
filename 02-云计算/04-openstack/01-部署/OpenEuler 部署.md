# 基于OpenStack SIG开发工具快速部署

1. 安装`oos`工具

   ```bash
   pip install openstack-sig-tool click panda pyyaml requests
   ```

2. 配置open stack环境信息

   ```bash
   vi /usr/local/etc/oos/oos.conf
   
   [environment]
   mysql_root_password = admin
   mysql_project_password = admin
   rabbitmq_password = admin
   project_identity_password = admin
   enabled_service = keystone,neutron,cinder,placement,nova,glance,horizon,aodh,ceilometer,cyborg,gnocchi,kolla,heat,trove,tempest
   neutron_provider_interface_name = br-ex
   default_ext_subnet_range = 10.100.100.0/24
   default_ext_subnet_gateway = 10.100.100.1
   neutron_dataplane_interface_name = eth1
   cinder_block_device = vdb
   swift_storage_devices = vdc
   swift_hash_path_suffix = ash
   swift_hash_path_prefix = has
   glance_api_workers = 2
   cinder_api_workers = 2
   nova_api_workers = 2
   nova_metadata_api_workers = 2
   nova_conductor_workers = 2
   nova_scheduler_workers = 2
   neutron_api_workers = 2
   horizon_allowed_host = *
   kolla_openeuler_plugin = false
   ```

   | 配置项                           | 解释                                                         |
   | -------------------------------- | ------------------------------------------------------------ |
   | enabled_service                  | 安装服务列表，根据用户需求自行删减                           |
   | neutron_provider_interface_name  | neutron L3网桥名称                                           |
   | default_ext_subnet_range         | neutron私网IP段                                              |
   | default_ext_subnet_gateway       | neutron私网gateway                                           |
   | neutron_dataplane_interface_name | neutron使用的网卡，推荐使用一张新的网卡，以免和现有网卡冲突，防止all in one主机断连的情况 |
   | cinder_block_device              | cinder使用的卷设备名                                         |
   | swift_storage_devices            | swift使用的卷设备名                                          |
   | kolla_openeuler_plugin           | 是否启用kolla plugin。设置为True，kolla将支持部署openEuler容器 |

3. 部署OpenStack `all in one`

   ```bash
   dnf install sshpass
   
   # 替换TARGET_MACHINE_IP为目标机ip、TARGET_MACHINE_PASSWD为目标机密码。
   oos env manage -r 22.03-lts -i TARGET_MACHINE_IP -p TARGET_MACHINE_PASSWD -n test-oos
   
   oos env manage -r 22.03-lts -i 192.168.31.254 -p openeuler -n openstack
   
   oos env manage -r 22.03-lts -i 10.211.55.4 -p openeuler -n openstack
   
   
   oos env setup openstack -r wallaby
   ```

4. 初始化tempest环境

   ```bash
   oos env init test-oos
   ```

   

## 问题记录

### `An exception occurred during task execution. To see the full traceback, use -vvv. The error was: AttributeError: module 'lib' has no attribute 'X509_V_FLAG_CB_ISSUER_CHECK'`

```bash
pip install -U pyOpenSSL
```

### `fatal: [controller]: FAILED! => {"changed": true, "cmd": "keystone-manage db_sync", "delta": "0:00:01.713579", "end": "2023-12-19 15:32:56.978664", "msg": "non-zero return code", "rc": 1, "start": "2023-12-19 15:32:55.265085", "stderr": "Traceback (most recent call last):\n  File \"/usr/bin/keystone-manage\", line 6, in <module>\n    from keystone.cmd.manage import main\n  File \"/usr/lib/python3.9/site-packages/keystone/cmd/manage.py\", line 19, in <module>\n    from keystone.cmd import cli\n  File \"/usr/lib/python3.9/site-packages/keystone/cmd/cli.py\", line 28, in <module>\n    from keystone.cmd import bootstrap\n  File \"/usr/lib/python3.9/site-packages/keystone/cmd/bootstrap.py\", line 21, in <module>\n    from keystone.server import backends\n  File \"/usr/lib/python3.9/site-packages/keystone/server/__init__.py\", line 19, in <module>\n    from keystone.server import backends\n  File \"/usr/lib/python3.9/site-packages/keystone/server/backends.py\", line 16, in <module>\n    from keystone import application_credential\n  File \"/usr/lib/python3.9/site-packages/keystone/application_credential/__init__.py\", line 13, in <module>\n    from keystone.application_credential.core import *  # noqa\n  File \"/usr/lib/python3.9/site-packages/keystone/application_credential/core.py\", line 23, in <module>\n    from keystone import notifications\n  File \"/usr/lib/python3.9/site-packages/keystone/notifications.py\", line 22, in <module>\n    import flask\n  File \"/usr/lib/python3.9/site-packages/flask/__init__.py\", line 14, in <module>\n    from jinja2 import escape\nImportError: cannot import name 'escape' from 'jinja2' (/usr/local/lib/python3.9/site-packages/jinja2/__init__.py)", "stderr_lines": ["Traceback (most recent call last):", "  File \"/usr/bin/keystone-manage\", line 6, in <module>", "    from keystone.cmd.manage import main", "  File \"/usr/lib/python3.9/site-packages/keystone/cmd/manage.py\", line 19, in <module>", "    from keystone.cmd import cli", "  File \"/usr/lib/python3.9/site-packages/keystone/cmd/cli.py\", line 28, in <module>", "    from keystone.cmd import bootstrap", "  File \"/usr/lib/python3.9/site-packages/keystone/cmd/bootstrap.py\", line 21, in <module>", "    from keystone.server import backends", "  File \"/usr/lib/python3.9/site-packages/keystone/server/__init__.py\", line 19, in <module>", "    from keystone.server import backends", "  File \"/usr/lib/python3.9/site-packages/keystone/server/backends.py\", line 16, in <module>", "    from keystone import application_credential", "  File \"/usr/lib/python3.9/site-packages/keystone/application_credential/__init__.py\", line 13, in <module>", "    from keystone.application_credential.core import *  # noqa", "  File \"/usr/lib/python3.9/site-packages/keystone/application_credential/core.py\", line 23, in <module>", "    from keystone import notifications", "  File \"/usr/lib/python3.9/site-packages/keystone/notifications.py\", line 22, in <module>", "    import flask", "  File \"/usr/lib/python3.9/site-packages/flask/__init__.py\", line 14, in <module>", "    from jinja2 import escape", "ImportError: cannot import name 'escape' from 'jinja2' (/usr/local/lib/python3.9/site-packages/jinja2/__init__.py)"], "stdout": "", "stdout_lines": []}`

```bash
pip install -U Flask-RESTful
```

### fatal: [controller]: FAILED! => {"msg": "The task includes an option with an undefined variable. The error was: 'dict object' has no attribute 'ipv4'\n\nThe error appears to be in '/usr/local/etc/oos/playbooks/neutron.yaml': line 138, column 7, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n\n    - name: Initialize linux-bridge config file\n      ^ here\n"}

