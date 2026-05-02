from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from posts.models import Post, Status

TEST_CREDENTIAL = 'StrongPass123!'


class PublicProfileTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='barney', password=TEST_CREDENTIAL)
		self.other = User.objects.create_user(username='other', password=TEST_CREDENTIAL)
		self.pub, _ = Status.objects.get_or_create(name='published', defaults={'description': 'Published'})
		self.draft, _ = Status.objects.get_or_create(name='draft', defaults={'description': 'Draft'})
		self.pub_post = Post.objects.create(
			title='Public Post', subtitle='sub', body='body', author=self.user, status=self.pub
		)
		self.draft_post = Post.objects.create(
			title='Draft Post', subtitle='sub', body='body', author=self.user, status=self.draft
		)

	def test_public_profile_loads(self):
		response = self.client.get(reverse('public_profile', kwargs={'username': 'barney'}))
		self.assertEqual(response.status_code, 200)

	def test_public_profile_shows_published_posts(self):
		response = self.client.get(reverse('public_profile', kwargs={'username': 'barney'}))
		self.assertContains(response, 'Public Post')

	def test_public_profile_hides_draft_posts(self):
		response = self.client.get(reverse('public_profile', kwargs={'username': 'barney'}))
		self.assertNotContains(response, 'Draft Post')

	def test_public_profile_shows_edit_button_to_owner(self):
		self.client.login(username='barney', password=TEST_CREDENTIAL)
		response = self.client.get(reverse('public_profile', kwargs={'username': 'barney'}))
		self.assertContains(response, 'Edit Profile')

	def test_public_profile_hides_edit_button_from_others(self):
		self.client.login(username='other', password=TEST_CREDENTIAL)
		response = self.client.get(reverse('public_profile', kwargs={'username': 'barney'}))
		self.assertNotContains(response, 'Edit Profile')

	def test_nonexistent_profile_returns_404(self):
		response = self.client.get(reverse('public_profile', kwargs={'username': 'nobody'}))
		self.assertEqual(response.status_code, 404)
