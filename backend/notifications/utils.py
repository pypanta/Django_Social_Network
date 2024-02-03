from .models import Notification


def send_notification(sender, recipient, notification_type, content_object):
    """
    Send a notification from one user to another.

    Parameters:
    - sender: User object, representing the user who sends the notification.
    - recipient: User object, representing the user who will receive the
                 notification.
    - notification_type: str, the type of the notification.
    - content_object: content object (post, comment, etc...)

    Return: Notification object

    Example of usage:
        user = User.objects.first()
        post = Post.objects.first()

        send_notification(user, post.created_by, 'postlike', post)
    """

    if sender.full_name:
        user = sender.full_name
    elif sender.username:
        user = sender.username
    else:
        user = sender.email

    match notification_type:
        case "newfriendrequest":
            message = f"{user} sent you a friend request"
        case "acceptedfriendrequest":
            message = f"{user} accepted friend request"
        case "rejectedfriendrequest":
            message = f"{user} rejected friend request"
        case "postlike":
            message = f"{user} liked one of your posts"
        case "postcomment":
            message = f"{user} commented one of your posts"
        case _:
            raise ValueError("Incorrect notification type")

    notification = Notification.objects.create(
        created_by=sender,
        created_for=recipient,
        message=message,
        notification_type=notification_type,
        content_object=content_object)

    return notification
