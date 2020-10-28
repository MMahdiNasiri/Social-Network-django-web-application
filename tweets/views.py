from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Tweet


def home(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={})

def tweet_list(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, 'content': x.content, 'likes': 12} for x in qs]
    data = {
        'response': tweets_list
    }
    return JsonResponse(data)


def tweet_detail(request, tweet_id, *args, **kwargs):
    data = {
        'id': tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = 'Not found'
        status = 404

    return JsonResponse(data, status=status)
