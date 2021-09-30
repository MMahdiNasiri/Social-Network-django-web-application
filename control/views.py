import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.forms import LoginForm
from posts.models import Post, PostComment
from django.core.paginator import Paginator

from profiles.models import Profile


def staff_login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('control-posts')
            else:
                messages.error(request, 'دسترسی شما قطع شده است')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')

    return render(request, 'control/staff-login.html', {'form': form})


@user_passes_test(lambda u: u.is_staff, login_url='staff-login')
def control_posts(request):
    posts = Post.objects.filter(parent=None).order_by("-timestamp")
    posts = [x.serialize() for x in posts]
    paginator = Paginator(posts, 25)
    top_users_sql = User.objects.annotate(
        post_count=Count('posts')).order_by('-post_count')[:10]
    top_users = [[x.username, x.post_count] for x in top_users_sql]
    top_users, count = map(list, zip(*top_users))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'top_users': top_users,
        'count': count,
        'page_obj': page_obj
    }
    return render(request, 'control/post-control.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='staff-login')
def control_comments(request):
    qs = PostComment.objects.all().order_by("-timestamp")
    comments = [x.serialize() for x in qs]
    paginator = Paginator(comments, 25)
    top_users_sql = User.objects.annotate(
        comment_count=Count('comments')).order_by('-comments')[:10]
    top_users = [[x.username, x.comment_count] for x in top_users_sql]
    top_users, count = map(list, zip(*top_users))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'top_users': top_users,
        'count': count,
        'page_obj': page_obj
    }
    return render(request, 'control/comments-control.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='staff-login')
def control_users(request):
    qs = Profile.objects.all().order_by("-timestamp")
    paginator = Paginator(qs, 25)
    top_users_sql = User.objects.annotate(comment_count=Count('comments'),
                                          post_count=Count('posts'),
                                          field_sum=F('post_count') + F('comment_count')
                                          ).order_by('-field_sum')[:10]
    top_users = [[x.username, x.post_count, x.comment_count] for x in top_users_sql]
    top_users, post_count, comment_count = map(list, zip(*top_users))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'top_users': top_users,
        'post_count': post_count,
        'comment_count': comment_count,
        'page_obj': page_obj
    }
    return render(request, 'control/users-control.html', context)


def delete_obj(request):
    object_types = {
        'post': Post,
        'comment': PostComment,
        'user': User
    }
    print('this is in delete obj')
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    obj_type = body['obj_type']
    obj_id = body['obj_id']
    obj = object_types[obj_type].objects.filter(id=obj_id)
    if obj:
        obj = obj.first()
    else:
        return JsonResponse({'status': 404})
    obj.delete()
    return JsonResponse({'result': 202})

