import hashlib
import secrets

from .models import Token


def generate_token(user=None):
    secret = secrets.token_hex(16)
    token = hashlib.sha256(secret.encode()).hexdigest()[:32]

    """
    Check if the token already exists in the database
    """
    if Token.objects.filter(token=token).exists():
        return generate_token()

    try:
        instance = Token.objects.get(user=user)
        if instance:
            instance.token = token
            instance.save()

    except Token.DoesNotExist:
        Token.objects.create(user=user, token=token)

    return secret
