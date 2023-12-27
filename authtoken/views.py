from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Token
from .tokens import obtain_authentication_token


@api_view(['POST'])
def token(request):
    user = request.user if request.user.is_authenticated else authenticate(request, **request.data)
    if user:
        token = obtain_authentication_token(user)
        return Response({"Token": token}, status=status.HTTP_200_OK)

    return Response({"error":
                         "Please ensure your credentials are valid."},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def test(request):
    try:
        token = Token.objects.get(user=request.user)
        if token.is_valid():
            return Response({"error": "Access token has expired."},
                            status=status.HTTP_401_UNAUTHORIZED)
    except Token.DoesNotExist:
        return Response({"error": "Access token does not exist."}, status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_200_OK)
