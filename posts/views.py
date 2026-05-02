from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Status
 

class PostListView(ListView):
	template_name = "posts/list.html"
	model = Post
	context_object_name = "posts"

	def get_queryset(self):
		queryset = super().get_queryset()
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


def combined_post_list_detail(request):
	posts = Post.objects.all()
	post = None
	post_id = request.GET.get('post_id')
	if post_id:
		post = get_object_or_404(Post, pk=post_id)
	return render(request, 'posts/combined_list_detail.html', {'posts': posts, 'post': post})


class PostDetailView(DetailView):
	template_name = "posts/detail.html"
	model = Post
	context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
	template_name = "posts/new.html"
	model = Post
	fields = ["title", "subtitle", "body", "status"]

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})

class PostUpdateView(LoginRequiredMixin, UpdateView):
	template_name = "posts/edit.html"
	model = Post
	fields = ["title", "subtitle", "body", "status"]

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
