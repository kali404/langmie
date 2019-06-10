from django.conf.urls import url

from .views import *
urlpatterns = [









    # 欺骗性路由
    url(r'^org$',Gut.as_view(),name='org_list'),
    url(r'^teacher_list$', Gut.as_view(), name="teacher_list"),
    url(r'^org_home$', Gut.as_view(), name="org_home"),
    url(r'^org_home$', Gut.as_view(), name="add_fav"),




]
