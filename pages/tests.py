from django.test import TestCase, Client
from django.urls import reverse

class PageTests(TestCase):
    def test_home_page(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to BoDomain")
        self.assertContains(response, "Launch Terminal")

    def test_terminal_page_moved(self):
        client = Client()
        response = client.get('/terminal/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BODOMAIN.DE")
        self.assertContains(response, "EXIT TO HOME")