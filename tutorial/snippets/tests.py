"""
Integration tests for Snippets Module.
"""

import base64
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from snippets.models import Snippet


class UsersTest(TestCase):
    """
    Integration tests for users view.
    """

    def setUp(self):
        # Set up data for the whole TestCase.
        self.trainee_coder = User.objects.create(username='trainee_coder')
        self.master_coder = User.objects.create(username='master_coder')

    def test_list(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Parse response body and check data.
        body = response.json()
        self.assertEqual(len(body), 2)
        self.assertEqual(body[0]['username'], self.trainee_coder.username)
        self.assertEqual(body[1]['username'], self.master_coder.username)

    def test_retrieve(self):
        response = self.client.get('/users/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Parse response body and check data.
        body = response.json()
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['username'], self.trainee_coder.username)

    def test_retrieve_not_found(self):
        response = self.client.get('/users/0/')
        # Check that the response is 404 NOT_FOUND.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SnippetsTest(TestCase):
    """
    Integration tests for snippets views.
    """

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.auth_headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(b'admin:123456').decode('utf-8'),
        }

        password = make_password('123456')
        cls.owner = User.objects.create(username='admin', password=password)
    
    def setUp(self):
        self.hello_world_snippet = Snippet.objects.create(code='print("hello, world")', owner=self.owner)
        self.foo_bar_snippet = Snippet.objects.create(code='foo = "bar"', owner=self.owner)

    def test_list(self):
        response = self.client.get('/snippets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Parse response body and check data.
        body = response.json()
        self.assertEqual(len(body), 2)
        self.assertEqual(body[0]['code'], self.hello_world_snippet.code)
        self.assertEqual(body[1]['code'], self.foo_bar_snippet.code)

    def test_create(self):
        response = self.client.post('/snippets/', {
            'code': 'print(123)',
        }, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Parse response body and check data.
        body = response.json()
        self.assertIsNotNone(body['id'])
        self.assertEqual(body['code'], 'print(123)')

    def test_retrieve(self):
        response = self.client.get('/snippets/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Parse response body and check data.
        body = response.json()
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['code'], self.hello_world_snippet.code)

    def test_retrieve_not_found(self):
        response = self.client.get('/snippets/0/')
        # Check that the response is 404 NOT_FOUND.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update(self):
        response = self.client.put('/snippets/1/', {
            'title': 'Updated hello world',
            'code': 'print("hello, world")',
        }, content_type='application/json', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Parse response body and check data.
        body = response.json()
        self.assertEqual(body['id'], self.hello_world_snippet.id)
        self.assertEqual(body['code'], self.hello_world_snippet.code)
        self.assertEqual(body['title'], 'Updated hello world')

    def test_update_not_found(self):
        response = self.client.put('/snippets/0/', **self.auth_headers)
        # Check that the response is 404 NOT_FOUND.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy(self):
        response = self.client.delete('/snippets/1/', **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Send GET request to verify if is really removed.
        response = self.client.get('/snippets/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_not_found(self):
        response = self.client.delete('/snippets/0/', **self.auth_headers)
        # Check that the response is 404 NOT_FOUND.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
