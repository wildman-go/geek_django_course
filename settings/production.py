from .base import *

# 首先，将base.py中的所有配置项导入进来
# 然后，在这个文件内覆盖base.py中的部分设置，实现生产环境的配置
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1']

# 如何在启动应用的时候指定使用 开发环境还是生产环境呢？
# python manage.py runserver --settings=settings.local
# python manage.py runserver --settings=settings.production
# python manage.py runserver # 默认采用manage.py中的配置读取配置 文件
