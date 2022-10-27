from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Posts
    path('posts/', views.posts, name='posts'),
    # Page for adding new post
    path('new_post/', views.new_post, name='new_post'),
    # Page for a single post
    path('posts/<int:post_id>/', views.post, name='post'),
    # Page for editing post
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    #Page for deleting post
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    

    # Page for commenting post
    path('comment_post/<int:post_id>/', views.comment_post, name='comment_post'),
    # Page for deleting comment
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    # Page for editing comment
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    
    # Page for user's posts
    path('user_posts/', views.user_posts, name='user_posts'),
    # Page for adding new user's post
    #path('user_new_post/', views.user_new_post, name='user_new_post'),
]