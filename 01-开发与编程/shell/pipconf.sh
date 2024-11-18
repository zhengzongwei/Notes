#!/bin/bash

pip_conf_context="
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
"

function pip_conf(){

    # 检查pip文件夹是否存在
    if [ ! -d $HOME/.pip ];then
        mkdir $HOME/.pip
    fi
    pip_conf_file=$HOME/.pip/pip.conf
    cat > $pip_conf_file << EOF
    ${pip_conf_context}
EOF
}


function usage(){
    

}

function main(){
    usage
}

main
