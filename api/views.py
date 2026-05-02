from rest_framework import viewsets
from posts.models import Post
from django.contrib.auth.models import User
from .serializers import PostSerializer, UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_fields = ['author', 'status']
    search_fields = ['title', 'subtitle', 'body']
    ordering_fields = ['created_on', 'title']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
