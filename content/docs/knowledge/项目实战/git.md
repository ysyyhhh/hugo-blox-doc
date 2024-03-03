软件配置管理



21.做代码管理用什么东西

Git 代码仓库



22.git rebase和git merge的区别

Merge会自动根据两个分支的共同祖先和两个分支的最新提交 进行一个三方合并，然后将合并中修改的内容生成一个新的 commit，即merge合并两个分支并生成一个新的提交,并且仍然后保存原来分支的commit记录



Rebase会从两个分支的共同祖先开始提取当前分支上的修改，然后将当前分支上的所有修改合并到目标分支的最新提交后面，如果提取的修改有多个，那git将依次应用到最新的提交后面。Rebase后只剩下一个分支的commit记录

rebase会打乱时间线，但是更加整洁，merge保留了时间线信息



### 23.git提交流程

https://blog.csdn.net/weixin_44256848/article/details/123812716

git pull 同步远程代码

修改代码

git status 显示被修改的文件

git diff 文件名 显示文件具体变更

git add 文件名 提交文件到本地缓存区

git commit 提交到本地仓库

git push 提交本地代码到远程仓库

https://blog.csdn.net/weixin_44256848/article/details/123812716

生产分支（master）‌

- Master分支是仓库的主分支，也有人叫Production分支，这个分支包含最近发布到生产环境的代码，最近发布的Release， 这个分支只能从其他分支合并，不能在这个分支直接修改‌

补丁分支（hotfix）‌

- 当我们在生产环境发现新的Bug时候，我们需要基于master分支创建一个Hotfix分支，然后在Hotfix分支上修复bug，完成Hotfix后，我们要把hotfix分支合并回Master和Develop分支‌，所以Hotfix的改动会进入下一个Release

发布分支（release)‌

- 当你需要发布一个新功能的时候，要基于Develop分支创建一个Release分支，在Release分支测试并修复bug，完成release后，把release合并到master和develop分支‌

开发分支（develop）‌

- 这个分支是我们的主开发分支，包含所有要发布到下一个Release的代码，这个主要合并与其他分支，比如Feature分支‌

功能分支（feature）‌

- feature分支主要是用来开发一个新的功能，一旦开发完成，我们合并回Develop分支进入下一个Release‌



