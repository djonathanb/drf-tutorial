from rest_framework import status
from django.test import TestCase
from snippets.models import Snippet


class SnippetsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.hello_world_snippet = Snippet.objects.create(code='print("hello, world")')
        cls.foo_bar_snippet = Snippet.objects.create(code='foo = "bar"')

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
            'title': '',
            'code': 'print(123)',
            'linenos': 'false',
            'language': 'python',
            'style': 'friendly'
        })
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
        self.assertEquals(body['id'], 1)
        self.assertEqual(body['code'], self.hello_world_snippet.code)

    def test_retrieve_not_found(self):
        response = self.client.get('/snippets/0/')
        # Check that the response is 404 NOT_FOUND.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update(self):
        response = self.client.put('/snippets/1/', {
            'title': 'Updated hello world',
            'code': 'print("hello, world")',
            'linenos': 'false',
            'language': 'python',
            'style': 'friendly'
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Parse response body and check data.
        body = response.json()
        self.assertEqual(body['id'], self.hello_world_snippet.id)
        self.assertEqual(body['code'], self.hello_world_snippet.code)
        self.assertEqual(body['title'], 'Updated hello world')

    def test_update_not_found(self):
        response = self.client.put('/snippets/0/')
        # Check that the response is 404 NOT_FOUND.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy(self):
        response = self.client.delete('/snippets/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Send GET request to verify if is really removed.
        response = self.client.delete('/snippets/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_not_found(self):
        response = self.client.delete('/snippets/0/')
        # Check that the response is 404 NOT_FOUND.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
