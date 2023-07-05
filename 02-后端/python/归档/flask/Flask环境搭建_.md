# Flask环境搭建

## 前期准备

1. 安装插件

    sudo pip3 install virtualenv

    sudo pip3 install virtualenvwrapper

## 卸载插件

    sudo pip uninstall 插件包

2. 配置环境变量

``` python
# 1、创建目录用来存放虚拟环境
mkdir
$HOME/.virtualenvs

# 2、打开~/.bashrc文件，并添加如下：
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

# 3、运行
source ~/.bashrc
```

调出所有虚拟环境 workon

1. 删除遗留虚拟环境 rmvirtualenv

2. 安装虚拟环境 mkvirtual -p python3 虚拟环境名称

3. 准备依赖包

    1. pip list 列出开发环境的所有依赖包

    2. pip freeze > requirements.txt 导出成文件

    3. 调用(新建虚拟环境安装依赖) pip install -r requirements.txt

4. 进入虚拟环境 workon 虚拟环境名

5. 退出虚拟环境 deactivate

其他命令：lsof -i:5000

## windows 下虚拟环境搭建

1. 安装virtualenv

    pip install virtualenv

2. 新建虚拟环境

    virtualenv 虚拟环境名

    注：虚拟环境位于当前命令的目录下

3. 进入虚拟环境

    1) 进入虚拟环境目录： cd C:\Users\WEi\venv>

    2) 进入脚本目录：     C:\Users\WEi\venv\django_py3\Scripts>

    3) 运行activate.bat:  activate.bat

4. 安装依赖包
5. 退出虚拟环境

    deactivate.bat

6. 安装 virtualenvwrapper

    pip install virtualenvwrapper-win

    注： linux下运行pip install virtualenvwrapper

7. 设置WORK_HOME环境变量
    windows 右键我的电脑  属性-->高级系统设置-->环境变量-->系统变量
    变量名:WORKON_HOME
    变量值:C:\Users\WEi\venv(虚拟环境总目录)
