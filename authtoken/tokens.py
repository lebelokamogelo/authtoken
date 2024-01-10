import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import Token


def obtain_authentication_token(user=None):
    secret = secrets.token_hex(16)
    token = hashlib.sha256(secret.encode()).hexdigest()[:32]

    """
    Check if the token already exists in the database
    """
    if Token.objects.filter(token=token).exists():
        return obtain_authentication_token()

    try:
        instance = Token.objects.get(user=user)

        if instance:
            instance.token = token
            instance.expire = timezone.now() + (
                settings.TOKEN_EXPIRE if hasattr(settings, 'TOKEN_EXPIRE')
                else timedelta(minutes=5))
            instance.save()

    except Token.DoesNotExist:
        Token.objects.create(user=user, token=token)

    return secret
