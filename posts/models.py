from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class Status(models.Model):
	name = models.CharField(max_length=128, unique=True)
	description = models.CharField(max_length=256, help_text="Write a description about the status")

	def __str__(self):
		return f"{self.name}"

class Post(models.Model):
	title = models.CharField(max_length=128)
	subtitle = models.CharField(max_length=256)
	body = models.TextField()
	tags = models.CharField(max_length=256, blank=True, help_text="Comma-separated tags, e.g. python,django,qa")
	created_on = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(
		get_user_model(),
		on_delete=models.CASCADE
	)
	status = models.ForeignKey(
		Status,
		on_delete=models.DO_NOTHING,
		null=True,
		blank=True,
		related_name='posts'
	)

	def get_tags(self):
		return [t.strip() for t in self.tags.split(',') if t.strip()]

	def __str__(self):
		return f"{self.title} by {self.author}"


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	body = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Comment by {self.author} on {self.post}"

# Create your models here.
