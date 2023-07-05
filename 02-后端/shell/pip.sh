#!/usr/bin/env bash

msg() {
  printf '%b\n' "$1" >&2
}

tips() {
  msg "\33[36m[*]\33[0m ${1}${2}"
}

success() {
  msg "\33[32m[✔]\33[0m ${1}${2}"
}

error() {
  msg "\33[31m[✘]\33[0m ${1}${2}"
  exit 1
}

tips "Config Pipy"

function configPipy() {

pip_config="
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
"
mkdir -p ~/.pip/
    tee > ~/.pip/pip.conf <<EOF
$pip_config
EOF

}

configPipy

success "Config PiPy done."