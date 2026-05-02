from rest_framework import routers
from .views import PostViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
