from rest_framework import serializers
from posts.models import Post
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'subtitle', 'body', 'tags', 'status', 'author', 'created_on']
        read_only_fields = ['id', 'created_on']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
