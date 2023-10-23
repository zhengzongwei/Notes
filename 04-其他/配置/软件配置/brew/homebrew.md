# homebrew 配置

```shell
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.ustc.edu.cn/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.ustc.edu.cn/homebrew-core.git"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles"
export HOMEBREW_API_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles/api/"

/bin/bash -c "$(curl -fsSL https://github.com/Homebrew/install/raw/HEAD/install.sh)"

/bin/bash -c "$(curl -fsSL https://cdn.jsdelivr.net/gh/Homebrew/install@HEAD/install.sh)"
```

## 安装问题
### 发现有提示fatal: not in a git directory Error: Command failed with exit 128: git

```shell
git config --global --add safe.directory path # path 为报错路径
```

```bash
# clean up 
brew untap homebrew/core homebrew/cask
```

## 软件问题

### pyenv

```bash
vim ～/.zshrc
# ======= PYENV START =========
export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
# ======= PYENV END =========
```



### Mariadb

安装mariadb时，发现安装上之后，不能正常在终端使用mysql命令，需要配置环境变量

```bash
# 安装
brew install mariadb

# 查询mariadb 安装路径
brew info mariadb

# 配置环境变量
vim ～/.zshrc

export MYSQL_PATH="/opt/homebrew/opt/mariadb/bin"
export PATH=$MYSQL_PATH:$PATH

source ～/.zshrc
```

