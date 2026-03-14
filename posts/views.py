from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Status
from .models import Post

class PostListView(ListView):
	template_name = "posts/list.html"
	model = Post
	context_object_name = "posts"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


from django.shortcuts import get_object_or_404

def combined_post_list_detail(request):
	posts = Post.objects.all()
	post = None
	post_id = request.GET.get('post_id')
	if post_id:
		post = get_object_or_404(Post, pk=post_id)
	return render(request, 'posts/combined_list_detail.html', {'posts': posts, 'post': post})

class PostUpdateView(LoginRequiredMixin, UpdateView):
	template_name = "posts/edit.html"
	model = Post
	fields = ["title", "subtitle", "body", "status"]
	success_url = reverse_lazy("post_list")

	def get_queryset(self):
		# Allow all logged-in users to edit any post
		return Post.objects.all()

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
from django.contrib.auth.mixins import LoginRequiredMixin


def post_list(request):
	posts = Post.objects.all()
	return render(request, 'posts/list.html', {'posts': posts})
