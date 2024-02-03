from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.authentication import JWTAuthentication

from .serializers import NotificationSerializer


class NotificationsAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        notifications = user.received_notifications.filter(is_read=False)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data

        if data.get('id'):
            notification = user.received_notifications.filter(id=data['id'])
            if notification.exists():
                notification = notification.first()
                notification.is_read = True
                notification.save()
                return Response({
                    'message': 'Notification successfully deleted!'
                    }, status=status.HTTP_204_NO_CONTENT)
            return Response({'message': 'Notification not found!'},
                            status=status.HTTP_404_NOT_FOUND)

        if data.get('all'):
            for notification in user.received_notifications.all():
                notification.is_read = True
                notification.save()
            return Response({
                'message': 'Notifications successfully deleted!'
                }, status=status.HTTP_204_NO_CONTENT)

        return Response({
            'message': f"No notifications were found with ID: "
                       f"{data.get('id')}!"},
            status=status.HTTP_404_NOT_FOUND)
