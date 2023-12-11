from rest_framework import generics, status
from rest_framework.response import Response

from accounts.api.authentication import JWTAuthentication
from accounts.models import User

from ..models import Conversation, ConversationMessage
from .serializers import (
    ConversationDetailSerializer,
    ConversationMessageSerializer,
    ConversationSerializer
)


class ConversationListCreateDeleteAPIView(generics.ListCreateAPIView,
                                          generics.DestroyAPIView):
    # queryset = Conversation.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        queryset = Conversation.objects.filter(users__in=[self.request.user])
        return queryset

    def perform_create(self, serializer):
        serializer.save(**serializer.initial_data)

    def create(self, request, *args, **kwargs):
        user1 = request.user
        user2 = User.objects.get(id=kwargs.get('pk'))
        conversation = Conversation.objects.filter(users__in=[user1]) \
                                           .filter(users__in=[user2])
        if conversation.exists():
            return self.list(request, *args, **kwargs)
        request.data['user1'] = user1
        request.data['user2'] = user2
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ConversationDetailAPIView(generics.RetrieveAPIView):
    queryset = Conversation.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ConversationDetailSerializer


class ConversationMessageCreateAPIView(generics.CreateAPIView):
    queryset = ConversationMessage.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ConversationMessageSerializer

    def perform_create(self, serializer):
        serializer.save(**serializer.initial_data)

    def create(self, request, *args, **kwargs):
        conversation = Conversation.objects.get(id=kwargs.get('pk'))
        sent_to = conversation.users.exclude(id=request.user.id).first()
        request.data['conversation'] = conversation
        request.data['created_by'] = request.user
        request.data['sent_to'] = sent_to
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)
