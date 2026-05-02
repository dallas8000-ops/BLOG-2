from django.db.models import Q
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Post, Status, Comment


class PostListView(ListView):
	template_name = "posts/list.html"
	model = Post
	context_object_name = "posts"
	ordering = ["-created_on"]
	paginate_by = 6

	def get_queryset(self):
		queryset = super().get_queryset().select_related("author", "status")
		# Non-staff only see published posts
		if not (self.request.user.is_authenticated and self.request.user.is_staff):
			queryset = queryset.filter(status__name__iexact='published')
		search = self.request.GET.get('search', '')
		status = self.request.GET.get('status', '')
		author = self.request.GET.get('author', '')
		if search:
			queryset = queryset.filter(
				Q(title__icontains=search) |
				Q(subtitle__icontains=search) |
				Q(body__icontains=search)
			)
		if status:
			queryset = queryset.filter(status__name__iexact=status)
		if author:
			queryset = queryset.filter(author__username__iexact=author)
		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search'] = self.request.GET.get('search', '')
		context['status'] = self.request.GET.get('status', '')
		context['author'] = self.request.GET.get('author', '')
		return context


class PostDetailView(DetailView):
	template_name = "posts/detail.html"
	model = Post
	context_object_name = "post"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['comments'] = self.object.comments.select_related('author').order_by('created_on')
		return context


class PostCreateView(LoginRequiredMixin, CreateView):
	template_name = "posts/new.html"
	model = Post
	fields = ["title", "subtitle", "body", "tags", "status"]

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})

class PostUpdateView(LoginRequiredMixin, UpdateView):
	template_name = "posts/edit.html"
	model = Post
	fields = ["title", "subtitle", "body", "tags", "status"]

	def get_queryset(self):
		return Post.objects.filter(author=self.request.user)

	def get_success_url(self):
		return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})

class PostDeleteView(LoginRequiredMixin, DeleteView):
	template_name = "posts/delete.html"
	model = Post
	context_object_name = "post"
	success_url = reverse_lazy("post_list")

	def get_queryset(self):
		# Only allow the author to delete their own posts
		return Post.objects.filter(author=self.request.user)

class PostDraftListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'posts/post_draft_list.html'
	context_object_name = 'posts'
	def get_queryset(self):
		return Post.objects.filter(status__name='draft', author=self.request.user)

class PostArchivedListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'posts/post_archived_list.html'
	context_object_name = 'posts'
	def get_queryset(self):
		return Post.objects.filter(status__name='archived', author=self.request.user)


@login_required
def toggle_post_status(request, pk):
	post = get_object_or_404(Post, pk=pk, author=request.user)
	if post.status and post.status.name.lower() == 'published':
		draft_status, _ = Status.objects.get_or_create(name='draft', defaults={'description': 'Draft post'})
		post.status = draft_status
	else:
		pub_status, _ = Status.objects.get_or_create(name='published', defaults={'description': 'Published post'})
		post.status = pub_status
	post.save()
	return redirect('post_detail', pk=pk)


@login_required
def add_comment(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		body = request.POST.get('body', '').strip()
		if body:
			Comment.objects.create(post=post, author=request.user, body=body)
	return redirect('post_detail', pk=pk)
