# Go pl

## 1. 输入输出

### 1.1 基本的IO接口

## 2. 字符串操作

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

### 2.1 字符串比较

- Compare

  ```go
  // Compare 函数，用于比较两个字符串的大小，如果两个字符串相等，返回为 0。如果 a 小于 b ，返回 -1 ，反之返回 1 。不推荐使用这个函数，直接使用 == != > < >= <= 等一系列运算符更加直观。
  func Compare(a, b string) int 
  
  ```

- EqualFold

  ```go
  // //   EqualFold 函数，计算 s 与 t 忽略字母大小写后是否相等。
  func EqualFold(s, t string) bool
  
  ```

### 2.2 是否存在某个字符或字串

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

### 2.3 子串出现次数 ( 字符串匹配 )

在数据结构与算法中，可能会讲解以下字符串匹配算法：

- 朴素匹配算法
- KMP 算法
- Rabin-Karp 算法
- Boyer-Moore 算法

在 Go 中，查找子串出现次数即字符串模式匹配，实现的是 Rabin-Karp 算法。Count 函数的签名如下

```go
func Count(s, sep string) int
```

### 2.4 字符串分割为[]string

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

### 2.5 字符串是否有某个前缀或后缀

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

### 2.6 字符或子串在字符串中出现的位置

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

### 2.7 字符串 JOIN 操作

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

### 2.8 字符串重复几次

将 s 重复 count 次，如果 count 为负数或返回值长度 len(s)*count 超出 string 上限会导致 panic，这个函数使用很简单：

```go
func Repeat(s string, count int) string
```

### 2.9 字符替换

Map 函数，将 s 的每一个字符按照 mapping 的规则做映射替换，如果 mapping 返回值  <0 ，则舍弃该字符。该方法只能对每一个字符做处理，但处理方式很灵活，可以方便的过滤，筛选汉字等

```go
func Map(mapping func(rune) rune, s string) string
```

### 2.10 字符串子串替换

```go

// 如果 n < 0，则不限制替换次数，即全部替换
func Replace(s, old, new string, n int) string

// 该函数内部直接调用了函数 Replace(s, old, new , -1)
func ReplaceAll(s, old, new string) string
```

### 2.11 大小写转换

```go
func ToLower(s string) string
func ToLowerSpecial(c unicode.SpecialCase, s string) string
func ToUpper(s string) string
func ToUpperSpecial(c unicode.SpecialCase, s string) string
```

### 2.12 标题处理

标题处理包含 3 个相关函数，其中 Title 会将 s 每个单词的首字母大写，不处理该单词的后续字符。ToTitle 将 s 的每个字母大写。ToTitleSpecial 将 s 的每个字母大写，并且会将一些特殊字母转换为其对应的特殊大写字母。

```go
func Title(s string) string
func ToTitle(s string) string
func ToTitleSpecial(c unicode.SpecialCase, s string) string
```

### 2.13 修剪

```go
// 将 s 左侧和右侧中匹配 cutset 中的任一字符的字符去掉
func Trim(s string, cutset string) string
// 将 s 左侧的匹配 cutset 中的任一字符的字符去掉
func TrimLeft(s string, cutset string) string
// 将 s 右侧的匹配 cutset 中的任一字符的字符去掉
func TrimRight(s string, cutset string) string
// 如果 s 的前缀为 prefix 则返回去掉前缀后的 string , 否则 s 没有变化。
func TrimPrefix(s, prefix string) string
// 如果 s 的后缀为 suffix 则返回去掉后缀后的 string , 否则 s 没有变化。
func TrimSuffix(s, suffix string) string
// 将 s 左侧和右侧的间隔符去掉。常见间隔符包括：'\t', '\n', '\v', '\f', '\r', ' ', U+0085 (NEL)
func TrimSpace(s string) string
// 将 s 左侧和右侧的匹配 f 的字符去掉
func TrimFunc(s string, f func(rune) bool) string
// 将 s 左侧的匹配 f 的字符去掉
func TrimLeftFunc(s string, f func(rune) bool) string
// 将 s 右侧的匹配 f 的字符去掉
func TrimRightFunc(s string, f func(rune) bool) string
```

### 2.14 Replacer 类型

