# Go语言从入门到进阶实战



## Base64 编码格式

```go
package main

import (
	"encoding/base64"
	"fmt"
)

func main() {
	message := "你好， 每日一码。"
	encodeMessage := base64.StdEncoding.EncodeToString([]byte(message))

	// 编码信息
	fmt.Println(encodeMessage)

	// 解码
	data, err := base64.StdEncoding.DecodeString(encodeMessage)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(string(data))
	}
}
```

