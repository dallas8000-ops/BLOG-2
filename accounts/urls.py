from django.urls import path, include
from .views import SignUpView, profile_edit

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('', include('django.contrib.auth.urls')),
    path('', include('allauth.urls')),
]
