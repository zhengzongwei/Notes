```shell
version: "3"

services:
  mariadb:
    image: "mariadb:${MARIADB_TAG}"
    container_name: mariadb
    environment:
      - MARIADB_ROOT_PASSWORD=${MARIADB_ROOT_PASSWORD}
      - MARIADB_USER=${MARIADB_USER}
      - MARIADB_PASSWORD=${MARIADB_PASSWORD}
    restart: always
    volumes:
      - ./mariadb/data:/var/lib/mysql
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "${MARIADB_PORT}:3306" 
      
      

# MARIADB
MARIADB_TAG=10.10.2
MARIADB_ROOT_PASSWORD=mysql
MARIADB_ALLOW_EMPTY_ROOT_PASSWORD=yes
MARIADB_USER=zhengzongwei
MARIADB_PASSWORD=zhengzongwei
MARIADB_PORT=16030
```
