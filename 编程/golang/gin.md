 

# Gin

```go

// 安装 gin
go get github.com/gin-gonic/gin

// 创建项目目录
mkdir web-app

// 项目根目录执行
go mod init
```



## 安装 gin

```go
go get github.com/gin-gonic/gin
```



##  创建

```go
package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
)

func main() {
	S := gin.Default()
	S.GET("/", func(c *gin.Context) {
		c.JSON(200, gin.H{"msg": "服务启动成功"})
	})
	err := S.Run(":8080")
	if err != nil {
		fmt.Println("服务器启动失败！")
	}
}
```

