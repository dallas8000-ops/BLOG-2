from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Post, Status


TEST_CREDENTIAL = 'StrongPass123!'


class AuthFlowTests(TestCase):
	def test_signup_page_loads(self):
		response = self.client.get(reverse('signup'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Sign Up')

	def test_user_can_sign_up(self):
		response = self.client.post(
			reverse('signup'),
			{
				'username': 'newuser',
				'email': 'newuser@example.com',
				'password1': TEST_CREDENTIAL,
				'password2': TEST_CREDENTIAL,
				'avatar': 'images/avatar-default.svg',
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertTrue(User.objects.filter(username='newuser').exists())


class PostCrudTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='barney', password=TEST_CREDENTIAL)
		self.other_user = User.objects.create_user(username='other', password=TEST_CREDENTIAL)
		self.status, _ = Status.objects.get_or_create(name='published', defaults={'description': 'Published post'})
		self.draft_status, _ = Status.objects.get_or_create(name='draft', defaults={'description': 'Draft post'})
		self.archived_status, _ = Status.objects.get_or_create(name='archived', defaults={'description': 'Archived post'})
		self.post = Post.objects.create(
			title='First Post',
			subtitle='Testing subtitle',
			body='Testing body content',
			author=self.user,
			status=self.status,
		)

	def test_post_list_loads(self):
		response = self.client.get(reverse('post_list'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'First Post')

	def test_post_detail_loads(self):
		response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Testing subtitle')

	def test_login_required_for_create(self):
		response = self.client.get(reverse('post_new'))

		self.assertEqual(response.status_code, 302)

	def test_logged_in_user_can_create_post(self):
		self.client.login(username='barney', password=TEST_CREDENTIAL)
		response = self.client.post(
			reverse('post_new'),
			{
				'title': 'Created Post',
				'subtitle': 'Created subtitle',
				'body': 'Created body',
				'status': self.status.pk,
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertTrue(Post.objects.filter(title='Created Post', author=self.user).exists())

	def test_author_can_edit_own_post(self):
		self.client.login(username='barney', password=TEST_CREDENTIAL)
		response = self.client.post(
			reverse('post_edit', kwargs={'pk': self.post.pk}),
			{
				'title': 'Updated Post',
				'subtitle': self.post.subtitle,
				'body': self.post.body,
				'status': self.status.pk,
			},
		)

		self.assertEqual(response.status_code, 302)
		self.post.refresh_from_db()
		self.assertEqual(self.post.title, 'Updated Post')

	def test_non_author_cannot_edit_post(self):
		self.client.login(username='other', password=TEST_CREDENTIAL)
		response = self.client.get(reverse('post_edit', kwargs={'pk': self.post.pk}))

		self.assertEqual(response.status_code, 404)

	def test_author_can_delete_own_post(self):
		self.client.login(username='barney', password=TEST_CREDENTIAL)
		response = self.client.post(reverse('post_delete', kwargs={'pk': self.post.pk}))

		self.assertEqual(response.status_code, 302)
		self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

	def test_draft_and_archived_views_require_login(self):
		draft_post = Post.objects.create(
			title='Draft Post',
			subtitle='Draft subtitle',
			body='Draft body',
			author=self.user,
			status=self.draft_status,
		)
		archived_post = Post.objects.create(
			title='Archived Post',
			subtitle='Archived subtitle',
			body='Archived body',
			author=self.user,
			status=self.archived_status,
		)

		self.assertTrue(draft_post.pk)
		self.assertTrue(archived_post.pk)

		draft_response = self.client.get(reverse('post_draft_list'))
		archived_response = self.client.get(reverse('post_archived_list'))

		self.assertEqual(draft_response.status_code, 302)
		self.assertEqual(archived_response.status_code, 302)

	def test_draft_and_archived_views_show_only_current_users_posts(self):
		Post.objects.create(
			title='Draft Post',
			subtitle='Draft subtitle',
			body='Draft body',
			author=self.user,
			status=self.draft_status,
		)
		Post.objects.create(
			title='Archived Post',
			subtitle='Archived subtitle',
			body='Archived body',
			author=self.user,
			status=self.archived_status,
		)
		Post.objects.create(
			title='Other Draft',
			subtitle='Other subtitle',
			body='Other body',
			author=self.other_user,
			status=self.draft_status,
		)

		self.client.login(username='barney', password=TEST_CREDENTIAL)
		draft_response = self.client.get(reverse('post_draft_list'))
		archived_response = self.client.get(reverse('post_archived_list'))

		self.assertContains(draft_response, 'Draft Post')
		self.assertNotContains(draft_response, 'Other Draft')
		self.assertContains(archived_response, 'Archived Post')
