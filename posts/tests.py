from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Comment, Post, Status


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


class TagsTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='barney', password=TEST_CREDENTIAL)
		self.status, _ = Status.objects.get_or_create(name='published', defaults={'description': 'Published'})
		self.post = Post.objects.create(
			title='Tagged Post',
			subtitle='sub',
			body='body',
			author=self.user,
			status=self.status,
			tags='django, python, testing',
		)

	def test_get_tags_returns_list(self):
		self.assertEqual(self.post.get_tags(), ['django', 'python', 'testing'])

	def test_tags_shown_on_detail_page(self):
		response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
		self.assertContains(response, 'django')
		self.assertContains(response, 'python')

	def test_empty_tags_returns_empty_list(self):
		self.post.tags = ''
		self.post.save()
		self.assertEqual(self.post.get_tags(), [])


class StatusToggleTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='barney', password=TEST_CREDENTIAL)
		self.other = User.objects.create_user(username='other', password=TEST_CREDENTIAL)
		self.pub, _ = Status.objects.get_or_create(name='published', defaults={'description': 'Published'})
		self.draft, _ = Status.objects.get_or_create(name='draft', defaults={'description': 'Draft'})
		self.post = Post.objects.create(
			title='Toggle Post', subtitle='sub', body='body', author=self.user, status=self.pub
		)

	def test_author_can_unpublish(self):
		self.client.login(username='barney', password=TEST_CREDENTIAL)
		self.client.get(reverse('toggle_post_status', kwargs={'pk': self.post.pk}))
		self.post.refresh_from_db()
		self.assertEqual(self.post.status.name, 'draft')

	def test_author_can_publish(self):
		self.post.status = self.draft
		self.post.save()
		self.client.login(username='barney', password=TEST_CREDENTIAL)
		self.client.get(reverse('toggle_post_status', kwargs={'pk': self.post.pk}))
		self.post.refresh_from_db()
		self.assertEqual(self.post.status.name, 'published')

	def test_non_author_cannot_toggle(self):
		self.client.login(username='other', password=TEST_CREDENTIAL)
		response = self.client.get(reverse('toggle_post_status', kwargs={'pk': self.post.pk}))
		self.assertEqual(response.status_code, 404)

	def test_unauthenticated_toggle_redirects(self):
		response = self.client.get(reverse('toggle_post_status', kwargs={'pk': self.post.pk}))
		self.assertEqual(response.status_code, 302)


class CommentTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='barney', password=TEST_CREDENTIAL)
		self.status, _ = Status.objects.get_or_create(name='published', defaults={'description': 'Published'})
		self.post = Post.objects.create(
			title='Comment Post', subtitle='sub', body='body', author=self.user, status=self.status
		)

	def test_logged_in_user_can_comment(self):
		self.client.login(username='barney', password=TEST_CREDENTIAL)
		self.client.post(reverse('add_comment', kwargs={'pk': self.post.pk}), {'body': 'Great post!'})
		self.assertEqual(Comment.objects.filter(post=self.post).count(), 1)
		self.assertEqual(Comment.objects.get(post=self.post).body, 'Great post!')

	def test_empty_comment_not_saved(self):
		self.client.login(username='barney', password=TEST_CREDENTIAL)
		self.client.post(reverse('add_comment', kwargs={'pk': self.post.pk}), {'body': '   '})
		self.assertEqual(Comment.objects.filter(post=self.post).count(), 0)

	def test_unauthenticated_comment_redirects(self):
		response = self.client.post(reverse('add_comment', kwargs={'pk': self.post.pk}), {'body': 'Hi'})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Comment.objects.filter(post=self.post).count(), 0)

	def test_comments_shown_on_detail_page(self):
		Comment.objects.create(post=self.post, author=self.user, body='Nice article!')
		response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
		self.assertContains(response, 'Nice article!')


