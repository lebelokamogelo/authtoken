from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TestAuthToken(APITestCase):
    def test_(self):
        User.objects.create_user(username='test', email='test@example.com', password='test1234')

        response = self.client.post(reverse('obtain_token'), {'username': 'test', 'password': 'test1234'}, format='json')
        token = response.data.get('token')

        headers = {'Authorization': f'Token {token}'}
        response = self.client.post(reverse('refresh_token'), headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
