from django.utils import timezone

from rest_framework import serializers

from accounts.api.serializers import UserSerializer

from ..models import Conversation, ConversationMessage


class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_time_ago')

    def create(self, validated_data):
        conversation = Conversation.objects.create()
        conversation.users.add(validated_data['user1'],
                               validated_data['user2'])
        return conversation


class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = ('id', 'sent_to', 'created_by', 'created_at_time_ago', 'body')

    def create(self, validated_data):
        conversation = validated_data.get('conversation')
        conversation.modified_at = timezone.now()
        conversation.save()
        return ConversationMessage.objects.create(**validated_data)


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_time_ago', 'messages')