class NonStaffVisibilityTests(TestCase):
	def setUp(self):
		self.author = User.objects.create_user(username='barney', password=TEST_CREDENTIAL)
		self.reader = User.objects.create_user(username='reader', password=TEST_CREDENTIAL)
		self.pub, _ = Status.objects.get_or_create(name='published', defaults={'description': 'Published'})
		self.draft, _ = Status.objects.get_or_create(name='draft', defaults={'description': 'Draft'})
		self.pub_post = Post.objects.create(
			title='Public Post', subtitle='sub', body='body', author=self.author, status=self.pub
		)
		self.draft_post = Post.objects.create(
			title='Draft Post', subtitle='sub', body='body', author=self.author, status=self.draft
		)

	def test_anonymous_sees_only_published(self):
		response = self.client.get(reverse('post_list'))
		self.assertContains(response, 'Public Post')
		self.assertNotContains(response, 'Draft Post')

	def test_logged_in_non_staff_sees_only_published(self):
		self.client.login(username='reader', password=TEST_CREDENTIAL)
		response = self.client.get(reverse('post_list'))
		self.assertContains(response, 'Public Post')
		self.assertNotContains(response, 'Draft Post')

	def test_staff_sees_all_posts(self):
		self.author.is_staff = True
		self.author.save()
		self.client.login(username='barney', password=TEST_CREDENTIAL)
		response = self.client.get(reverse('post_list'))
		self.assertContains(response, 'Public Post')
		self.assertContains(response, 'Draft Post')


class PostSearchTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='barney', password=TEST_CREDENTIAL)
		self.pub, _ = Status.objects.get_or_create(name='published', defaults={'description': 'Published'})
		Post.objects.create(
			title='Django Tips',
			subtitle='sub',
			body='A post about Django views.',
			author=self.user,
			status=self.pub,
		)
		Post.objects.create(
			title='React Hooks',
			subtitle='sub',
			body='A post about useState and useEffect.',
			author=self.user,
			status=self.pub,
		)

	def test_search_returns_matching_post(self):
		response = self.client.get(reverse('post_list'), {'search': 'Django'})

		self.assertContains(response, 'Django Tips')
		self.assertNotContains(response, 'React Hooks')

	def test_search_matches_body_text(self):
		response = self.client.get(reverse('post_list'), {'search': 'useState'})

		self.assertContains(response, 'React Hooks')
		self.assertNotContains(response, 'Django Tips')

	def test_search_no_results_returns_empty(self):
		response = self.client.get(reverse('post_list'), {'search': 'nonexistent_xyz'})

		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, 'Django Tips')
		self.assertNotContains(response, 'React Hooks')


class PostAPITests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(username='barney', password=TEST_CREDENTIAL)
		self.pub, _ = Status.objects.get_or_create(name='published', defaults={'description': 'Published'})
		self.post = Post.objects.create(
			title='API Test Post',
			subtitle='sub',
			body='body text',
			author=self.user,
			status=self.pub,
		)

	def test_api_post_list_is_public(self):
		response = self.client.get('/api/posts/')

		self.assertEqual(response.status_code, 200)

	def test_api_post_detail_is_public(self):
		response = self.client.get(f'/api/posts/{self.post.pk}/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['title'], 'API Test Post')

	def test_api_create_requires_authentication(self):
		response = self.client.post('/api/posts/', {'title': 'New', 'subtitle': 'sub', 'body': 'b'})

		self.assertEqual(response.status_code, 401)

	def test_api_authenticated_user_can_create_post(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.post('/api/posts/', {
			'title': 'Auth Post',
			'subtitle': 'sub',
			'body': 'body',
			'author': self.user.pk,
			'status': self.pub.pk,
		})

		self.assertEqual(response.status_code, 201)
		self.assertTrue(Post.objects.filter(title='Auth Post').exists())

	def test_api_user_cannot_edit_others_post(self):
		other = User.objects.create_user(username='other', password=TEST_CREDENTIAL)
		self.client.force_authenticate(user=other)
		response = self.client.patch(f'/api/posts/{self.post.pk}/', {'title': 'Stolen'})

		self.assertEqual(response.status_code, 403)

	def test_api_author_can_edit_own_post(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.patch(f'/api/posts/{self.post.pk}/', {'title': 'Updated via API'})

		self.assertEqual(response.status_code, 200)
		self.post.refresh_from_db()
		self.assertEqual(self.post.title, 'Updated via API')

	def test_api_users_endpoint_requires_auth(self):
		response = self.client.get('/api/users/')

		self.assertEqual(response.status_code, 401)

	def test_api_users_endpoint_accessible_when_authenticated(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.get('/api/users/')

		self.assertEqual(response.status_code, 200)
