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

	def test_resume_page_returns_ok(self):
		response = self.client.get(reverse('resume'))

		self.assertEqual(response.status_code, 200)

	def test_contact_page_returns_ok(self):
		response = self.client.get(reverse('contact'))

		self.assertEqual(response.status_code, 200)

	def test_robots_txt_disallows_admin(self):
		response = self.client.get('/robots.txt')

		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Disallow: /admin/', response.content)

	def test_sitemap_xml_returns_ok(self):
		response = self.client.get('/sitemap.xml')

		self.assertEqual(response.status_code, 200)
		self.assertIn(b'urlset', response.content)

	def test_contact_post_missing_fields_shows_error(self):
		response = self.client.post(reverse('contact'), {'name': '', 'email': '', 'message': ''})

		# Should redirect back to contact page
		self.assertEqual(response.status_code, 302)

