import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from user.models import User


class Auth0Middleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", None)

        if auth_header:
            try:
                token = auth_header.split()[1]  # Extract the token
                payload = jwt.decode(
                    token,
                    settings.AUTH0_CLIENT_SECRET,
                    algorithms=["HS256"],
                    audience=settings.AUTH0_CLIENT_ID,
                )

                # Get or create the user
                user, created = User.objects.get_or_create(
                    email=payload["email"],
                    defaults={"name": payload.get("name", ""), "id": payload["sub"]},
                )
                request.user = user
            except jwt.ExpiredSignatureError:
                request.user = AnonymousUser()
            except jwt.DecodeError:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
