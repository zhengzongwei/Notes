# git操作

## 分支

## 工作暂存

```shell
# 暂存
git stash
git stash save "注释"

# 查看暂存记录列表
git stash list

# 应用某个存储
git stash apple stash@{0}

# 应用并删除某个存储
git stash pop

# 删除某个存储
git stash drop

# 晴空所有暂存的stash
git stash clear

```

## 解决冲突

```shell
git rebase master

# 查看冲突文件

# 修改冲突

git add .


git rebase --continue

git push -f

```

## 同步现有仓库到远程仓库

### 方法一

添加第一个仓库

git remote add origin <https://gitee.com/fsoooo/test.git>

再添加第二个仓库

git remote set-url --add origin <https://github.com/fsooo/test.git>

如果还有其他，则可以像添加第二个一样继续添加其他仓库。

然后使用下面命令提交：`git push origin --all`

### 方法二

#### 添加配置模块

打开 .git/config 找到 [remote]，添加对应的 模块 即可，效果如下：

```shell
[core]
    repositoryformatversion = 0
    filemode = false
    bare = false
    logallrefupdates = true
    symlinks = false
    ignorecase = true
[remote "origin"]
    url = https://gitee.com/wangslei/test.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[remote "github"]
    url = https://github.com/fsoooo/test.git
    fetch = +refs/heads/*:refs/remotes/github/*
[branch "master"]
    remote = origin
    merge = refs/heads/master

```

#### 查看远程情况

```shell
git remote
origin
github

git remote
github  https://github.com/fsoooo/test.git (fetch)
github  https://github.com/fsoooo/test.git (push)

```

#### 推送远程分支

```shell
git push origin master
git push github master

```

### 关于 git pull

方法一在 push 的时候比较方便。但是在 pull 的时候只能从方法一中的第一个 url 地址拉取代码。而方法二则不存在这种问题（可能要解决冲突）。
所以，如果只进行 push 操作，推荐方法一，如果也要进行 pull 操作，推荐方法二。

### git 配置

``` shell
 git config #查看本机是否配置了个人信息
 git config --global user.name "……" #定义全局的用户名
 git config --global user.email "……" #定义全局的邮件地址
 git config --list #查看配置信息
```

### 修改已提交用户的账户名

``` bash
git commit --amend --reset-author
```



```bash
name: Release on Tag

on:
  push:
    tags:
      - '*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Go
        uses: actions/setup-go@v2
        with:
          go-version: 1.21

      - name: Build binaries
        run: make

      - name: List repository contents
        run: ls -R

      - name: Create Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: Release notes for ${{ github.ref }}
          draft: false
          prerelease: false
          commitish: ${{ github.sha }}
          owner: ${{ github.repository_owner }}
          repo: ${{ github.event.repository.name }}

      - name: Upload Release Asset (Mac amd64)
        id: upload-release-app-darwin-amd64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_darwin_amd64
          asset_name: app_darwin_amd64_v${{ github.ref#refs/tags/ }}
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Mac arm64)
        id: upload-release-app-darwin-arm64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_darwin_arm64
          asset_name: app_darwin_arm64_v${{ github.ref#refs/tags/ }}
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Linux amd64)
        id: upload-release-app-darwin-arm64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_linux_amd64
          asset_name: app_linux_amd64_v${{ github.ref#refs/tags/ }}
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Linux arm64)
        id: upload-release-app-darwin-arm64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_linux_arm64
          asset_name: app_linux_arm64_v${{ github.ref#refs/tags/ }}
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Windows amd64)
        id: upload-release-app-windows-arm64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_windows_amd64.exe
          asset_name: app_windows_amd64_v${{ github.ref#refs/tags/ }}.exe
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Windows arm64)
        id: upload-release-app-windows-arm64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_windows_arm64.exe
          asset_name: app_windows_arm64_v${{ github.ref#refs/tags/ }}.exe
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Windows 386)
        id: upload-release-app-windows-386
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_windows_386.exe
          asset_name: app_windows_386_v${{ github.ref#refs/tags/ }}.exe
          asset_content_type: application/octet-stream

```



```bash
name: Release on Tag

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Go
        uses: actions/setup-go@v2
        with:
          go-version: 1.21

      - name: Build binaries
        run: make

      - name: List repository contents
        run: ls -R

      - name: Create Release
        id: create_release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: Release notes for ${{ github.ref }}
          draft: false
          prerelease: false
          commitish: ${{ github.sha }}
          owner: ${{ github.repository_owner }}
          repo: ${{ github.event.repository.name }}

      - name: Upload Release Asset (Mac amd64)
        id: upload-release-app-darwin-amd64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_darwin_amd64
          asset_name: app_darwin_amd64_v${{ github.ref }}
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Mac arm64)
        id: upload-release-app-darwin-arm64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_darwin_arm64
          asset_name: app_darwin_arm64_v${{ github.ref }}
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Linux amd64)
        id: upload-release-app-darwin-arm64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_linux_amd64
          asset_name: app_linux_amd64_v${{ github.ref }}
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Linux arm64)
        id: upload-release-app-darwin-arm64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_linux_arm64
          asset_name: app_linux_arm64_v${{ github.ref }}
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Windows amd64)
        id: upload-release-app-windows-arm64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_windows_amd64.exe
          asset_name: app_windows_amd64_v${{ github.ref }}.exe
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Windows arm64)
        id: upload-release-app-windows-arm64
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_windows_arm64.exe
          asset_name: app_windows_arm64_v${{ github.ref }}.exe
          asset_content_type: application/octet-stream

      - name: Upload Release Asset (Windows 386)
        id: upload-release-app-windows-386
        uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ steps.create_release.outputs.upload_url }}
          asset_path: ./build/darwin/app_windows_386.exe
          asset_name: app_windows_386_v${{ github.ref }}.exe
          asset_content_type: application/octet-stream

```

