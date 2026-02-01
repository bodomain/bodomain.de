from django.test import TestCase, Client
from django.urls import reverse
import json

class TerminalTests(TestCase):
    def test_index_view(self):
        client = Client()
        # The index view is now at /terminal/
        response = client.get('/terminal/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BODOMAIN.DE")

    def test_command_api(self):
        client = Client()
        # The API is at /terminal/api/command/
        # We can use reverse to find it dynamically
        url = reverse('command')
        self.assertEqual(url, '/terminal/api/command/')
        
        data = {'command': 'help'}
        response = client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('output', response_data)
        self.assertIn('Available commands', response_data['output'])