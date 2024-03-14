from django.forms import ValidationError
from rest_framework import generics
from todo_list.models import Task
from .serializers import TaskSerializer

class TaskListCreate(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from django.http import Http404

class ToDoItemDetail(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        todo_item = self.get_object(pk)
        serializer = TaskSerializer(todo_item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        todo_item = self.get_object(pk)
        serializer = TaskSerializer(todo_item, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo_item = self.get_object(pk)
        todo_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)