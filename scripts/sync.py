"""
每天定时更新博客内容
1.进入项目根目录: D:/program_about/hugo/hugo-blog
2. 将D:/nextclou/Public/下的文件同步到 ./content/posts/下
3. 执行./push.bat 或 git add . && git commit -m "update" && git push

同步时的更改:
1. 图片路径更正
2. 添加文章head


"""

import os
import shutil

import yaml
import datetime

from config import get_setting


def load_yaml():
    """
    加载yaml文件
    """
    # 当前文件所在目录
    yaml_path = os.path.dirname(os.path.abspath(__file__))
    # yaml文件路径
    yaml_path = os.path.join(yaml_path, "head.yaml")

    with open(yaml_path, "r", encoding="utf-8") as f:
        head = yaml.load(f, Loader=yaml.FullLoader)
        # print(head)
        return head


head = load_yaml()
# print(head)

root_path = get_setting().root_path

dst_path = root_path + "/content/posts/"

src_path = get_setting().blog_path


def create_img_index(root, name):
    """
    name = A.md
    在root下生成'A'文件夹
    将A.md移动到A文件夹下，并重命名为index.md

    如果 存在 root + '/img' 的文件夹
    将 root + '/img' 复制到 root + '/A/img' 下
    """
    # 生成文件夹
    dir_name = name.split(".")[0]
    # print(root, name, dir_name)
    os.mkdir(os.path.join(root, dir_name))
    # 移动文件
    shutil.move(os.path.join(root, name), os.path.join(root, dir_name, "index.md"))
    # 处理img
    if os.path.exists(os.path.join(root, "img")):
        shutil.copytree(os.path.join(root, "img"), os.path.join(root, dir_name, "img"))


class Article:
    head: str
    content: str

    path = ""

    def _get_title(self):
        """
        使用第一个#后的内容作为title, 并删除这一行
        """
        content = self.content
        title = ""
        for line in content.split("\n"):
            if line.startswith("#"):
                title = line.split("#")[1]
                # 删除content中的这一行
                content = content.replace(line, "", 1)
                break
        if title == "":
            title = self.path.split("/")[-1].split(".")[0]
        self.content = content.strip()
        return title.strip()

    def _get_tags(self):
        """
        使用上一层文件夹的名称作为tags
        """
        tag = self.path.split("/")[-2]
        return [tag.strip()]

    def _get_categories(self):
        """
        使用dst_path下的第一个文件夹作为categories
        """
        path = self.path
        categories = ""
        index = path.find(dst_path)
        if index != -1:
            path = path[index + len(dst_path) :]
            categories = path.split("/")[0]
        return [categories.strip()]

    def get_description(self):
        """
        使用TL;DR:后的内容作为description
        """
        content = self.content
        description = ""
        for line in content.split("\n"):
            if line.startswith("TL;DR:"):
                description = line.split("TL;DR:")[1]
                break
        return description.strip()

    def __init__(self, root, name):
        self.path = os.path.join(root, name)
        # 'D:/program_about/hugo/hugo-blog/content/posts/.\\c++\\.\\modern c++.md'
        # 整理路径
        self.path = os.path.abspath(self.path).replace("\\", "/")

        self.load_content()
        self.load_head()

    def load_content(self):
        content = ""
        with open(self.path, "r", encoding="utf-8") as f:
            content = f.read()
        self.content = content

    def load_head(self):
        self.head = head.copy()
        self.head["title"] = self._get_title()
        self.head["tags"] = self._get_tags()
        self.head["categories"] = self._get_categories()
        self.head["description"] = self.get_description()

        # 日期获取文件的创建和修改时间
        # 修改时间
        updateDate = datetime.datetime.fromtimestamp(os.path.getctime(self.path))
        # 创建时间
        createData = datetime.datetime.fromtimestamp(os.path.getmtime(self.path))
        self.head["date"] = createData.strftime("%Y-%m-%d")
        self.head["lastmod"] = updateDate.strftime("%Y-%m-%d")

    def to_md_content(self):
        """
        将head和content合并成md文件
        ---
        head
        ---
        content
        """
        md_content = ""
        md_content += "---\n"
        for key, value in self.head.items():
            md_content += key + ": " + str(value) + "\n"
        md_content += "---\n"
        md_content += self.content
        return md_content


def adjust_md(root, name):
    article = Article(root, name)
    with open(os.path.join(root, name), "w", encoding="utf-8") as f:
        f.write(article.to_md_content())

    create_img_index(root, name)


def adjust(dir):
    print("adjust", dir)
    os.chdir(dir)
    """
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
    """
    for root, dirs, files in os.walk("."):
        root = os.path.join(dir, root)
        for name in files:
            if name == ".md":
                os.remove(os.path.join(root, name))
                continue
            if name.endswith(".md"):
                # 调整md文件的内容和图片引用
                adjust_md(root, name)

        for name in dirs:
            # 递归调用
            adjust(os.path.join(root, name))


def sync():
    print("sync start")
    print("root_path", root_path)
    print("dst_path", dst_path)
    print("src_path", src_path)
    os.chdir(root_path)
    # 当文件已存在时，无法创建该文件。: './content/posts/'

    # 如果文件夹存在，删除
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
    # print(result)
    # return
    # git中也要删除
    os.system("git rm -r ./content/posts/")

    shutil.copytree(src_path, dst_path)

    # 把所有文件夹和文件的名称大写转换为小写
    os.chdir("./content/posts/")
    for root, dirs, files in os.walk("."):
        for name in files:
            new_name = name.lower()
            os.rename(os.path.join(root, name), os.path.join(root, new_name))
        for name in dirs:
            new_name = name.lower()
            os.rename(os.path.join(root, name), os.path.join(root, new_name))
    # 调整文件夹结构
    adjust(dst_path)
    # 上传到git

    os.chdir(root_path)
    os.system("git add ./content/posts/")
    os.system('git commit -m "update"')
    os.system("git push")
    # os.chdir("D:/program_about/hugo/hugo-blog")
    print("sync done")


if __name__ == "__main__":
    sync()
    pass
