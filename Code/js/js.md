

## 1. 生成网卡地址代码

```js
 function randomMac() {
      const mac = [
        (0x52).toString(16),
        (0x16).toString(16),
        (0x3e).toString(16),
        Math.floor((Math.random() * 0xff)).toString(16),
        Math.floor((Math.random() * 0xff)).toString(16),
        Math.floor((Math.random() * 0xff)).toString(16)
      ]
      return mac.join(':')
    }
```

## 2. 时间格式化

```js
	//  格式化时间
	let dt = new Date()
	let yyyy = dt.getFullYear()
	let MM = (dt.getMonth() +1).toString().padStart(2, '0')
	let dd = dt.getDate().toString().padStart(2, '0')
	let h = dt.getHours().toString().padStart(2, '0')
	let m = dt.getMinutes().toString().padStart(2, '0')
	let s = dt.getSeconds().toString().padStart(2, '0')
	const time = yyyy + MM +dd + '_' + h  + m + s
```

