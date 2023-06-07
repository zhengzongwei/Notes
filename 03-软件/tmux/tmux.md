# tmux 快捷键指北

|        功能        |               命令                |                             说明                             |
| :----------------: | :-------------------------------: | :----------------------------------------------------------: |
|   进入 tmux 空间   |            输入`tmux`             |                    默认有1个窗口，1个格子                    |
|     prefix key     |             `Ctrl-b`              | tmux命令一般由`prefix key`+`command key`触发，`prefix key`默认是`Ctrl-b` |
|      新建窗口      |           `prefix`+`c`            |               左下角可以看到窗口序号和当前程序               |
|      跳转窗口      |          `prefix`+`num`           |                      `prefix`+窗口序号                       |
|      切换窗口      |     `prefix`+`p` `prefix`+`n`     |   `prefix`+`p`切换到左窗口 <br />`prefix`+`n`切换到右窗口    |
|      切换窗口      |     `prefix`+`p` `prefix`+`n`     |      `prefix`+`p`切换到左窗口 `prefix`+`n`切换到右窗口       |
|      创建格子      |     `prefix`+`%` `prefix`+`"`     |                   `%`左右分割 `"`上下分割                    |
|      切换格子      |         `prefix`+`方向键`         |                                                              |
|      选择格子      |        `prefix`+`q`+`num`         |      按下`prefix`+`q`显示格子序号，按下对应数字跳转格子      |
|      全屏格子      |           `prefix`+`z`            |                     切换当前格子全屏状态                     |
|      关闭格子      |     `prefix`+`x` 或输入`exit`     | 左下角提示是否关闭，键入`y`确认关闭。`exit`直接退出格子。当最后一个大格子都被关闭时，关闭窗口。 |
|    调整格子大小    |          `prefix-方向键`          |                         调整格子大小                         |
|    查看所有窗口    |           `prefix`+`w`            |        上下键查看每个窗口的结构预览，`Enter`进入窗口         |
|   离开 tmux 空间   |           `prefix`+`d`            |             离开空间后，空间被缓冲，没有被结束。             |
|   回到 tmux 空间   | 输入 `tmux attach` **或`tmux a`** |                       重新连回工作空间                       |
| 查看所有 tmux 空间 |           输入`tmux ls`           |                      查看 tmux 空间编号                      |
|   选择 tmux 空间   |    输入`tmux attach -t <num>`     |                       `<num>`空间编号                        |
|                    |                                   |                                                              |

## 复制粘贴

`prefix`+`[` 进入文本复制模式

`prefix`+`空格` 开始复制的起始位置

上下左右选择要复制的文本

`ALT + w `将文本保存到tmux的buffer中

`prefix`+`]`粘贴



## 配置



```shell
路径：
~/.tmux.conf

# 添加鼠标操作
set -g mouse on
set -g mouse-resize-pane on
set -g mouse-select-pane on
set -g mouse-select-window on

# 在当前目录下打开新的终端
# bind c new-window -c "#{pane_current_path}"
bind '"' split-window -c "#{pane_current_path}"
bind % split-window -h -c "#{pane_current_path}"

```

