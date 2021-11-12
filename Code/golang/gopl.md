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

### 字符串分割为[]string

这个需求很常见，倒不一定是为了得到[]string。

该包提供了六个三组分割函数：Fields 和 FieldsFunc、Split 和 SplitAfter、SplitN 和 SplitAfterN。

- Fields 用一个或多个连续的空格分隔字符串
- FieldsFunc 用这样的 Unicode 代码点 c 进行分隔：满足 f(c) 返回 true

- Split 会将 s 中的 sep 去掉
- SplitAfter 会保留 sep
- 带 N 的方法可以通过最后一个参数 n 控制返回的结果中的 slice 中的元素个数，当 n < 0 时，返回所有的子字符串；当 n == 0 时，返回的结果是 nil；当 n > 0 时，表示返回的 slice 中最多只有 n 个元素，其中，最后一个元素不会分割

```go
fmt.Printf("%q\n", strings.Split("a,b,c", ",")) // ["a" "b" "c"]
fmt.Printf("%q\n", strings.Split("a man a plan a canal panama", "a ")) // ["" "man " "plan " "canal panama"]
fmt.Printf("%q\n", strings.Split(" xyz ", "")) // [" " "x" "y" "z" " "]
fmt.Printf("%q\n", strings.Split("", "Bernardo O'Higgins")) // [""]
```

### 	字符串是否有某个前缀或后缀

- HasPrefix

  ```go
  // s 中是否以 prefix 开始
  func HasPrefix(s, prefix string) bool {
    return len(s) >= len(prefix) && s[0:len(prefix)] == prefix
  }
  ```

- HasSuffix

  ```go
  
  // s 中是否以 suffix 结尾
  func HasSuffix(s, suffix string) bool {
    return len(s) >= len(suffix) && s[len(s)-len(suffix):] == suffix
  }
  ```

### 字符或子串在字符串中出现的位置

```go
// 在 s 中查找 sep 的第一次出现，返回第一次出现的索引
func Index(s, sep string) int
// 在 s 中查找字节 c 的第一次出现，返回第一次出现的索引
func IndexByte(s string, c byte) int
// chars 中任何一个 Unicode 代码点在 s 中首次出现的位置
func IndexAny(s, chars string) int
// 查找字符 c 在 s 中第一次出现的位置，其中 c 满足 f(c) 返回 true
func IndexFunc(s string, f func(rune) bool) int
// Unicode 代码点 r 在 s 中第一次出现的位置
func IndexRune(s string, r rune) int

// 有三个对应的查找最后一次出现的位置
func LastIndex(s, sep string) int
func LastIndexByte(s string, c byte) int
func LastIndexAny(s, chars string) int
func LastIndexFunc(s string, f func(rune) bool) int
```

### 字符串 JOIN 操作

将字符串数组（或 slice）连接起来可以通过 Join 实现，函数签名如下：

```go
func Join(a []string, sep string) string
```

假如没有这个库函数，我们自己实现一个，我们会这么实现：

```go
func Join(str []string, sep string) string {
  // 特殊情况应该做处理
  if len(str) == 0 {
      return ""
  }
  if len(str) == 1 {
      return str[0]
  }
  buffer := bytes.NewBufferString(str[0])
  for _, s := range str[1:] {
      buffer.WriteString(sep)
      buffer.WriteString(s)
  }
  return buffer.String()
}
```
