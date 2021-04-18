from .base import *

# 首先，将base.py中的所有配置项导入进来
# 然后，在这个文件内覆盖base.py中的部分设置，实现开发环境的配置
DEBUG = True

INSTALLED_APPS += [
    # 'debug_toolbar',  # and other apps for local development
]
