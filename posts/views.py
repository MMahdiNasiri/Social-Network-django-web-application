from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Post, PostComment, Hashtag
from .forms import CreatePost
import json


def last_posts_view(request):
    qs = Post.objects.all().order_by("-timestamp")
    posts = [x.serialize() for x in qs]
    paginator = Paginator(posts, 50)
    top_hashtags = Hashtag.objects.annotate(
        num_posts=Count('post_hashtag')).order_by('-num_posts')[:5]
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'type': 'last_posts',
        'top_hashtags': top_hashtags
    }
    return render(request, 'posts/posts.html', context)


@login_required(login_url='/accounts/login/')
def home(request):
    user = request.user
    qs = user.following.all()
    followed_users = [x.user.id for x in qs]
    followed_users.append(user.id)
    posts = Post.objects.filter(
        user__id__in=followed_users).order_by("-timestamp")[:60]
    posts = [x.serialize() for x in posts]
    context = {
        'posts': posts,
        'type': 'home'
    }
    return render(request, 'posts/posts.html', context)


@login_required(login_url='/accounts/login/')
def like(request):
    user = request.user
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    post_id = body['post_id']
    post = Post.objects.filter(id=post_id).first()
    if post:
        post_likes = post.likes.all()
        if user in post_likes:
            post.likes.remove(user)
        else:
            post.likes.add(user)
    else:
        return HttpResponse(False)
    likes = post.likes.all().count()
    return HttpResponse(likes)


@login_required(login_url='/accounts/login/')
def post_create_view(request, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = user
            post.save()
            tags = [tag.strip("#") for tag in post.content.split() if tag.startswith("#")]
            for tag in tags:
                qr = Hashtag.objects.filter(name=tag)
                if qr.exists():
                    tagobj = qr.first()
                else:
                    tagobj = Hashtag.objects.create(name=tag)
                post.hashtag.add(tagobj)
            data = post.serialize()
            return JsonResponse(data=data)
    return


@login_required(login_url='/accounts/login/')
def republish_view(request):
    action_user = request.user
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    target_id = body['post_id']
    target_post = Post.objects.filter(id=target_id)
    if not target_post.exists():
        return Http404
    target_post = target_post.first()
    if target_post.parent:
        target_post = target_post.parent

    post = Post.objects.create(user=action_user, parent=target_post)
    parent_post = post.parent.serialize()
    data = {
        'id': post.id,
        'username': action_user.username,
        'name': action_user.get_full_name(),
        'profile_img': action_user.profile.profileImage.url,
        'parent': parent_post,
    }
    return JsonResponse(data=data)


def post_detail_view(request, post_id):
    post = Post.objects.filter(id=post_id)
    if not post:
        return Http404
    qs = PostComment.objects.filter(post=post.first()).order_by("-timestamp")
    comments = [x.serialize() for x in qs]
    post = post.first().serialize()

    context = {
        'post': post,
        'comments': comments
    }
    return render(request, 'posts/detail.html', context=context)


@login_required(login_url='/accounts/login/')
def create_comment(request, post_id):
    user = request.user
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    content = body['content']
    post_id = body['post_id']
    if not content or not post_id:
        return JsonResponse(data='', status=404)
    post = Post.objects.filter(id=post_id)
    if not post:
        return JsonResponse(data='', status=404)

    comment = PostComment.objects.create(user=user,
                                         comment=content,
                                         post=post.first())
    comment.save()
    comment = comment.serialize()
    return JsonResponse(data=comment)


@login_required(login_url='/accounts/login/')
def hashtags(request, name):
    tag = Hashtag.objects.filter(name=name)
    top_hashtags = Hashtag.objects.annotate(
        num_posts=Count('post_hashtag')).order_by('-num_posts')[:5]
    posts = []
    if tag.exists():
        tagobj = tag.first()
        posts = Post.objects.filter(hashtag=tagobj).order_by("-timestamp")
        posts = [x.serialize() for x in posts]
        paginator = Paginator(posts, 50)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'type': 'hashtag',
        'name': name,
        'top_hashtags': top_hashtags
    }
    return render(request, 'posts/posts.html', context)
