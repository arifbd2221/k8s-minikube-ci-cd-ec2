from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('posts/', views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', views.LikePostView.as_view(), name='like-post'),
    path('comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('friend-request/send/<int:to_user_id>/', views.SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/accept/<int:from_user_id>/', views.AcceptFriendRequestView.as_view(), name='accept-friend-request'),
]
