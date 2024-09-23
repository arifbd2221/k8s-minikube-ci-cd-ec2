# todo/views.py
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework import status


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    View to list all categories or create a new category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskListCreateView(generics.ListCreateAPIView):
    """
    View to list all tasks or create a new task.
    Only authenticated users can create tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific task.
    Only the owner of the task can update or delete it.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)


class HealthCheckVIew(APIView):
    def get(self, request, *args, **kwargs):
        # You can add more checks here (e.g., database, cache, etc.)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)