from rest_framework import serializers
from .models import Task
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    is_urgent = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user']

    def get_is_overdue(self, obj):
        if obj.deadline and obj.status != 'DONE':
            deadline = obj.deadline
            now_time = timezone.now()
            if timezone.is_naive(deadline):
                deadline = timezone.make_aware(deadline, timezone.get_current_timezone())
            return deadline < now_time
        return False

    def get_is_urgent(self, obj):
        if obj.deadline and obj.status != 'DONE':
            seconds_left = (obj.deadline - timezone.now()).total_seconds()
            return 0 < seconds_left < 86400
        return False

