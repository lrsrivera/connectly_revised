from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer
from .pagination import CustomPagination


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    paginator = CustomPagination()
    paginated_users = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(paginated_users, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    try:
        print(f"Authenticated user: {request.user}")
        print(f"User type: {type(request.user)}")

       
        if not isinstance(request.user, User):
            return Response({"error": "Invalid user or authentication failed"}, status=401)

        
        tasks = Task.objects.filter(user=request.user)

        
        title = request.GET.get('title')
        if title:
            tasks = tasks.filter(title__icontains=title)

        
        is_completed = request.GET.get('is_completed')
        if is_completed:
            if is_completed.lower() not in ['true', 'false']:
                return Response(
                    {"error": "Invalid value for 'is_completed'. Use 'true' or 'false'."},
                    status=400
                )
            tasks = tasks.filter(is_completed=is_completed.lower() == 'true')

    
        paginator = CustomPagination()
        paginated_tasks = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(paginated_tasks, many=True)

        
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        print(f"Error: {str(e)}")  
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
 
    data = request.data.copy()
    data['user'] = request.user.id  
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    try:
      
        task = Task.objects.get(id=task_id, user=request.user)  
    except Task.DoesNotExist:
        return Response({"error": "Task not found or access denied"}, status=404)

   
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, task_id):
    try:
       
        task = Task.objects.get(id=task_id, user=request.user)  
        task.delete()
        return Response({"message": "Task deleted successfully"})
    except Task.DoesNotExist:
        return Response({"error": "Task not found or access denied"}, status=404)
