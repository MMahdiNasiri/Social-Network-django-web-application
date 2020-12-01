from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect



def home(request, *args, **kwargs):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'pages/home.html', context={"username": username})


def tweets_list_view(request, *args, **kwargs):
    return render(request, 'tweets/list.html')

def tweets_detail_view(request, tweet_id, *args, **kwargs):
    return render(request, 'tweets/detail.html', context={"tweet_id": tweet_id})


def tweets_profile_view(request, username, *args, **kwargs):
    return render(request, 'tweets/profile.html', context={"profile_username": username})




