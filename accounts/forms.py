
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, AVATAR_CHOICES


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ChoiceField(choices=AVATAR_CHOICES, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "avatar")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit)
        avatar = self.cleaned_data.get('avatar')
        profile, created = Profile.objects.get_or_create(user=user)
        if avatar:
            profile.avatar = avatar
        profile.save()
        return user
