
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from blog_users.forms import CreateAdminUser, CreateWriter
from django.contrib.auth import authenticate
from django.contrib import auth
from myblog.models import Blog

# Create your views here.
User = get_user_model()


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            request.session['id'] = str(user.pk)
            request.session['type'] = user.user_type
            if user.is_staff:
                request.session['name'] = "super user"
            else:
                request.session['name'] = user.first_name
            request.session['super_user'] = user.is_staff
            if request.session['type'] == 'writer':
                return redirect('/')
            elif request.session['type'] == 'admin':
                contex = User.objects.all()
                return redirect('/')
            else:
                if user.is_staff:
                    return redirect('/')
                else:
                    return redirect("/login")
        else:
            return HttpResponse("username and password not match")

    elif request.method == "GET":
        return render(request, 'login.html')


def blog_user(request):
    if len(request.session.keys()) > 0:
        id = request.session['id']
        try:
            user = User.objects.get(id=id)
            if user.user_type == "admin" or user.is_staff:
                contex = User.objects.all()
                return render(request, 'admin/body.html', {'contex': contex})

            elif user.user_type == "writer":
                return redirect("/")

        except User.DoesNotExist:
            return HttpResponse("user not found")

        except Exception as e:
            return HttpResponse("user not found")

    else:
        return HttpResponse("Bad Request")


def admin_create_user(request):
    if request.method == 'POST':
        form = CreateAdminUser(request.POST)
        if form.is_valid():
            username = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            user_type = request.POST.get('user_type')

            u = User.objects.create_user(
                username=username,
                email=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type
            )
            u.save()
            return redirect('/user')
        else:
            return HttpResponse(form.errors)
    elif request.method == 'GET':
        return render(request, 'admin/createuser.html')
    return render(request, 'admin/createuser.html')


def createuser(request):
    if request.method == 'POST':
        form = CreateWriter(request.POST)
        if form.is_valid():
            username = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            password1 = request.POST.get('password1')
            if password == password1:

                u = User.objects.create_user(
                    username=username, email=username, password=password, first_name=first_name, last_name=last_name)
                u.save()
            else:
                return render(request, 'createuser.html', {'error': True, 'message': 'password not match'})
            return redirect('/login')
        else:
            return HttpResponse(form.errors)
    elif request.method == 'GET':
        return render(request, 'createuser.html')


def profile(request):
    if request.session['type'] == 'writer':
        contex = User.objects.get(pk=request.session['id'])
        name = request.session['name']
        return render(request, 'admin/profile.html', {'contex': contex, 'user': 'writer', 'name': name})


def blog(request):
    contex = Blog.objects.filter(approve=True)
    if len(request.session.keys()) > 0:
        if request.session['type'] == 'writer':
            id = request.session['id']
            name = request.session['name']
            return render(request, 'body.html', {'user': 'writer', 'id': id, 'name': name, 'contex': contex})

        elif request.session['type'] == 'admin' or request.session['super_user']:
            id = request.session['id']
            name = request.session['name']
            if name == "":
                name = "user"
            return render(request, 'body.html', {'user': 'admin', 'id': id, 'name': name, 'contex': contex})

    return render(request, 'body.html', {'contex': contex})


def newblog(request):
    if request.session['type'] == 'admin' or request.session['super_user']:
        bloglist = Blog.objects.filter(approve=False)
        return render(request, 'admin/bloglist.html', {'contex': bloglist})
    else:
        return redirect("/")


def update_status(request):
    if request.session['type'] == 'admin' or request.session['super_user']:
        id = request.GET.get('id')
        try:
            blog = Blog.objects.get(id=id)
            blog.approve = True
            blog.save()
            bloglist = Blog.objects.filter(approve=False)
            return render(request, 'admin/bloglist.html', {'contex': bloglist})
        except Exception as e:
            return HttpResponse("Bad Request")
    else:
        return redirect("/")


def oldblog(request):
    if request.session['type'] == 'admin' or request.session['super_user']:
        bloglist = Blog.objects.filter(approve=True)
        return render(request, 'admin/approvedblog.html', {'contex': bloglist})
    else:
        return redirect("/")


def blog_detail_admin(request):
    if request.session['type'] == 'admin' or request.session['super_user']:
        return redirect('/blogs/')


def logout(request):
    auth.logout(request)
    return redirect('/')
