from django.test import TestCase

from accounts.models import User

from ..models import Conversation, ConversationMessage


class ConversationModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='user1@email.com',
                                         password='test1234')
        self.user2 = User.objects.create(email='user2@email.com',
                                         password='test1234')

    def test_create_conversation(self):
        conversation = Conversation.objects.create()
        conversation.users.add(self.user1, self.user2)
        self.assertEqual(Conversation.objects.count(), 1)
        self.assertEqual(conversation.users.count(), 2)
        self.assertTrue(
            self.user1.conversations.filter(id=conversation.id).exists()
        )
        self.assertTrue(
            self.user2.conversations.filter(id=conversation.id).exists()
        )


class ConversationMessageTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='user1@email.com',
                                         password='test1234')
        self.user2 = User.objects.create(email='user2@email.com',
                                         password='test1234')
        self.conversation = Conversation.objects.create()
        self.conversation.users.add(self.user1, self.user2)

    def test_create_conversation_message(self):
        message = ConversationMessage.objects.create(
            conversation=self.conversation,
            created_by=self.user1,
            sent_to=self.user2,
            body='Test message'
        )
        self.assertEqual(ConversationMessage.objects.count(), 1)
        self.assertTrue(
            self.conversation.messages.filter(id=message.id).exists()
        )
