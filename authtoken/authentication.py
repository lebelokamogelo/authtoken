import hashlib

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from .models import Token


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:

            token = hashlib.sha256(auth[1]).hexdigest()[:32]
        except ValueError:
            msg = 'invalid auth token'
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token, request)

    def authenticate_credentials(self, token, request=None):
        """
        Authenticate the token.
        """

        user = None
        try:
            user = Token.objects.get(token=token).user
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('invalid auth token')

        if user is None or not user.is_active:
            raise exceptions.AuthenticationFailed('Authentication failed')

        return user, token

    def authenticate_header(self, request):
        return 'Token'
