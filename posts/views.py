from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Post, Status
from .models import Post

class PostListView(ListView):
	model = Post
	template_name = 'posts/list.html'
	context_object_name = 'posts'

class PostDetailView(DetailView):
	model = Post
	template_name = 'posts/post_detail.html'
	context_object_name = 'post'

class PostUpdateView(LoginRequiredMixin, UpdateView):
	template_name = "posts/edit.html"
	model = Post
	fields = ["title", "subtitle", "body"]

	def get_queryset(self):
		# Only allow the author to update their own posts
		return Post.objects.filter(author=self.request.user)

class PostDeleteView(LoginRequiredMixin, DeleteView):
	template_name = "posts/delete.html"
	model = Post

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
class PostCreateView(CreateView):
	template_name = "posts/new.html"
	model = Post
	fields = ["title", "subtitle", "body"]

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

def post_list(request):
	posts = Post.objects.all()
	return render(request, 'posts/list.html', {'posts': posts})
