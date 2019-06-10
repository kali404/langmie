from django.conf.urls import url, include
<<<<<<< HEAD
from .views import *
urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^logout/$', LogOut.as_view(), name="logout"),
    url(r'^login/$', LogIn.as_view(), name="login"),
    url(r'^forget/$', ForGet.as_view(), name="forget_pwd"),
    url(r'^reset/$', ResetView.as_view(), name='reset_pwd'),
    # url(r'^/$', ResetView.as_view(), name='modify_pwd'),
    url(r'^image/upload/$', UserInfo.as_view(), name='user_upload'),
    url(r'^users/info/$', UserInfo.as_view(), name='user_info'),
    url(r'^image/$', UploadImageView.as_view(), name='image_upload'),
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),




    # 欺骗性路由
    # url(r'^image$', UploadImageView.as_view(), name='mymessage'),
    # url(r'^image$', UploadImageView.as_view(), name='myfav_teacher'),
    url(r'^image$', UploadImageView.as_view(), name='add_fav'),
    url(r'^image$', UploadImageView.as_view(), name='modify_pwd'),
    # url(r'^image$', UploadImageView.as_view(), name='myfav_course'),
    # url(r'^image$', UploadImageView.as_view(), name='myfav_org'),
=======

urlpatterns = [

>>>>>>> master
]
