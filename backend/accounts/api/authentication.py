from rest_framework_simplejwt.authentication import \
    JWTStatelessUserAuthentication

from ..models import User


class JWTAuthentication(JWTStatelessUserAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get('access') or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        user = User.objects.get(id=validated_token.get('user_id'))
        return (user, None)
