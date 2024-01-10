from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Token

User = get_user_model()


class TestAuthToken(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             email='test@example.com',
                                             password='test1234')
        self.client.force_login(self.user)

    def test_(self):
        response = self.client.post(reverse('obtain_token'),
                                    {'username': 'test',
                                     'password': 'test1234'},
                                    format='json')
        token = response.data.get('token')

        headers = {'Authorization': f'Token {token}'}
        response = self.client.post(reverse('refresh_token'), headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_model(self):
        token = Token(user=self.user, token="010101")
        token.save()
        self.assertEqual(str(token), "010101")

    def test_obtain_token(self):
        self.client.logout()
        response = self.client.post(reverse('obtain_token'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):
        response = self.client.post(reverse('obtain_token'),
                                    {'username': 'test',
                                     'password': 'test1234'},
                                    format='json')
        response = self.client.post(reverse('refresh_token'),
                                    data={'token': '010101'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_refresh_token_invalid(self):
        response = self.client.post(reverse('refresh_token'),
                                    data={'token': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token_header(self):
        response = self.client.post(reverse('refresh_token'),
                                    headers={'Authorization': 'Bearer '})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
