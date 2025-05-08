from celery import shared_task
from .models import Task

@shared_task
def update_all_tasks_status():
    for task in Task.objects.all():
        task.update_status_flags()
        task.save()
