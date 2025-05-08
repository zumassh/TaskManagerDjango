from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Task
from .serializers import TaskSerializer
from django.http import HttpResponse
import ics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['priority', 'status', 'is_urgent', 'is_overdue']
    ordering_fields = ['priority', 'status', 'is_urgent', 'is_overdue']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def generate_ics(self, request, pk=None):
        task = self.get_object()
        calendar = ics.Calendar()
        event = ics.Event()
        event.name = task.title
        event.begin = task.deadline if task.deadline else timezone.now()
        event.description = task.description or ''
        calendar.events.add(event)
        response = HttpResponse(str(calendar), content_type='text/calendar')
        response['Content-Disposition'] = f'attachment; filename="task_{task.id}.ics"'
        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Введите имя пользователя и пароль'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Пользователь уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        token = Token.objects.create(user=user)
        return Response({'token': token.key})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class DeleteAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