这是一个结构，没有导出任何字段，实例化通过 `func NewReplacer(oldnew ...string) *Replacer` 函数进行，其中不定参数 oldnew 是 old-new 对，即进行多个替换。如果 oldnew 长度与奇数，会导致 panic.

示例：

```go
r := strings.NewReplacer("<", "&lt;", ">", "&gt;")
fmt.Println(r.Replace("This is <b>HTML</b>!"))
```

输出结果：

```go
This is &lt;b&gt;HTML&lt;/b&gt;!
```

另外，Replacer 还提供了另外一个方法，它在替换之后将结果写入 io.Writer 中。

```go
func (r *Replacer) WriteString(w io.Writer, s string) (n int, err error)
```

### 2.15 Reader 类型

看到名字就能猜到，这是实现了 `io` 包中的接口。它实现了 io.Reader（Read  方法），io.ReaderAt（ReadAt 方法），io.Seeker（Seek 方法），io.WriterTo（WriteTo  方法），io.ByteReader（ReadByte 方法），io.ByteScanner（ReadByte 和 UnreadByte  方法），io.RuneReader（ReadRune 方法） 和 io.RuneScanner（ReadRune 和 UnreadRune  方法）。

Reader 结构如下：

```go
type Reader struct {
  s        string    // Reader 读取的数据来源
  i        int // current reading index（当前读的索引位置）
  prevRune int // index of previous rune; or < 0（前一个读取的 rune 索引位置）
}
```

可见 Reader 结构没有导出任何字段，而是提供一个实例化方法：

```go
func NewReader(s string) *Reader
```

该方法接收一个字符串，返回的 Reader 实例就是从该参数字符串读数据。在后面学习了 bytes 包之后，可以知道 bytes.NewBufferString 有类似的功能，不过，如果只是为了读取，NewReader 会更高效。

其他方法不介绍了，都是之前接口的实现，有兴趣的可以看看源码实现，大部分都是根据 i、prevRune 两个属性来控制。

### 2.16 Builder 类型

该类型实现了 io 包下的 Writer, ByteWriter, StringWriter 等接口，可以向该对象内写入数据，Builder 没有实现 Reader 等接口，所以该类型不可读，但提供了 String 方法可以获取对象内的数据。

```go
type Builder struct {
    addr *Builder // of receiver, to detect copies by value
    buf  []byte
}
```

```go
// 该方法向 b 写入一个字节
func (b *Builder) WriteByte(c byte) error
// WriteRune 方法向 b 写入一个字符
func (b *Builder) WriteRune(r rune) (int, error)
// WriteRune 方法向 b 写入字节数组 p
func (b *Builder) Write(p []byte) (int, error)
// WriteRune 方法向 b 写入字符串 s
func (b *Builder) WriteString(s string) (int, error)
// Len 方法返回 b 的数据长度。
func (b *Builder) Len() int
// Cap 方法返回 b 的 cap。
func (b *Builder) Cap() int
// Grow 方法将 b 的 cap 至少增加 n (可能会更多)。如果 n 为负数，会导致 panic。
func (b *Builder) Grow(n int)
// Reset 方法将 b 清空 b 的所有内容。
func (b *Builder) Reset()
// String 方法将 b 的数据以 string 类型返回。
func (b *Builder) String() string
```

Builder 有 4 个与写入相关的方法，这 4 个方法的 error 都总是为 nil.

Builder 的 cap 会自动增长，一般不需要手动调用 Grow 方法。

String 方法可以方便的获取 Builder 的内容。

 举个例子：

```go
b := strings.Builder{}
_ = b.WriteByte('7')
n, _ := b.WriteRune('夕')
fmt.Println(n)
n, _ = b.Write([]byte("Hello, World"))
fmt.Println(n)
n, _ = b.WriteString("你好，世界")
fmt.Println(n)
fmt.Println(b.Len())
fmt.Println(b.Cap())
b.Grow(100)
fmt.Println(b.Len())
fmt.Println(b.Cap())
fmt.Println(b.String())
b.Reset()
fmt.Println(b.String())
```

 输出结果：

```bash
3
12
15
31
32
31
164
7夕Hello, World你好，世界
```
