from django.conf.urls import url
from .views import joblist

urlpatterns = [
    # 职位列表
    url(r"^joblist/", joblist, name='joblist')
]
