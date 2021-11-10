# Go 语言注释规范

## 1. 项目结构

### 1.1 web框架

以下为一般项目结构，根据不同的 Web 框架习惯，可使用括号内的文字替换；根据不同的项目类型和需求，可自由增删某些结构：

    - templates (views)          # 模板文件
    - public (static)            # 静态文件
        - css                    
        - fonts                  
        - img                    
        - js                     
    - routers (controllers)      # 路由逻辑处理
    - models                     # 数据逻辑层
    - modules                    # 子模块
        - setting                # 应用配置存取
    - cmd                        # 命令行程序命令
    - conf                       # 默认配置
        - locale                 # i18n 本地化文件
    - custom                     # 自定义配置
    - data                       # 应用生成数据文件
    - log                        # 应用生成日志文件

### 1.2 命令行应用

当应用类型为命令行应用时，需要将命令相关文件存放于 `/cmd` 目录下，并为每个命令创建一个单独的源文件

    /cmd
    dump.go
    fix.go
    serve.go
    update.go
    web.go

## 2. 注释规范

### 2.1 注释的意义

- 注释可以帮我们很好的完成文档的工作，写得好的注释可以方便我们以后的维护。
- /**/ 的块注释和 // 的单行注释两种注释风格， 在我们的项目中为了风格的统一，全部使用单行注释，注释的质量决定了生成的文档的质量。
- 下面从包注释、结构体（接口）注释、函数（方法）注释、代码逻辑注释以及注释规范方面进行说明。

### 2.2 包注释

- 每个包都应该有一个包注释，一个位于 package 子句之前行注释

- 包注释应该包含下面基本信息

    ```go
    // @Title  请填写文件名称（需要改）
    // @Description  请填写文件描述（需要改）
    // @Author  请填写自己的真是姓名（需要改）  ${DATE} ${TIME}
    // @Update  请填写自己的真是姓名（需要改）  ${DATE} ${TIME}
    package ${GO_PACKAGE_NAME}
    
    /*
    * @Title common.go
    * @Description
    * @Author zhengzongwei 2021/11/10 10:16
    * @Update
    */
    
    ```


### 2.3 结构（接口）注释

每个自定义的结构体或者接口都应该有注释说明，该注释对结构进行简要介绍，放在结构体定义的前一行，格式为： 结构体名， 结构体说明。同时结构体内的每个成员变量都要有说明，该说明放在成员变量的后面（注意对齐），实例如下：

        // User   用户对象，定义了用户的基础信息
        type User struct{
            Username  string // 用户名
            Email     string // 邮箱
        }


### 2.4 函数（方法）注释

- 每个函数，或者方法（结构体或者接口下的函数称为方法）都应该有注释说明
- 函数的注释应该包括三个方面

    ```go
    // @title    函数名称
    // @description   函数的详细描述
    // @auth      作者             时间（2019/6/18   10:57 ）
    // @param     输入参数名        参数类型         "解释"
    // @return    返回参数名        参数类型         "解释"
    ```

### 2.5 代码逻辑注释

- 每个代码块都要添加单行注释
- 注视使用 TODO 开始 详细如下

    ```go
    // TODO  代码块的执行解释
    if   userAge < 18 {
    
    }

### 2.6 注释要求

- 统一使用中文注释，对于中英文字符之间严格使用空格分隔， 这个不仅仅是中文和英文之间，英文和中文标点之间也都要使用空格分隔
- 全部使用单行注释，禁止使用多行注释
- 和代码的规范一样，单行注释不要过长，禁止超过 120 字符。

### 2.7 缩进和折行

- 缩进必须使用 `gofmt` 工具格式化
- 折行方面，一行最长不超过 120 个字符，超过的请使用换行展示，尽量保持格式优雅

### 2.8 括号和空格

括号和空格方面，也可以直接使用 `gofmt` 工具格式化（go 会强制左大括号不换行，换行会报语法错误），所有的运算符和操作数之间要留空格。

### 2.9 其它说明

- 当某个部分等待完成时，可用 `TODO:` 开头的注释来提醒维护人员。
- 当某个部分存在已知问题进行需要修复或改进时，可用 `FIXME:` 开头的注释来提醒维护人员。
- 当需要特别说明某个问题时，可用 `NOTE:` 开头的注释：

    ```go
      // NOTE: os.Chmod and os.Chtimes don't recognize symbolic link,
      // which will lead "no such file or directory" error.
      return os.Symlink(target, dest)
    ```

### 2.10 注释模板

```go
/*
 * @Title common.go
 * @Description
 * @Author zheng 2021/11/10 10:16
 * @Update
 */

