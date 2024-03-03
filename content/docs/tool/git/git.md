# git

## git 常用命令

### git 基本配置

```bash
git config --global user.name "your name"
git config --global user.email "your email"
```

### git 基本操作

```bash
git init # 初始化仓库
git add . # 添加所有文件到暂存区
git commit -m "commit message" # 提交到本地仓库
git remote add origin
git push -u origin master # 推送到远程仓库
git pull origin master # 拉取远程仓库
git clone # 克隆远程仓库
git status # 查看当前状态
git log # 查看提交日志
git diff # 查看修改内容
git branch # 查看分支
git checkout -b branch_name # 创建并切换到新分支
git checkout branch_name # 切换分支
git merge branch_name # 合并分支
git branch -d branch_name # 删除分支
git reset --hard HEAD^ # 回退到上一个版本
git reset --hard commit_id # 回退到指定版本
git reflog # 查看命令历史
git rm file_name # 删除文件
git stash # 暂存当前修改
git stash list # 查看暂存列表
git stash apply # 恢复暂存
git stash drop # 删除暂存
git stash pop # 恢复并删除暂存
git remote -v # 查看远程仓库地址
git remote set-url origin new_url # 修改远程仓库地址
git push origin --delete branch_name # 删除远程分支
git push origin :branch_name # 删除远程分支
git tag # 查看标签
git tag tag_name # 创建标签
git tag tag_name commit_id # 指定提交创建标签
git tag -a tag_name -m "tag message" # 创建带有说明的标签
git tag -d tag_name # 删除标签
git push origin tag_name # 推送标签到远程
git push origin --tags # 推送所有标签到远程
git push origin :refs/tags/tag_name # 删除远程标签
git push origin --delete tag tag_name # 删除远程标签
git checkout -- file_name # 撤销工作区修改
git reset HEAD file_name # 撤销暂存区修改
git reset --hard HEAD^ # 撤销本地提交
git reset --hard commit_id # 撤销本地提交
git config --global alias.st status # 设置别名
git config --global alias.co checkout # 设置别名
git config --global alias.ci commit # 设置别名
git config --global alias.br branch # 设置别名
git config --global alias.unstage 'reset HEAD' # 设置别名
git config --global alias.last 'log -1' # 设置别名
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit" # 设置别名
```

### git 子模块

```bash

# 查看子模块
git submodule

git submodule add # 添加子模块

# 添加子模块并自定义子模块目录名称和分支
git submodule add <repository> [<path>]

git submodule init # 初始化子模块
git submodule update # 更新子模块

git submodule foreach git pull # 更新所有子模块

# 删除子模块
# 1. 删除.gitmodules中对应子模块的条目
# 2. 删除.git/config中对应子模块的条目
# 3. 执行git rm --cached path/to/submodule
# 4. 执行rm -rf .git/modules/path/to/submodule
# 5. 执行rm -rf path/to/submodule
```

