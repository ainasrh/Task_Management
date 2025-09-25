from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .task_serializers import TaskSerializer, TaskUpdateSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Task
from django.contrib.auth.decorators import login_required



# Create your views here.

class TaskListApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assigned_to=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK )
    
# task updated user

class TaskUpdateApi(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            
        except Task.DoesNotExist:
            return Response({'error': "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        if task.assigned_to != request.user.username:
            return Response({'error': "You can only update your own task"}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




