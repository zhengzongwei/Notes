# jellyfin 部署

```dockerfile
version: '3'

services:
  # jellyfin
  jellyfin:
    image: jellyfin/jellyfin:latest
    container_name: nas_jellyfin
    volumes:
      - ./config:/config
      - ./cache:/cache
      - ./dejavu:/usr/share/fonts/truetype/dejavu  # 配置字体
      - /path/to/your/media:/media  # 媒体库位置
      - /etc/localtime:/etc/localtime:ro
      - /etc/timezone:/etc/timezone:ro
    devices:
      - /dev/dri:/dev/dri  # 核显
    user: "1000:1000"  # 用户uid:组gid
    group_add:
      - '109'  # render组
    extra_hosts:
      - "api.themoviedb.org:13.224.161.90"  # themoviedbDNS问题
    ports:
      - "8096:8096"
    restart: unless-stopped
```

