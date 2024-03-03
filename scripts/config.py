import os
from pydantic import BaseSettings

'''
属于docs
guide
knowledge
language
Tips
tool

属于blog
Paper
public-course
QA
'''

class Settings(BaseSettings):
    # root_path 默认为当前目录的上一级
    root_path: str = os.path.abspath(os.getcwd())
    
    public_path: str = "E:\\nextcloud\\Public"
    # blog_path: str = "E:\\nextcloud\\Public"
    
    docs_dir: set = {"guide", "knowledge", "language", "Tips", "tool"}
    blog_dir: set = {"Paper", "public-course", "QA"}

def get_setting():
    return Settings()
