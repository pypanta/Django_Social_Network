from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ConversationListCreateDeleteAPIView.as_view(),
         name='conversations'),
    path('<uuid:pk>/', views.ConversationDetailAPIView.as_view(),
         name='conversation-detail'),
    path('<uuid:pk>/create/',
         views.ConversationListCreateDeleteAPIView.as_view(),
         name='conversation-create'),
    path('<uuid:pk>/delete/',
         views.ConversationListCreateDeleteAPIView.as_view(),
         name='conversation-delete'),
    path('<uuid:pk>/send/', views.ConversationMessageCreateAPIView.as_view(),
         name='conversation-send-message'),
]
