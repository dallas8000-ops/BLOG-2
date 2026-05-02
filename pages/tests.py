from django.test import TestCase
from django.urls import reverse


class PagesTests(TestCase):
	def test_home_page_returns_ok(self):
		response = self.client.get(reverse('home'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Barney R. Gilliom')

	def test_about_page_returns_ok(self):
		response = self.client.get(reverse('about'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'About Me')

	def test_favicon_redirect_exists(self):
		response = self.client.get('/favicon.ico')

		self.assertEqual(response.status_code, 301)
