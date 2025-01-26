from django.apps import AppConfig
from django.db.models.signals import class_prepared
from django.dispatch import receiver

class TaskManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager'

@receiver(class_prepared)
def model_prepared(sender, **kwargs):
    print(f"Model prepared: {sender.__name__}")

    
