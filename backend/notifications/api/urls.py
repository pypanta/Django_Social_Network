from django.urls import path

from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationsAPIView.as_view(), name='notifications'),
]
