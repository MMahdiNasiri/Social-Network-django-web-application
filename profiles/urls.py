from django.urls import path
from .views import profile_detail, follow_view, profile_update_view, save_file

urlpatterns = [
    path('follow', follow_view, name='follow'),
    path('edit/', profile_update_view, name='profile-update'),
    path('savefile', save_file, name='save-file'),
    path('profile/<str:username>/', profile_detail, name='profile'),
]

