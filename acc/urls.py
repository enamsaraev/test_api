from django.urls import path, include

from . import views

urlpatterns = [
    path('createacc/', views.CreateProfile.as_view(), name='create_acc'),
    path('createpost/', views.CreatePostView.as_view(), name='create_post'),
    path('myposts/', views.ShowMyPostsView.as_view(), name='shows_users_posts'),
    path('mysub/', views.ShowMySubscriptions.as_view(), name='users_subscriptions'),
]