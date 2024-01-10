import hashlib

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .tokens import obtain_authentication_token


@api_view(['POST'])
def obtain_token(request):
    user = request.user if request.user.is_authenticated \
        else authenticate(request, **request.data)
    if user:
        token = obtain_authentication_token(user)
        return Response({"token": token}, status=status.HTTP_200_OK)

    return Response({"error": "Please ensure your credentials are valid."},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def refresh_token(request):
    secret = request.META.get('HTTP_AUTHORIZATION')

    if not secret:
        token = request.data.get('token')
        if not token:
            return Response({"error": "Token is required."},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            secret = token
    else:
        if len(secret.split()) == 2 and secret.split()[0].lower() == 'token':
            secret = secret.split()[1]
        else:
            return Response({"error": "Invalid Token header"},
                            status=status.HTTP_400_BAD_REQUEST)

    token = hashlib.sha256(secret.encode()).hexdigest()[:32]

    user_token = request.user.token

    if not user_token.is_valid() or user_token.token != token:
        return Response({"error": "Token has expired or is invalid"},
                        status=status.HTTP_403_FORBIDDEN)

    new_token = obtain_authentication_token(request.user)
    return Response({"token": new_token}, status=status.HTTP_200_OK)
