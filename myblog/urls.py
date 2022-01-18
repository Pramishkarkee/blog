from . import views
from django.urls import path,include
from myblog import views
urlpatterns = [
    path("post",views.post_blog,name="post blog"),
    path("mybloglist",views.mybloglist,name="my-blog-list"),
    path("blogdetail/<bid>",views.blogdetail,name="blog-detail"),
    path("detailblog/<bid>",views.detailblog,name="blog-detail-by-id"),
    path("comment",views.comment,name="comment"),
    path("like",views.like_post,name="like-post")
]