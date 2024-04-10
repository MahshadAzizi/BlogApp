from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from user.models import User
from rest_framework import status


class TestBlog(APITestCase):
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

    def test_get_all_posts_comments(self):
        user = self.create_user('admin', '1234')
        url = reverse('blogs')
        tokens = self.get_token_ok(user['username'], user['password'])
        token = f'Bearer {tokens["access"]}'
        response = self.client.get(
            url, HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_create_post(self):
        user = self.create_user('admin', '1234')
        url = reverse('blogs')
        tokens = self.get_token_ok(user['username'], user['password'])
        token = f'Bearer {tokens["access"]}'
        response = self.client.post(
            url, data={'title': 'test', 'content': 'hello'},
            HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_update_post(self):
        user = self.create_user('admin2', '1234')
        post = self.test_create_post()
        url = reverse('blog-detail', kwargs={'title': post['results']['title']})
        tokens = self.get_token_ok(user['username'], user['password'])
        token = f'Bearer {tokens["access"]}'
        response = self.client.patch(
            url, data={'title': 'test1'},
            HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_post_detail(self):
        user = self.create_user('admin2', '1234')
        post = self.test_create_post()
        url = reverse('blog-detail', kwargs={'title': post['results']['title']})
        tokens = self.get_token_ok(user['username'], user['password'])
        token = f'Bearer {tokens["access"]}'
        response = self.client.get(
            url, HTTP_AUTHORIZATION=token, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

