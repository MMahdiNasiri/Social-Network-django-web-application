from django.urls import path
from .views import (
    tweet_action,
    tweet_detail,
    tweet_delete,
    tweet_list,
    tweet_create
)


urlpatterns = [
    path('', tweet_list),
    path('action/', tweet_action),
    path('create-tweet/', tweet_create),
    path('<int:tweet_id>/', tweet_detail),
    path('<int:tweet_id>/delete/', tweet_delete),
]
