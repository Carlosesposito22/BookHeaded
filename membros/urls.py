from django.urls import path
from .views import user_register

urlpatterns = [
    path('register/', user_register, name='register'),
]