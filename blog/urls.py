from django.urls import path
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    #path('post/new/', views.create_post, name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    #path('post/<int:pk>/', views.add_comment, name='add_comment'),
    path('about/', views.about, name='blog-about'),
   path('comment/<int:pk>/block/', views.comment_block, name='comment_block'),
	path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]


