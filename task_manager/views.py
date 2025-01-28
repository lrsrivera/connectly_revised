from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import User, Task, Post, Comment
from .serializers import UserSerializer, TaskSerializer, PostSerializer, CommentSerializer

# Users
@api_view(['GET'])
def get_users(request):
    """Retrieve all users with pagination."""
    paginator = PageNumberPagination()
    paginator.page_size = 10  
    users = User.objects.all()
    paginated_users = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(paginated_users, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def create_user(request):
    """Create a new user."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def verify_email(request, user_id):
    """Mark a user's email as verified."""
    if not isinstance(user_id, int) or user_id <= 0:
        return Response({"error": "Positive integer user ID is required."}, status=400)
    try:
        user = User.objects.get(id=user_id)
        user.is_verified = True
        user.save()
        return Response({
            "message": f"Email for {user.username} has been verified.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_verified": user.is_verified
            }
        }, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    
@api_view(['DELETE'])
def delete_user(request, user_id):
    """Delete a user by ID."""
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": f"User {user.username} has been deleted successfully."}, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


# Posts
@api_view(['GET'])
def get_posts(request):
    """Retrieve all posts."""
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_post(request):
    """Create a new post."""
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def like_post(request, post_id):
    """Allow a user to like a post."""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

    user_id = request.data.get('user_id')  
    if not user_id:
        return Response({"error": "User ID is required"}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    post.liked_by.add(user)
    return Response({
        "message": f"Post '{post.title}' liked by {user.username}.",
        "post_id": post.id,
        "liked_by": [user.username for user in post.liked_by.all()]
    }, status=200)

@api_view(['PUT'])
def unlike_post(request, post_id):
    """Allow a user to unlike a post."""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

    user_id = request.data.get('user_id')  
    if not user_id:
        return Response({"error": "User ID is required"}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if user in post.liked_by.all():
        post.liked_by.remove(user)
        return Response({
            "message": f"Post '{post.title}' unliked by {user.username}.",
            "post_id": post.id,
            "liked_by": [user.username for user in post.liked_by.all()]
        }, status=200)
    else:
        return Response({"error": f"{user.username} has not liked this post."}, status=400)



@api_view(['PUT'])
def update_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Post updated successfully", "data": serializer.data}, status=200)
    return Response({"error": "Invalid data", "details": serializer.errors}, status=400)

@api_view(['DELETE'])
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=200)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)



# Tasks
@api_view(['GET'])
def get_tasks(request):
    """Retrieve all tasks with pagination."""
    paginator = PageNumberPagination()
    paginator.page_size = 10 
    tasks = Task.objects.all()
    paginated_tasks = paginator.paginate_queryset(tasks, request)
    serializer = TaskSerializer(paginated_tasks, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def create_task(request):
    """Create a new task."""
    data = request.data
    data.setdefault("description", "")  
    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response({"error": "Invalid task data", "details": serializer.errors}, status=400)

@api_view(['PUT'])
def update_task(request, task_id):
    """Update an existing task."""
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)
    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Task updated successfully",
            "data": serializer.data
        })
    return Response({"error": "Invalid data", "details": serializer.errors}, status=400)

@api_view(['DELETE'])
def delete_task(request, task_id):
    """Delete a task by ID."""
    try:
        task = Task.objects.get(id=task_id)
        task.delete()
        return Response({"message": "Task deleted successfully"}, status=200)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

# Comments
@api_view(['GET'])
def get_comments(request):
    """Retrieve all comments."""
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_post_comments(request, post_id):
    """Retrieve all comments for a specific post."""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

    comments = post.comments.all()  # Access the related comments
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_comment(request):
    """Create a new comment."""
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_comment(request, comment_id):
    """Delete a comment by its ID."""
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return Response({"message": "Comment deleted"}, status=200)
    except Comment.DoesNotExist:
        return Response({"error": "Comment not found"}, status=404)

