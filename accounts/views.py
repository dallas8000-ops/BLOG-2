
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

    def form_invalid(self, form):
        print("DEBUG: Form is invalid")
        print(form.errors.as_json())
        return super().form_invalid(form)

    def form_valid(self, form):
        print("DEBUG: Form is valid")
        return super().form_valid(form)
