from rest_framework import viewsets, permissions
from posts.models import Post
from django.contrib.auth.models import User
from .serializers import PostSerializer, UserSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow read to anyone; write only to the post's author or staff."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_fields = ['author', 'status']
    search_fields = ['title', 'subtitle', 'body']
    ordering_fields = ['created_on', 'title']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [permissions.AllowAny()]
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only. Exposes id and username only — no email leakage."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
