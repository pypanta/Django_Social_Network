from django.urls import path

from . import views

urlpatterns = [
    path('activate/<uuid:user_id>/', views.activate_user),
]
