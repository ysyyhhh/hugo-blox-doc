import os
import shutil

from config import get_setting

def create_index_blog(root, name):
    '''
    name = A.md
    在root下生成'A'文件夹
    将A.md移动到A文件夹下，并重命名为index.md
  
    如果 存在 root + '/img' 的文件夹
    将 root + '/img' 复制到 root + '/A/img' 下 
    '''
    # 生成文件夹
    dir_name = name.split('.')[0]
    # print(root, name, dir_name)
    os.mkdir(os.path.join(root, dir_name))
    # 移动文件
    shutil.move(os.path.join(root, name), os.path.join(root, dir_name, 'index.md'))
    # 处理img
    if os.path.exists(os.path.join(root, 'img')):
        shutil.copytree(os.path.join(root, 'img'), os.path.join(root, dir_name, 'img'))

from blog import Article

def adjust_blog(dir):
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
                article = Article(root, name)
                with open(os.path.join(root, name), "w", encoding="utf-8") as f:
                    f.write(article.to_md_content())
                create_index_blog(root, name)
      
        for name in dirs:
            # 递归调用
            adjust_blog(os.path.join(root, name))
     
def adjust_docs(dir):
    os.chdir(dir)
    '''
    对于每一个原有的文件夹D
    需要在D下创建一个_index.md文件
    内容为：
    ---
    linkTitle: D
    title: D
    ---

    This section covers D docs.
    
    然后调用blog
    '''
    
    os.chdir(dir)
    for root, dirs, files in os.walk("."):
        root = os.path.join(dir, root)
        for name in dirs:
            # 生成_index.md
            with open(os.path.join(root, name, '_index.md'), 'w', encoding='utf-8') as f:
                f.write('---\n')
                f.write('linkTitle: ' + name + '\n')
                f.write('title: ' + name + '\n')
                f.write('---\n\n')
                f.write('This section covers ' + name + ' docs.\n')
            # 调整文件夹
    
    for root, dirs, files in os.walk("."):
        root = os.path.join(dir, root)
        for name in files:
            if name == '.md':
                os.remove(os.path.join(root, name))
                continue
            # if name.endswith('.md') and name != '_index.md':
            #     create_index_blog(root, name)
        for name in dirs:
            # 递归调用
            adjust_docs(os.path.join(root, name))

def sync():
    
    root_path = get_setting().root_path
    os.chdir(root_path)
    # 当文件已存在时，无法创建该文件。: './content/posts/'
    
    
    # blog文件夹
    root_post_path = root_path + '/content/post/'
    print(root_post_path)
    if os.path.exists(root_post_path):
        shutil.rmtree(root_post_path)
    else:
        print(root_post_path, 'not exists')
    
    # git中也要删除
    os.system('git rm -r ./content/post/')
    
    # docs文件夹
    root_docs_path = root_path + '/content/docs/'
    print(root_docs_path)
    if os.path.exists(root_docs_path):
        shutil.rmtree(root_docs_path)
    else:
        print(root_docs_path, 'not exists')
    # git中也要删除
    os.system('git rm -r ./content/docs/')
    
    # return 
    '''
    先创建content/posts和content/docs 文件夹
    将setting中的属于blog的文件夹复制到content/posts下
    将setting中的属于docs的文件夹复制到content/docs下
    '''
    os.mkdir(root_post_path)
    os.mkdir(root_docs_path)
    
    # 找到属于
    os.chdir(get_setting().public_path)
    
    for root, dirs, files in os.walk("."):
        for name in dirs:
            if name in get_setting().blog_dir:
                blog_path = os.path.join(get_setting().public_path, name)
                shutil.copytree(blog_path, root_post_path + name)
            if name in get_setting().docs_dir:
                docs_path = os.path.join(get_setting().public_path, name)
                shutil.copytree(docs_path, root_docs_path + name)
  
    # 把所有文件夹和文件的名称大写转换为小写
    os.chdir(root_path+'/content/')
    for root, dirs, files in os.walk("."):
        for name in files:
            new_name = name.lower()
            os.rename(os.path.join(root, name), os.path.join(root, new_name))
        for name in dirs:
            new_name = name.lower()
            os.rename(os.path.join(root, name), os.path.join(root, new_name))
    
    # # 调整文件夹结构
    adjust_blog(root_post_path)
    adjust_docs(root_docs_path)
    
    
    with open(os.path.join(root_post_path, '_index.md'), 'w', encoding='utf-8') as f:
        # ---
        # title: Blog
        # view: date-title-summary
        # url: /blog/
        # ---
        f.write('---\n')
        f.write('title: Blog\n')
        f.write('view: date-title-summary\n')
        f.write('url: /blog/\n')
        f.write('---\n')
    
    # 上传到git
  
    # os.chdir('./content/posts/')
    
    os.chdir(root_path)
    os.system('git add ./content/post/')
    os.system('git add ./content/docs/')
    os.system('git commit -m "update"')
    os.system('git push')
    print('sync done')
  
if __name__ == '__main__':
    sync()  
