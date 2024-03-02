import os
import shutil

from config import get_setting

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
    # root_path = 'D:/program_about/hugo/hugo-blog'
    root_path = get_setting().root_path
    os.chdir(root_path)
    # 当文件已存在时，无法创建该文件。: './content/posts/'
    
    posts_path = root_path + '/content/posts/'
    if os.path.exists(posts_path):
        shutil.rmtree(posts_path)
    
    # git中也要删除
    os.system('git rm -r ./content/posts/')
    
    blog_path = get_setting().blog_path
    shutil.copytree(blog_path, posts_path)
  
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
    adjust(posts_path)
    # 上传到git
  
    # os.chdir('./content/posts/')
    
    os.chdir(root_path)
    os.system('git add ./content/posts/')
    os.system('git commit -m "update"')
    os.system('git push')
    print('sync done')
  
if __name__ == '__main__':
    sync()  