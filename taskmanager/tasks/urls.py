from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, RegisterView, LogoutView, DeleteAccountView
from rest_framework.authtoken.views import ObtainAuthToken


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('login/', ObtainAuthToken.as_view()),
    path('logout/', LogoutView.as_view()),
    path('delete_account/', DeleteAccountView.as_view()),
]
