from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from ..models import Conversation, ConversationMessage


class ConversationAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='user1@email.com')
        self.user1.set_password('test1234')
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create(email='user2@email.com')
        self.user2.set_password('test1234')
        self.user2.is_active = True
        self.user2.save()
        self.conversation = Conversation.objects.create()
        self.conversation.users.add(self.user1, self.user2)

        url = reverse('accounts:login')
        payload = {'email': 'user1@email.com', 'password': 'test1234'}
        self.client.post(url, payload, format='json')

    def test_conversation_list_view(self):
        url = reverse('chat:conversations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], str(self.conversation.id))
        self.assertEqual(len(response.data[0]['users']), 2)

    def test_conversation_exist_create_view(self):
        url = reverse('chat:conversation-create', args=[self.user2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Conversation.objects.count(), 1)

    def test_conversation_new_create_view(self):
        new_user = User.objects.create(email='newuser@email.com')
        new_user.set_password('test1234')
        url = reverse('chat:conversation-create', args=[new_user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 2)
        self.assertTrue(
            Conversation.objects.filter(id=response.data['id']).exists())
        self.assertTrue(
            Conversation.objects.filter(id=response.data['id'])
                                .filter(users__in=[new_user]).exists()
        )

    def test_conversation_detail_view(self):
        url = reverse('chat:conversation-detail', args=[self.conversation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.conversation.id))

    def test_conversation_delete_view(self):
        url = reverse('chat:conversation-delete', args=[self.conversation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Conversation.objects.count(), 0)

    def test_conversation_message_create(self):
        url = reverse('chat:conversation-send-message',
                      args=[self.conversation.id])
        payload = {'body': 'Test message'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(self.conversation.messages.count(), 1)
        self.assertTrue(
            self.conversation.messages.filter(id=response.data['id']).exists()
        )
        self.assertEqual(response.data['sent_to']['id'], str(self.user2.id))
        self.assertEqual(response.data['created_by']['id'],
                         str(self.user1.id))
