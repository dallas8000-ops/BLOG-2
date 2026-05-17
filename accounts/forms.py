
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, AVATAR_CHOICES


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'website', 'github']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ChoiceField(choices=AVATAR_CHOICES, required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    website = forms.URLField(required=False)
    github = forms.URLField(required=False)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "avatar", "bio", "website", "github", "role")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit)
        avatar = self.cleaned_data.get('avatar')
        bio = self.cleaned_data.get('bio')
        website = self.cleaned_data.get('website')
        github = self.cleaned_data.get('github')
        role = self.cleaned_data.get('role')
        profile, _ = Profile.objects.get_or_create(user=user)
        if avatar:
            profile.avatar = avatar
        if bio:
            profile.bio = bio
        if website:
            profile.website = website
        if github:
            profile.github = github
        if role:
            profile.role = role
        profile.save()
        return user
