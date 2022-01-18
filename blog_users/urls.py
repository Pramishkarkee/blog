from . import views
from django.urls import path,include

urlpatterns = [
    path('login', views.login ,name = "login"),
    path('user',views.blog_user, name="admin-user"),
    path('createuser',views.createuser, name="createuser"),
    path('admin_createuser',views.admin_create_user, name="admin-create-user"),
    path('newblog',views.newblog,name="new-blog"),
    path('',views.blog,name="blog"),
    path('logout',views.logout,name="logout"),
    path('oldblog',views.oldblog,name="old-blog"),
    path('update_status',views.update_status,name="update-status"),
    path('profile',views.profile,name="profile")

]