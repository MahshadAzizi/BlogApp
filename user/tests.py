from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from user.models import User
from rest_framework import status


class TestUser(APITestCase):
    def setUp(self):
        self.client = APIClient()

    @staticmethod
    def create_user(username, password):
        user = User.objects.create_user(
            username, password
        )
        context = {
            'user': user,
            'username': user.username,
            'password': password
        }
        return context

    @staticmethod
    def create_super_user(username, password):
        user = User.objects.create_superuser(
            username, password
        )
        context = {
            'user': user,
            'username': user.username,
            'password': password
        }
        return context

    def get_token_ok(self, username, password):
        url = reverse('login')
        resp = self.client.post(
            url,
            {"username": username, "password": password}, HHTP_REMOTE_ADDR='127.0.0.1', format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in resp.data['results'])
        self.assertTrue("refresh" in resp.data['results'])
        self.access = resp.data['results']["access"]
        self.refresh = resp.data['results']["refresh"]
        tokens = {'access': self.access, 'refresh': self.refresh}
        return tokens

    def test_login(self):
        user = self.create_user('admin3', '1234')
        url = reverse('login')
        tokens = self.get_token_ok(user['username'], user['password'])
        token = f'Bearer {tokens["access"]}'
        response = self.client.post(
            url, data={'username': user['username'], "password": user['password']},
            HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_token_not_exist(self):
        url = reverse('login')
        username = 'abcd'
        password = "123"
        resp = self.client.post(
            url,
            {"username": username, "password": password}, HHTP_REMOTE_ADDR='127.0.0.1',
            format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        user = self.create_user('admin3', '1234')
        tokens = self.get_token_ok(user['username'], user['password'])
        url = reverse('logout')
        token = f'Bearer {tokens["access"]}'
        response = self.client.post(
            url, {'refresh_token': tokens["refresh"]}, HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

