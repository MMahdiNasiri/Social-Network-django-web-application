import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .forms import UpdateProfile, UpdateUser, UpdateImage
from .models import Profile
from posts.models import Post


@login_required(login_url='/accounts/login/')
def profile_update_view(request, *args, **kwargs):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        user_form = UpdateUser(request.POST, instance=user)
        profile_form = UpdateProfile(request.POST, instance=profile)
        if user_form.is_valid():
            user_form.save()
        if profile_form.is_valid():
            profile_form.save()

    else:
        user_form = UpdateUser(instance=user)
        profile_form = UpdateProfile(instance=profile)
    context = {
        "profile_form": profile_form,
        "user_form": user_form,
        "image": profile.profileImage.url
    }
    return render(request, "profiles/editProfile.html", context)


@login_required(login_url='/accounts/login/')
def save_file(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = UpdateImage(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile_img = form.save()

    data = {
        'url': profile_img.profileImage.url
    }
    return JsonResponse(data)


def profile_detail(request, username, *args, **kwargs):
    # get the profile for the passed username
    qs = Profile.objects.filter(user__username=username)
    target_user = User.objects.filter(username=username)
    if not (qs.exists() and target_user.exists()):
        raise Http404
    profile_obj = qs.first()
    target_user = target_user.first()
    # following = target_user.first().following.count()
    posts = Post.objects.filter(user=target_user)
    posts = [x.serialize() for x in posts]
    is_following = False
    if request.user.is_authenticated:
        user = request.user
        is_following = user in profile_obj.followers.all()
        # is_following = profile_obj in user.following.all()
    context = {
        "target_user": target_user,
        "profile": profile_obj,
        "is_following": is_following,
        "posts": posts
    }
    return render(request, "profiles/profile.html", context)


@login_required(login_url='/accounts/login/')
def follow_view(request):
    action_user = request.user
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    followed = body['followed']
    username = body['username'].split('@')[1]
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        raise Http404
    target_profile = qs.first()

    if followed:
        # action for unfollow
        target_profile.followers.remove(action_user)
        data = {
            'type': 'follow'
        }
    else:
        target_profile.followers.add(action_user)
        data = {
            'type': 'follow'
        }
    return JsonResponse(data=data)


