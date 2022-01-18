
from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import auth
# User = get_user_model()
from myblog.forms import CommentForm, CreateWriter, LikeForm
from myblog.models import Blog, Like, Comment
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your views here.


def post_blog(request):
    if request.method == 'POST':
        if len(request.session.keys()) > 0:
            if request.session['type'] == 'writer' or request.session['type'] == 'admin' or request.session['super_user']:
                id = request.session['id']
                data = request.POST.copy()
                data['user'] = id
                form = CreateWriter(data)
                if form.is_valid():
                    form.save()
                    return redirect("/blogs/mybloglist")
                else:
                    print(form.errors)
                    return HttpResponse("error")
            else:
                return HttpResponse("access denied")
    else:
        if len(request.session.keys()) > 0:
            id = request.session['id']
            name = request.session['name']
            if request.session['type'] == 'writer':
                return render(
                    request,
                    'create_blogs.html',
                    {
                        'user': 'writer',
                        'id': id,
                        'name': name
                    })
            elif request.session['type'] == 'admin' or request.session['super_user']:
                return render(
                    request,
                    'create_blogs.html',
                    {
                        'user': 'admin',
                        'id': id,
                        'name': name
                    })
            else:
                return HttpResponse("access denied")


def mybloglist(request):
    if len(request.session.keys()) > 0:
        id = request.session['id']
        name = request.session['name']
        if request.session['type'] == 'writer':
            
            contex = Blog.objects.filter(user=id)
            return render(
                request,
                'myblogs.html',
                {
                    'user': 'writer',
                    'id': id,
                    'name': name,
                    "contex": contex
                })
        elif request.session['type'] == 'admin' or request.session['super_user']:
            contex = Blog.objects.filter(user=id)
            if name==None:
                name="user"
            return render(
                request,
                'myblogs.html',
                {
                    'user': 'admin',
                    'id': id,
                    'name': name,
                    "contex": contex
                })

        else:
            return HttpResponse("access denied")


def blogdetail(request, bid=None):
    if bid is not None:
        if len(request.session.keys()) > 0:
            id = request.session['id']
            name = request.session['name']
            if request.session['type'] == 'writer':
                contex = Blog.objects.get(pk=bid, user=id)
                name = contex.user.first_name + " " + contex.user.last_name
                like = Like.objects.filter(blog=bid).count()
                comment = Comment.objects.filter(blog=bid)
                return render(request, 'blog_detail.html', {'user': 'writer', 'id': id, 'name': name, 'contex': contex, 'name': name, "comment": comment, "like": like})
            elif request.session['type'] == 'admin' or request.session['super_user']:
                contex = Blog.objects.get(pk=bid, user=id)
                name = contex.user.first_name + " " + contex.user.last_name
                like = Like.objects.filter(blog=bid).count()
                comment = Comment.objects.filter(blog=bid)
                return render(request, 'blog_detail.html', {'user': 'admin', 'id': id, 'name': name, 'contex': contex, 'name': name, "comment": comment, "like": like})

    return HttpResponse("not found")


def detailblog(request, bid=None):
    if bid is not None:
        contex = Blog.objects.get(pk=bid)
        name = contex.user.first_name + " " + contex.user.last_name
        like = Like.objects.filter(blog=bid).count()
        comment = Comment.objects.filter(blog=bid)
        if len(request.session.keys()) > 0:
            id = request.session['id']
            name = request.session['name']
            if request.session['type'] == 'writer':
                return render(
                    request,
                    'blog_detail.html',
                    {
                        'user': 'writer',
                        'id': id, 'name': name,
                        'contex': contex,
                        'name': name,
                        "comment": comment,
                        "like": like
                    }
                )

            elif request.session['type'] == 'admin' or request.session['super_user']:

                return render(
                    request,
                    'blog_detail.html',
                    {
                        'user': 'admin',
                        'id': id,
                        'name': name,
                        'contex': contex,
                        'name': name,
                        "comment": comment,
                        "like": like
                    }
                )

            else:
                return HttpResponse("user not found")
        else:
            return render(
                request,
                'blog_detail.html',
                {
                    'contex': contex,
                    'name': name,
                    "comment": comment,
                    "like": like
                }
            )


def comment(request):
    if request.method == "POST":
        if len(request.session.keys()) > 0:
            bid = request.POST.get('blog')
            form = CommentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/blogs/detailblog/'+bid)

        return HttpResponse("somethings wrong")
    else:
        return HttpResponse("get method")


def like_post(request):
    if request.method == 'POST':
        user = request.POST.get("user")
        blog = request.POST.get("blog")
        try:
            like = Like.objects.get(user=user, blog=blog)
            return redirect('/blogs/detailblog/'+blog)
        except Like.DoesNotExist:
            form = LikeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/blogs/detailblog/'+blog)
            else:
                return HttpResponse("error")
    else:
        return HttpResponse("not exist")
