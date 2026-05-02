
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ProfileEditForm
from posts.models import Post


class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            form.save()
            return redirect('profile_edit')
    else:
        form = ProfileEditForm(instance=profile, user=request.user)
    return render(request, 'registration/profile_edit.html', {'form': form})


def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user, status__name__iexact='published').order_by('-created_on')
    return render(request, 'registration/public_profile.html', {'profile_user': user, 'posts': posts})
