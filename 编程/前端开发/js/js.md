# JS

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

// 完整生成mac地址
function randomMac() {
    const mac = [
      (0x52).toString(16),
      (0x16).toString(16),
      (0x3e).toString(16),

    ]

    for(let i=0;i<3;i++){
        let tmp_mac = Math.floor((Math.random() * 0xff)).toString(16)
        if(tmp_mac.length==1){
            tmp_mac = tmp_mac + "0"
            mac.push(tmp_mac)
        }else{
            mac.push(tmp_mac)
        }
    }
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
    
    
    // 标准时间格式化
    function formatDate(time){
        var date = new Date(time);

        var year = date.getFullYear(),
            month = date.getMonth() + 1,//月份是从0开始的
            day = date.getDate(),
            hour = date.getHours(),
            min = date.getMinutes(),
            sec = date.getSeconds();
        var newTime = year + '-' +
                    month + '-' +
                    day + ' ' +
                    hour + ':' +
                    min + ':' +
                    sec;
        return newTime; 
    }

```
