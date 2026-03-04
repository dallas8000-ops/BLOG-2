from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('posts/', include('posts.urls')),
    # Django built-in auth URLs for password reset/change
    path('accounts/', include('django.contrib.auth.urls')),
]
