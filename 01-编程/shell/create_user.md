```shell
#!/usr/bin/env bash

USER_LIST=("zhengzongwei" "nieantai" "hujinyong")

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

create_user(){
  for USER in ${USER_LIST[*]};do
  tips "create user ${USER}"
  useradd -d /home/$USER -s /bin/bash -m $USER
  echo "$USER:$USER" | chpasswd

  success "create user ${USER} success!"
  done

}

create_user
```

