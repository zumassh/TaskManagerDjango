from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    PRIORITY_CHOICES = [('CRITICAL', 'Critical'), ('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low')]
    STATUS_CHOICES = [('TODO', 'К выполнению'), ('IN_PROGRESS', 'В работе'), ('DONE', 'Завершено')]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    tags = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_urgent = models.BooleanField(default=False)
    is_overdue = models.BooleanField(default=False)

    def update_status_flags(self):
        now = timezone.now()
        if self.deadline:
            self.is_overdue = self.deadline < now
            self.is_urgent = (self.deadline - now).total_seconds() < 86400
        else:
            self.is_overdue = False
            self.is_urgent = False

    def save(self, *args, **kwargs):
        self.update_status_flags()
        super().save(*args, **kwargs)

