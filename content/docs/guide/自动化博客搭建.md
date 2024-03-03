# 用Hugo + Github Pages/Action + py + 任务计划程序 搭建 全自动化markdown笔记转博客

#### TL;DR

> 1. 背景: 已使用nextcloud和typora写笔记
> 2. 需求: 将笔记转换为博客.(且因为本人太懒,😂 所以需要全自动化)
>    1. 在nextcloud中, 专门设置一个文件夹"笔记" 转换为博客文件夹
>    2. 不能改变原来记笔记的方式
>    3. 不能有任何新增的操作
> 3. 方案:
>    1. 使用hugo搭建博客
>    2. 使用Github pages部署博客
>    3. 使用Github Actions自动化部署
>    4. 使用py脚本将笔记转换为博客
>    5. 使用任务计划程序定时执行py脚本

## 使用hugo搭建博客

参考:
[hugo官网](https://gohugo.io/getting-started/quick-start/)
[Hugo+Github Pages+Github Action博客方案之二](https://zhuanlan.zhihu.com/p/568470172)
[Hugo+Github Pages+Github Action博客方案之三](https://zhuanlan.zhihu.com/p/568764664)
[PaperMod主题](https://github.com/adityatelange/hugo-PaperMod/wiki/Installation)

#### 创建github仓库

要创建两个仓库

1. 一个仓库用于存放博客源码
2. 一个仓库用于存放博客静态文件

###### 创建博客静态文件仓库

设置仓库名为: `用户名.github.io`
[我的博客仓库](https://github.com/ysyyhhh/ysyyhhh.github.io)

###### 创建博客源码仓库

设置仓库名为: `hugo-blog`  // 仓库名可以自定义
[我的博客源码仓库](https://github.com/ysyyhhh/hugo-blog)

#### 安装hugo

```bash
scoop install hugo
```

#### 创建hugo博客

```bash
hugo new site hugo-blog
```

#### 安装主题

```bash
cd hugo-blog ## 进入博客目录, 这个是博客源码仓库
git init
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
git submodule update --init --recursive ## needed when you reclone your repo (submodules may not get cloned automatically)
```

#### 配置主题

这里使用yaml格式的配置文件, 也可以使用toml格式的配置文件
所以需要删除config.toml文件, 并创建config.yaml文件

config.yaml:

```yaml
baseURL: /
title: ysyy's blog
theme: PaperMod
languageCode: zh-cn
```

[剩余配置参考](https://github.com/adityatelange/hugo-PaperMod/wiki/Installation#sample-configyml)

#### 创建文章

```bash
hugo new posts/first/hello-world.md
```

#### 本地预览

```bash
hugo server -D
```

#### 生成静态文件

生成静态文件, 生成的静态文件在 `public`文件夹中。
之后我们将这个文件夹中复制到博客静态文件仓库中

```bash
hugo 
```

#### 部署到github pages

创建静态文件夹

```bash
git clone git@用户名.github.io.git

cd 用户名.github.io

cp -r hugo-blog/public/* ./
```

提交到github

```bash
git add .
git commit -m "first commit"
git push origin main
```

#### 配置github pages

在github中的 `用户名.github.io`仓库中,
点击 `Settings`选项卡, 找到 `GitHub Pages`选项,
将 `Source`选项设置为 `main`分支, 点击 `Save`按钮,
这样就可以通过 `https://用户名.github.io`访问博客了

## 使用Github Actions自动化部署

[参考](https://zhuanlan.zhihu.com/p/568764664)

如果每一次更新/发布新博客都需要手动执行上面的步骤, 那么就太麻烦了, 所以我们需要自动化部署

在博客源码仓库的根目录下创建
`.github/workflows/deploy.yml`文件

```yaml
name: ysyyblog
on:
  push:
    branches:
      - main
jobs:
  build-deploy:
    runs-on: ubuntu-20.04
#    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true  # Fetch Hugo themes (true OR recursive)
          fetch-depth: 0    # Fetch all history for .GitInfo and .Lastmod

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
          # extended: true

      - name: Build
        run: hugo --minify

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          personal_token: ${{ secrets.PERSONAL_TOKEN }} # 另外还支持 deploy_token 和 github_token
          external_repository: ysyyhhh/ysyyhhh.github.io # 修改为你的 静态文件GitHub Pages 仓库
          publish_dir: ./public
#          keep_files: false
          publish_branch: main
          # 如果使用自定义域名，还需要添加下面一行配置
          # cname: www
```

### 创建personal_token

在github主页的右上角点击头像, 点击 `Settings`选项卡, 找到 `Developer settings`选项,

找到 `Personal access tokens`选项, 点击 `Generate new token`按钮, 创建一个新的token

### 配置personal_token

在hugo-blog仓库中, 点击 `Settings`选项卡, 找到 `Secrets`选项, 点击 `New repository secret`按钮,

新增一个名为 `PERSONAL_TOKEN`的secret, 值为上面创建的personal_token

### 测试自动化部署

在本地的hugo-blog仓库中, 修改 `content/posts/first/hello-world.md`文件, 然后提交到github

可以在 `Actions`选项卡中查看自动化部署的状态

如果在 `Actions`选项卡中看到了 `build-deploy`任务, 且状态为 `success`, 那么就说明自动化部署成功了

可以在 `用户名.github.io`仓库中查看是否已经更新.

## 使用任务计划程序和py脚本实现全自动化

上面的步骤已经让我们发布笔记的过程变成:

1. 使用hugo new / 直接编辑 content的文件 来创建笔记
2. 提交到hugo-blog仓库

然后hugo-blog仓库就会自动部署到用户名.github.io仓库中

虽然已经只剩两步了,但遵循能自动化就自动化的原则, 我们还是要把这两步也自动化

### 使用py脚本将笔记转换为博客

安装python这些步骤就省去了,这里直接给出py脚本

```python
'''
每天定时更新博客内容
1.进入项目根目录: D:/program_about/hugo/hugo-blog
2. 将D:/nextcloud/笔记/下的文件同步到 ./content/posts/下
3. 执行./push.bat 或 git add . && git commit -m "update" && git push
'''

import os
import shutil

def create_index(root, name):
    '''
    name = A.md
    在root下生成'A'文件夹
    将A.md移动到A文件夹下，并重命名为index.md
  
    如果 存在 root + '/img' 的文件夹
    将 root + '/img' 复制到 root + '/A/img' 下 
    '''
    # 生成文件夹
    dir_name = name.split('.')[0]
    print(root, name, dir_name)
    os.mkdir(os.path.join(root, dir_name))
    # 移动文件
    shutil.move(os.path.join(root, name), os.path.join(root, dir_name, 'index.md'))
    # 处理img
    if os.path.exists(os.path.join(root, 'img')):
        shutil.copytree(os.path.join(root, 'img'), os.path.join(root, dir_name, 'img'))
  
  

def adjust(dir):
    os.chdir(dir)
    '''
    将所有下面的格式
    - A.md
    - img
        - A-1.png
    
    转换成
    - A
        - index.md
        - img
            - A-1.png
  
    如果遇到".md"文件,直接删除
    '''
    for(root, dirs, files) in os.walk("."):
        root = os.path.join(dir, root)
        for name in files:
            if name == '.md':
                os.remove(os.path.join(root, name))
                continue
            if name.endswith('.md'):
                create_index(root, name)
      
        for name in dirs:
            # 递归调用
            adjust(os.path.join(root, name))
      
      
  
def sync():
    root_path = 'D:/program_about/hugo/hugo-blog'
    os.chdir(root_path)
    # 当文件已存在时，无法创建该文件。: './content/posts/'
    shutil.rmtree('./content/posts/')
    # git中也要删除
    os.system('git rm -r ./content/posts/')
  
    shutil.copytree('D:/nextcloud/笔记/', './content/posts/')
  
    # 把所有文件夹和文件的名称大写转换为小写
    os.chdir('./content/posts/')
    for root, dirs, files in os.walk("."):
        for name in files:
            new_name = name.lower()
            os.rename(os.path.join(root, name), os.path.join(root, new_name))
        for name in dirs:
            new_name = name.lower()
            os.rename(os.path.join(root, name), os.path.join(root, new_name))
    # 调整文件夹结构
    adjust(root_path+'./content/posts/')
    # 上传到git
  
    # os.chdir('./content/posts/')
    os.chdir('D:/program_about/hugo/hugo-blog')
    os.system('git add ./content/posts/')
    os.system('git commit -m "update"')
    os.system('git push')
    os.chdir('D:/program_about/hugo/hugo-blog')
    print('sync done')
  
if __name__ == '__main__':
    sync()  
```

将上面的路径修改为自己的路径, 然后保存为 `sync.py`文件
可以执行py脚本,测试一下

#### 关于图片路径问题

[参考方案](https://discourse.gohugo.io/t/image-path-with-relative-urls/21970/3)

因为我平时的图片路径是
  
```markdown
- A.md
- img
    - A-1.png
```

但是hugo会将A.md文件转换为A文件夹, 所以此时是无法访问A-1.png的.

这里是通过改变相对路径关系来解决的, 即代码中的adjust()

当然如果你有图床就不需要这么麻烦了

### 使用任务计划程序定时执行py脚本

参考
这里我使用的是win10自带的任务计划程序, 其他系统的任务计划程序也是类似的

以下步骤由Claude生成

```markdown
下面是如何使用Windows任务计划程序来配置定时每天执行Python脚本的步骤:

打开任务计划程序(Windows + R 输入taskschd.msc回车)

点击"操作"栏中的"创建基本任务"

输入任务名称,选择触发器为每天定时,设置执行时间

在操作栏中,点击“新建”

选择“启动一个程序”

在“程序/脚本”框中输入Python解释器的路径,例如C:\Python37\python.exe

在“添加参数(可选)”中输入python脚本文件的完整路径,例如C:\Users\username\script.py

点击“确定”保存此操作

在下一页中选择用户账号,例如“当前用户”

点击“确定”完成创建任务

根据需要配置触发器记录和其他选项

点击“确定”保存任务

任务将在设定的时间自动执行python脚本文件

每次修改脚本后需要停止原有任务,然后再新建一个相同的任务来加载修改后的脚本代码。

需要注意python interpreter路径和脚本路径的正确性。定时执行格式也需要正确,这样就可以实现Windows系统中的自动定时任务执行Python脚本了。
```
