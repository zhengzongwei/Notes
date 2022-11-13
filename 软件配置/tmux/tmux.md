```
# --------------------------------------------------- Tmux Config -----------------------------------------------------------
#  Filename: ~/.tmux.conf
#   Created: Now
#      Desc:
#    _
#   | |_ _ __ ___  _   ___  __
#   | __| '_ ` _ \| | | \ \/ /
#   | |_| | | | | | |_| |>  <
#    \__|_| |_| |_|\__,_/_/\_\
#
#    Author: LWY, 1091761664@qq.com
#   Company: myself
# --------------------------------------------------- prefix -----------------------------------------------------------
# 设置前缀命令和命令的间隔时间
set -g escape-time 0

# Bigger history
set -g history-limit 65535

# 提示信息的持续时间(ms)
set -g display-time 3000

# 控制台激活后的持续时间(ms)
set -g repeat-time 500

# 修改指令前缀
set-option -g prefix C-a

# C-b 即 Ctrl+b 键，unbind 意味着解除绑定
unbind-key C-b

# 绑定 Ctrl+a 为新的指令前缀
bind-key a send-prefix

# 从tmux v1.6版起，支持设置第二个指令前缀
# set-option -g prefix2 ` # 设置一个不常用的`键作为指令前缀，按键更快些

# 重新加载配置文件指令为： Ctrl+a r
bind r source-file ~/.tmux.conf \; display-message "Config reloaded.."

# --------------------------------------------------- 更改新增面板键 -----------------------------------------------------------
unbind '"'
bind - splitw -v -c '#{pane_current_path}' # 垂直方向新增面板，默认进入当前目录，前缀 + -
unbind %
bind = splitw -h -c '#{pane_current_path}' # 水平方向新增面板，默认进入当前目录，前缀 + =

# --------------------------------------------------- 开启鼠标支持 -----------------------------------------------------------
# v2.1(2015.10.28)之前的版本
# setw -g mode-mouse on # 支持鼠标选取文本等
# setw -g mouse-resize-pane on # 支持鼠标拖动调整面板的大小(通过拖动面板间的分割线)
# setw -g mouse-select-pane on # 支持鼠标选中并切换面板
# setw -g mouse-select-window on # 支持鼠标选中并切换窗口(通过点击状态栏窗口名称)

# v2.1及以上的版本
set-option -g mouse on # 等同于以上4个指令的效果

# --------------------------------------------------- vim 风格 -----------------------------------------------------------
# 绑定hjkl键为面板切换的上下左右键，-r表示可重复按键，大概500ms之内
bind -r k select-pane -U # 绑定k为↑
bind -r j select-pane -D # 绑定j为↓
bind -r h select-pane -L # 绑定h为←
bind -r l select-pane -R # 绑定l为→

# 面板调整大小
# 绑定Ctrl+hjkl键为面板上下左右调整边缘的快捷指令
bind -r ^k resizep -U 5 # 绑定Ctrl+k为往↑调整面板边缘5个单元格
bind -r ^j resizep -D 5 # 绑定Ctrl+j为往↓调整面板边缘5个单元格
bind -r ^h resizep -L 5 # 绑定Ctrl+h为往←调整面板边缘5个单元格
bind -r ^l resizep -R 5 # 绑定Ctrl+l为往→调整面板边缘5个单元格

# 复制模式更改为 vi 风格
# 进入复制模式 快捷键：prefix + [
setw -g mode-keys vi # 开启vi风格后，支持vi的C-d、C-u、hjkl等快捷键

# 多个窗口操作
bind b setw synchronize-panes

# --------------------------------------------------- 复制粘贴 -----------------------------------------------------------

# 复制模式向 vi 靠拢
#旧版本：
#bind -t vi-copy v begin-selection	# 绑定v键为开始选择文本
#bind -t vi-copy y copy-selection 	# 绑定y键为复制选中文本

# 新版本：
bind -T copy-mode-vi v send -X begin-selection	# 开始复制
bind -T copy-mode-vi y send -X copy-selection	# 复制剪切板
bind p pasteb # 绑定p键为粘贴文本（p键默认用于进入上一个窗口，不建议覆盖）

# --------------------------------------------------- 其他 -----------------------------------------------------------

#设置窗口面板起始序号
set -g base-index 1         # 设置窗口的起始下标为1
set -g pane-base-index 1    # 设置面板的起始下标为1
set -s focus-events on
set-window-option -g automatic-rename on
set-window-option -g monitor-activity on

# --------------------------------------------------- 自定义状态栏 -----------------------------------------------------------

set -g default-terminal "screen-256color"
set -g status-interval 30                   # 状态栏刷新时间
set -g status-justify centre                # 状态栏列表左对齐
setw -g monitor-activity on                 # 非当前窗口有内容更新时在状态栏通知

set -g status-bg black                      # 设置状态栏背景黑色
set -g status-fg white                      # 设置状态栏前景黄色
set -g status-style "bg=black, fg=yellow"   # 状态栏前景背景色

set -g status-left "#[fg=green]#h S:#S #[fg=yellow]W:#I #[fg=cyan]P:#P"                                     # 状态栏左侧内容
set -g status-right "#{?pane_synchronized, #[fg=colour196]*SYNC*#[default],} | #[fg=cyan][%W] %a %b %d %R"  # 状态栏右侧内容
set -g status-left-length 40 	                                                                            # 状态栏左边长度40
set -g status-right-length 40 	                                                                            # 状态栏左边长度40

set -wg window-status-format " #I #W "                              # 状态栏窗口名称格式
setw -g window-status-current-format '#[bg=red]#[fg=white]#I:#W#F'  # 状态栏当前窗口名称格式(#I：序号，#w：窗口名称，#F：间隔符)
set -wg window-status-separator ""                                  # 状态栏窗口名称之间的间隔
set -wg window-status-current-style "bg=red"                        # 状态栏当前窗口名称的样式
set -wg window-status-last-style "fg=red"                           # 状态栏最后一个窗口名称的样式
set -g message-style "bg=#202529, fg=#91A8BA"                       # 指定消息通知的前景、后景色
# --------------------------------------------------- End -----------------------------------------------------------
```

- 安装 tmux 3.2

```
yum install -y libevent-devel.x86_64
yum install -y ncurses-devel.x86_64
./configure && make && sudo make install
```