from django.db import models
from django.utils.timezone import now

# User Model
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.username

# Post Model
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')  
    title = models.CharField(max_length=100)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(default=now)  

    def short_content(self):
        """Returns a truncated version of the content."""
        return self.content[:50] + "..." if len(self.content) > 50 else self.content

    def __str__(self):
        return self.title

# Task Model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title

# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
