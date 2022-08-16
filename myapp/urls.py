from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/detail/<slug:slug>/', views.detail, name='detail'),
    path('post/my-post/<int:pk>/', views.myPost, name='my-post'),

    path('post/create/', views.createPost, name='create-post'),
    path('post/like/<post>/', views.likeView, name='post-like'),
    path('post/update/<slug:slug>/', views.updatePost, name='update-post'),
    path('post/delete/<slug:slug>/', views.deletePost, name='delete-post'),

    path('post/detail/comment/<int:pk>/delete', views.deleteComment, name='delete-comment'),
    path('post/detail/comments/<slug:slug>/update', views.updateComment, name='update-comment'),
]