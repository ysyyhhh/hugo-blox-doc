import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # root_path 默认为当前目录的上一级
    root_path: str = os.path.abspath(os.getcwd())
    blog_path: str = "E:\\nextcloud\\Public"


def get_setting():
    return Settings()
