from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.last_posts_view, name='last-posts'),
    path('home/', views.home, name='home'),
    path('like', views.like, name='like'),
    path('republish', views.republish_view, name='republish'),
    path('createpost', views.post_create_view, name='create-post'),
    path('detail/<int:post_id>/create-comment', views.create_comment, name='create-comment'),
    path('detail/<int:post_id>/', views.post_detail_view, name='detail-post'),
    path('hashtag/<str:name>/', views.hashtags, name='hashtags')
]