package common

import (
	"fmt"
	"time"
)

/*
 * @title FormatPrint
 * @description
 * @param
 * @return None
 */
func FormatPrint() {
	fmt.Printf("this is a common.go")
}

/*
 * @title TimeStamp()
 * @description Convert time to timestamp
 * @param None
 * @return currentTimeStamp int64 "timestamp"
 */
func TimeStamp() int64 {
	currentTimeStamp := time.Now().Unix()
	return currentTimeStamp
}

/*
 * @title NowTime
 * @description get current time
 * @param None
 * @return currentTime string "time"
 */
func NowTime() string {
	currentTime := time.Now().Format("2006-01-02 15:04:05")
	return currentTime
}

//TODO 创建一个记录程序运行时间的函数

```

## 3. 命名规范

### 3.1 文件名

- 整个应用或包的主入口文件应当是 `main.go` 或与应用名称简写相同。例如：`Gogs` 的主入口文件名为 `gogs.go`。

### 3.2 函数与方法

若函数或方法为判断类型（返回值主要为 `bool` 类型），则名称应以 `Has`, `Is`, `Can` 或 `Allow` 等判断性动词开头：

```go
  func HasPrefix(name string, prefixes []string) bool { ... }
  func IsEntry(name string, entries []string) bool { ... }
  func CanManage(name string) bool { ... }
  func AllowGitHook() bool { ... }
```

### 3.3 常量

- 常量均需使用全部大写字母组成，并使用下划线分词：

    ```go
      const APP_VER = "0.7.0.1110 Beta"
    ```
    
- 如果是枚举类型的常量，需要先创建相应类型：

    ```go
      type Scheme string
      const (
          HTTP  Scheme = "http"
          HTTPS Scheme = "https"
      )
    ```

- 如果模块的功能较为复杂、常量名称容易混淆的情况下，为了更好地区分枚举类型，可以使用完整的前缀：

    ```go
      type PullRequestStatus int
      const (
          PULL_REQUEST_STATUS_CONFLICT PullRequestStatus = iota
          PULL_REQUEST_STATUS_CHECKING
          PULL_REQUEST_STATUS_MERGEABLE
      )
    ```

### 3.4 变量

- 变量命名基本上遵循相应的英文表达或简写。

- 在相对简单的环境（对象数量少、针对性强）中，可以将一些名称由完整单词简写为单个字母，例如：

  - `user` 可以简写为 `u`
  - `userID` 可以简写 `uid`

- 若变量类型为 `bool` 类型，则名称应以 `Has`, `Is`, `Can` 或 `Allow` 开头：

  ```go
    var isExist bool
    var hasConflict bool
    var canManage bool
    var allowGitHook bool
  ```

- 上条规则也适用于结构定义：

     ```go
        // Webhook represents a web hook object.
        type Webhook struct {
            ID           int64 `xorm:"pk autoincr"`
            RepoID       int64
            OrgID        int64
            URL          string `xorm:"url TEXT"`
            ContentType  HookContentType
            Secret       string `xorm:"TEXT"`
            Events       string `xorm:"TEXT"`
            *HookEvent   `xorm:"-"`
            IsSSL        bool `xorm:"is_ssl"`
            IsActive     bool
            HookTaskType HookTaskType
            Meta         string     `xorm:"TEXT"` // store hook-specific attributes
            LastStatus   HookStatus // Last delivery status
            Created      time.Time  `xorm:"CREATED"`
            Updated      time.Time  `xorm:"UPDATED"`
        }
     ```

### 3.5 命名惯例

变量名称一般遵循驼峰法，但遇到特有名词时，需要遵循以下规则：

- 如果变量为私有，且特有名词为首个单词，则使用小写，如 `apiClient`。

- 其它情况都应当使用该名词原有的写法，如 `APIClient`、`repoID`、`UserID`。

  ```go
  // A GonicMapper that contains a list of common initialisms taken from golang/lint
  var LintGonicMapper = GonicMapper{
      "API":   true,
      "ASCII": true,
      "CPU":   true,
      "CSS":   true,
      "DNS":   true,
      "EOF":   true,
      "GUID":  true,
      "HTML":  true,
      "HTTP":  true,
      "HTTPS": true,
      "ID":    true,
      "IP":    true,
      "JSON":  true,
      "LHS":   true,
      "QPS":   true,
      "RAM":   true,
      "RHS":   true,
      "RPC":   true,
      "SLA":   true,
      "SMTP":  true,
      "SSH":   true,
      "TLS":   true,
      "TTL":   true,
      "UI":    true,
      "UID":   true,
      "UUID":  true,
      "URI":   true,
      "URL":   true,
      "UTF8":  true,
      "VM":    true,
      "XML":   true,
      "XSRF":  true,
      "XSS":   true,
  }
  ```

## 4. 导入规范

###  4.1 import规范

```go
// 单行引入
import  "fmt"

