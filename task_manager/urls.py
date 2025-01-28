from django.urls import path
from . import views

urlpatterns = [
    #User URLS
    path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/verify/', views.verify_email, name='verify_email'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),

    #Tasks URLS
    path('tasks/', views.get_tasks, name='get_tasks'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),

    #Post URLS
    path('posts/', views.get_posts, name='get_posts'),  
    path('posts/create/', views.create_post, name='create_post'),  
    path('posts/<int:post_id>/update/', views.update_post, name='update_post'),  
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),  
    path('posts/<int:post_id>/like/', views.like_post, name='like_post'),  
    path('posts/<int:post_id>/unlike/', views.unlike_post, name='unlike_post'),  
    path('posts/<int:post_id>/comments/', views.get_post_comments, name='get_post_comments'),  

    #Comments
    path('comments/create/', views.create_comment, name='create_comment'), 
    path('comments/', views.get_comments, name='get_comments'),  
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),  
]
