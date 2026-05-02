from django.urls import path, include
from .views import SignUpView, profile_edit, public_profile

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/<str:username>/', public_profile, name='public_profile'),
    path('', include('django.contrib.auth.urls')),
    path('', include('allauth.urls')),
]