// 多包引入，每包独占一行
// 使用绝对路径，避免相对路径如 ../encoding/json
import (
"strings"
"fmt"
)
```

  ## 5. 声明语句

  ### 5.1 函数或方法

  函数或方法的参数排列顺序遵循以下几点原则（从左到右）：

  1. 参数的重要程度与逻辑顺序
  2. 简单类型优先于复杂类型
  3. 尽可能将同种类型的参数放在相邻位置，则只需写一次类型

  以下声明语句，`User` 类型要复杂于 `string` 类型，但由于 `Repository` 是 `User` 的附属品，首先确定 `User` 才能继而确定 `Repository`。因此，`User` 的顺序要优先于 `repoName`。

  ```go
  func IsRepositoryExist(user *User, repoName string) (bool, error) { ...
  ```


  ## 6. 代码指导

  ### 6.1 基本约束

  - 所有应用的 `main` 包需要有 `APP_VER` 常量表示版本，格式为 `X.Y.Z.Date [Status]`，例如：`0.7.6.1112 Beta`。
  
  - 单独的库需要有函数 `Version` 返回库版本号的字符串，格式为 `X.Y.Z[.Date]`。
  
  - 当单行代码超过 80 个字符时，就要考虑分行。分行的规则是以参数为单位将从较长的参数开始换行，以此类推直到每行长度合适：
  
    ```go
      So(z.ExtractTo(
          path.Join(os.TempDir(), "testdata/test2"),
          "dir/", "dir/bar", "readonly"), ShouldBeNil)
    ```
  
  - 当单行声明语句超过 80 个字符时，就要考虑分行。分行的规则是将参数按类型分组，紧接着的声明语句的是一个空行，以便和函数体区别：
  
    ```go
      // NewNode initializes and returns a new Node representation.
      func NewNode(
          importPath, downloadUrl string,
          tp RevisionType, val string,
          isGetDeps bool) *Node {
          n := &Node{
              Pkg: Pkg{
                  ImportPath: importPath,
                  RootPath:   GetRootPath(importPath),
                  Type:       tp,
                  Value:      val,
              },
              DownloadURL: downloadUrl,
              IsGetDeps:   isGetDeps,
          }
          n.InstallPath = path.Join(setting.InstallRepoPath, n.RootPath) + n.ValSuffix()
          return n
      }
    ```
  
  - 分组声明一般需要按照功能来区分，而不是将所有类型都分在一组：
  
    ```go
      const (
          // Default section name.
          DEFAULT_SECTION = "DEFAULT"
          // Maximum allowed depth when recursively substituing variable names.
          _DEPTH_VALUES = 200
      )
      type ParseError int
      const (
          ERR_SECTION_NOT_FOUND ParseError = iota + 1
          ERR_KEY_NOT_FOUND
          ERR_BLANK_SECTION_NAME
          ERR_COULD_NOT_PARSE
      )
    ```
  
  - 当一个源文件中存在多个相对独立的部分时，为方便区分，需使用由 [ASCII Generator](http://www.network-science.de/ascii/) 提供的句型字符标注（示例：`Comment`）：
  
    ```go
      // _________                                       __
      // \_   ___ \  ____   _____   _____   ____   _____/  |_
      // /    \  \/ /  _ \ /     \ /     \_/ __ \ /    \   __\
      // \     \___(  <_> )  Y Y  \  Y Y  \  ___/|   |  \  |
      //  \______  /\____/|__|_|  /__|_|  /\___  >___|  /__|
      //         \/             \/      \/     \/     \/
    ```
  
  - 函数或方法的顺序一般需要按照依赖关系由浅入深由上至下排序，即最底层的函数出现在最前面。例如，下方的代码，函数 `ExecCmdDirBytes` 属于最底层的函数，它被 `ExecCmdDir` 函数调用，而 `ExecCmdDir` 又被 `ExecCmd` 调用：
  
    ```go
      // ExecCmdDirBytes executes system command in given directory
      // and return stdout, stderr in bytes type, along with possible error.
      func ExecCmdDirBytes(dir, cmdName string, args ...string) ([]byte, []byte, error) {
          ...
      }
      // ExecCmdDir executes system command in given directory
      // and return stdout, stderr in string type, along with possible error.
      func ExecCmdDir(dir, cmdName string, args ...string) (string, string, error) {
          bufOut, bufErr, err := ExecCmdDirBytes(dir, cmdName, args...)
          return string(bufOut), string(bufErr), err
      }
      // ExecCmd executes system command
      // and return stdout, stderr in string type, along with possible error.
      func ExecCmd(cmdName string, args ...string) (string, string, error) {
          return ExecCmdDir("", cmdName, args...)
      }
    ```
  
  - 结构附带的方法应置于结构定义之后，按照所对应操作的字段顺序摆放方法：
  
    ```go
      type Webhook struct { ... }
      func (w *Webhook) GetEvent() { ... }
      func (w *Webhook) SaveEvent() error { ... }
      func (w *Webhook) HasPushEvent() bool { ... }
    ```
  
  - 如果一个结构拥有对应操作函数，大体上按照 `CRUD` 的顺序放置结构定义之后：
  
    ```
      func CreateWebhook(w *Webhook) error { ... }  func GetWebhookById(hookId int64) (*Webhook, error) { ... }  func UpdateWebhook(w *Webhook) error { ... }  func DeleteWebhook(hookId int64) error { ... }
    ```
  
  - 如果一个结构拥有以 `Has`、`Is`、`Can` 或 `Allow` 开头的函数或方法，则应将它们至于所有其它函数及方法之前；这些函数或方法以 `Has`、`Is`、`Can`、`Allow` 的顺序排序。
  
  - 变量的定义要放置在相关函数之前：
  
    ```
      var CmdDump = cli.Command{      Name:  "dump",      ...      Action: runDump,      Flags:  []cli.Flag{},  }  func runDump(*cli.Context) { ...
    ```
  
  - 在初始化结构时，尽可能使用一一对应方式：
  
    ```go
      	AddHookTask(&HookTask{      Type:        HTT_WEBHOOK,      Url:         w.Url,      Payload:     p,      ContentType: w.ContentType,      IsSsl:       w.IsSsl,  })
    ```

## 7. 测试用例

- 单元测试都必须使用 [GoConvey](http://goconvey.co/) 编写，且辅助包覆盖率必须在 80% 以上。

### 7.1 使用示例

- 为辅助包书写使用示例的时，文件名均命名为 `example_test.go`。
- 测试用例的函数名称必须以 `Test_` 开头，例如：`Test_Logger`。
- 如果为方法书写测试用例，则需要以 `Text_<Struct>_<Method>` 的形式命名，例如：`Test_Macaron_Run`。

