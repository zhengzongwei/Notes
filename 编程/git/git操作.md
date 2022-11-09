# git操作

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

       http://172.16.99.4/openstack/python-eagleclient/merge_requests/66


```

