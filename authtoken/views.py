from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .tokens import generate_token


@api_view(['POST', 'GET'])
def token(request):
    if request.method == 'POST':

        user = authenticate(request, **request.data)
        if user:
            token = generate_token(user)
            return Response({"Token": token}, status=status.HTTP_200_OK)

    return Response({"error": "Unable to log in with provided credentials."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def test(request):
    return Response(status=status.HTTP_200_OK)
