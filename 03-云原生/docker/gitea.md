# gitea



## gitea

docker-compose

```shell
version: "3"

networks:
  gitea:
    external: false

services:
  serveer:
    image: gitea/gitea:1.18.3
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
    restart: always
    networks:
      - gitea
    volumes:
      - ./data:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    ports:
      - "9527:3000"
      - "9528:22"
```



