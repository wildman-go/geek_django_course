from django.conf.urls import url
from .views import joblist, detail

urlpatterns = [
    # 职位列表
    url(r"^joblist/", joblist, name='joblist'),
    # 职位详情
    url(r"^job/(?P<job_id>\d+)/$", detail, name='detail'),
]
