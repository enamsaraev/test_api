from django.urls import path, include

from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='list_of_users'),
    path('posts/', views.PostList.as_view(), name='list_of_posts'),
    path('posts/by_date/', views.ShowPostsByDate.as_view(), name='posts_by_date'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('users/<int:pk>/subscribe/', views.CreateSubscription.as_view(), name='create_a_subscription'),
]
