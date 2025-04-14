# harbor 安装

## 安装

1. 下载离线安装包

   - tar包

      https://github.com/goharbor/harbor/releases/download/v2.13.0/harbor-offline-installer-v2.13.0.tgz

   - md5

     https://github.com/goharbor/harbor/releases/download/v2.13.0/md5sum

   

2. 解压

   ```sh
   tar xzvf harbor-offline-installer-version.tgz
   ```

## 生成证书

### 生成证书颁发机构证书

1. 生成CA证书私钥

   ```shell
   openssl genrsa -out ca.key 4096
   ```

2. 生成CA证书

   ```shell
   openssl req -x509 -new -nodes -sha512 -days 3650 \
    -subj "/C=CN/ST=Beijing/L=Beijing/O=example/OU=Personal/CN=MyPersonal Root CA" \
    -key ca.key \
    -out ca.crt
   ```

### 生成服务器证书

1. 创建配置文件

   - registry.cnf

     ```shell
     [req]
     distinguished_name = req_distinguished_name
     req_extensions = v3_req
     prompt = no
     
     [req_distinguished_name]
     C = CN
     ST = Beijing
     L = Beijing
     O = MyOrg
     OU = Dev
     CN = registry.dev.com  # 必须与Harbor访问域名一致
     
     [v3_req]
     basicConstraints = CA:FALSE
     keyUsage = digitalSignature, keyEncipherment
     extendedKeyUsage = serverAuth
     subjectAltName = @alt_names
     
     [alt_names]
     DNS.1 = registry.dev.com  # 主域名
     DNS.2 = registry          # 局域网短名（可选）
     # 如果有IP访问需求，添加：
     # IP.1 = 192.168.1.100
     ```

2. 生成私钥和证书签名请求（CSR）

   ```shell
   openssl genrsa -out registry.dev.com.key 4096
   openssl req -new -sha256 -key registry.dev.com.key \
     -out registry.dev.com.csr \
     -config registry.cnf
   ```

   

3. 用CA证书签发Harbor证书

   ```shell
   openssl x509 -req -sha256 -days 3650 \
     -in registry.dev.com.csr \
     -CA ca.crt \
     -CAkey ca.key \
     -CAcreateserial \
     -out registry.dev.com.crt \
     -extfile registry.cnf \
     -extensions v3_req
   ```

4. 合并证书链（Harbor要求）

   `cat registry.dev.com.crt ca.crt > registry.dev.com.combined.crt`

   ```shell
   # 将证书文件放入Harbor目录
   mkdir -p /data/cert/
   cp registry.dev.com.combined.crt registry.dev.com.key /data/cert/
   
   # 修改Harbor配置文件 harbor.yml
   https:
     certificate: /data/cert/registry.dev.com.combined.crt
     private_key: /data/cert/registry.dev.com.key
   hostname: registry.dev.com  # 必须与证书CN一致
   
   # 重启Harbor
   docker-compose down -v && docker-compose up -d
   ```

### 客户端配置

- Linux/Mac

  ```shell
  # 将CA证书加入系统信任
  sudo cp ca.crt /usr/local/share/ca-certificates/
  sudo update-ca-certificates
  
  # 测试连接
  curl -vk https://registry.dev.com/api/v2.0/health
  ```

- Docker客户端

  ```shell
  # 编辑Docker配置
  sudo mkdir -p /etc/docker/certs.d/registry.dev.com
  sudo cp ca.crt /etc/docker/certs.d/registry.dev.com/ca.crt
  
  # 重启Docker
  sudo systemctl restart docker
  
  # 测试登录
  docker login registry.dev.com
  ```

  

## 参考链接

1. [Harbor 文档 | Harbor 安装前提条件 - Harbor 中文](https://harbor.k8s.ac.cn/docs/2.11.0/install-config/installation-prereqs/)

   