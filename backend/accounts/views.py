from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import User


def activate_user(request, user_id):
    """
    Activate user account

    Parameters:
        user_id: UUID
    """
    user = get_object_or_404(User, id=user_id)

    user.is_active = True
    user.save()

    context = """
    Your account is now activated! Please
    <a href="http://localhost:5173/login">Click here</a> to log in.
    """

    return HttpResponse(content=context)
