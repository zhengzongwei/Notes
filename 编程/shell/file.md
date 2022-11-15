```shell
##!/bin/bash



# Data Time
# DATE_TIME='date +%Y-%m-%d-%H:%M:%S's
# LOG_TIME = $($DATE_TIME)s

# PYTHON_PATH = '/usr/lib/python2.7/site-packages/'


upFile(){

    echo "Updating file"
    #   将文件上传到服务器
    scp ${FilePath} ${$username}@${password}:/home/

    if [ $? -eq 0 ];then
        echo "File upload success"
    else
        echo "File upload failed"
    fi

    # connectRemoteHost $1 $2 $3

}



downloadFile(){
    echo "Downloading file"

}

# connectRemoteHost(){
#     echo "Connecting to remote host "
#     username=$1
#     ip=$2
#     password=$3

#     echo "username: $username"
#     echo "IP: $ip"
#     echo "Password: $password"
#     expect -c "
#         set timeout 1
#!/bin/bash



# Data Time
# DATE_TIME='date +%Y-%m-%d-%H:%M:%S's
# LOG_TIME = $($DATE_TIME)s

# PYTHON_PATH = '/usr/lib/python2.7/site-packages/'


upFile(){

    echo "Updating file"
    #   将文件上传到服务器
    scp ${FilePath} ${$username}@${password}:/home/

    if [ $? -eq 0 ];then
        echo "File upload success"
    else
        echo "File upload failed"
    fi

    # connectRemoteHost $1 $2 $3

}



downloadFile(){
    echo "Downloading file"

}

# connectRemoteHost(){
#     echo "Connecting to remote host "
#     username=$1
#     ip=$2
#     password=$3

#     echo "username: $username"
#     echo "IP: $ip"
#     echo "Password: $password"
#     expect -c "
#         set timeout 1
#         spawn ssh ${username}@${ip};
#         expect {
#             *yes/no* { send \"yes\r\"; exp_continue }
#             *password* { send \"${password}\r\"; exp_continue}
#         }
#         interact
#     "
# }


# copyFileFromLocalToContainer(){
#     echo "Copying file from local to container"
# }

# copyFileFromContainerToLocal(){
#     # copy file from container to local
# }


# run(){
#     while [ -n "$1" ]; do
#         case $1 in
#         --help)
#             help
#             exit 0
#             ;;
        
#         esac
#         shift
#     done

# }

# run

main(){
    echo "Starting main"
    upFisle $1 $2 $3
    # downloadFile
    # connectRemoteHost
    # copyFileFromLocalToContainer
    # copyFileFromContainerToLocal

}

# connectRemoteHost $1 $2 $3
main $1 $2 $3

```

