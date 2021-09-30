from django.urls import path
from control.views import staff_login_view, control_posts, control_comments, control_users, delete_obj

urlpatterns = [
    path('stafflogin/', staff_login_view, name='staff-login'),
    path('posts/', control_posts, name='control-posts'),
    path('comments/', control_comments, name='control-comments'),
    path('users/', control_users, name='control-users'),
    path('delete', delete_obj, name='delete-obj'),
]

