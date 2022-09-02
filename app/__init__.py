import os
from app.BaseServer import BaseServer

def create_app():
    config = {
        "NEXTCLOUD_URL": "", # nextcloud地址
        "NEXTCLOUD_USER": "", # 上传文件用户
        "NEXTCLOUD_PWD": "", # 上传文件用户密码
        "BLOG_IMAGES": os.path.join("blog", "images") # 文件默认上传位置
    }
    app = BaseServer(config)
    return app

