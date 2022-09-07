from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='feed-home'),
    path('p/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('p/<int:pk>/comment', views.add_comment, name='add-comment'),
    path('p/<int:pk>/like', views.like_post, name='like-post'),
    path('p/create-post/', views.create_post, name='create-post'),
    path('p/<int:pk>/delete', views.delete_post, name='delete-post')
]