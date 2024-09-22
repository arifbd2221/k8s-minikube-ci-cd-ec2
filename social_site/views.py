from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .models import (
    Post, Like, Comment,
    Like, Friendship, Message,
    Notification, 
)

from .serializers import (
    UserSerializer, PostSerializer, CommentSerializer,
    
)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        
        if not created:
            return Response({"message": "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        like = Like.objects.filter(post=post, user=request.user).first()
        
        if like:
            like.delete()
            return Response({"message": "Like removed"}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({"message": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)


class SendFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, to_user_id):
        to_user = User.objects.get(pk=to_user_id)
        if Friendship.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({"message": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)
        
        Friendship.objects.create(from_user=request.user, to_user=to_user)
        return Response({"message": "Friend request sent"}, status=status.HTTP_201_CREATED)

class AcceptFriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, from_user_id):
        from_user = User.objects.get(pk=from_user_id)
        friendship = Friendship.objects.filter(from_user=from_user, to_user=request.user).first()
        
        if friendship:
            friendship.accepted = True
            friendship.save()
            return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
        
        return Response({"message": "No friend request found"}, status=status.HTTP_400_BAD_REQUEST)


