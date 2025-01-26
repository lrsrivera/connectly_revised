from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_completed', 'user')  
    search_fields = ('title', 'user__username') 
    list_filter = ('is_completed',) 
