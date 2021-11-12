# Go pl



## 字符串操作

字符串常见操作

- 字符串长度；
- 求子串；
- 是否存在某个字符或子串；
- 子串出现的次数（字符串匹配）；
- 字符串分割（切分）为[]string；
- 字符串是否有某个前缀或后缀；
- 字符或子串在字符串中首次出现的位置或最后一次出现的位置；
- 通过某个字符串将[]string 连接起来；
- 字符串重复几次；
- 字符串中子串替换；
- 大小写转换；
- Trim 操作；
- ...

### 字符串比较

-  Compare 

  ```go
  // Compare 函数，用于比较两个字符串的大小，如果两个字符串相等，返回为 0。如果 a 小于 b ，返回 -1 ，反之返回 1 。不推荐使用这个函数，直接使用 == != > < >= <= 等一系列运算符更加直观。
  func Compare(a, b string) int 
  
  ```

- EqualFold 

  ```go
  // //   EqualFold 函数，计算 s 与 t 忽略字母大小写后是否相等。
  func EqualFold(s, t string) bool
  
  ```


### 是否存在某个字符或字串

- Contains  子串 substr 在 s 中，返回 true

  ```go
  	name := "hello golang"
  	a := strings.Contains(name, " ")
  	fmt.Printf("%v", a)
  
  ```

- ContainsAny chars 中任何一个 Unicode 代码点在 s 中

  ```go
  	name := "hello golang"
  	a :=strings.ContainsAny(name, " & i")
  	fmt.Printf("%v", a)
  ```

- ContainsRune Unicode 代码点 r 在 s 中，返回 true

  ```go
  	name := "hello golang"
  	a :=strings.ContainsRune(name, ' ')
  	fmt.Printf("%v", a)
  ```


### 子串出现次数 ( 字符串匹配 )

在数据结构与算法中，可能会讲解以下字符串匹配算法：

- 朴素匹配算法
- KMP 算法
- Rabin-Karp 算法
- Boyer-Moore 算法

在 Go 中，查找子串出现次数即字符串模式匹配，实现的是 Rabin-Karp 算法。Count 函数的签名如下

```go
func Count(s, sep string) int
```

