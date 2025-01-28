from rest_framework import serializers
from .models import User, Task, Post, Comment

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    is_verified_email = serializers.BooleanField(source='is_verified', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_verified_email', 'created_at']

    def validate_username(self, value):
        """Custom validation for username uniqueness."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)  # Display user's username

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_completed', 'user']

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    liked_by = serializers.SlugRelatedField(slug_field='username', many=True, read_only=True)  # Display usernames of likes

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'is_published', 'author', 'author_name', 'liked_by']

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='post.title', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_title', 'user', 'user_name', 'content', 'created_at']
