from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Ray Gilliom'
        context['description'] = (
            'Hello, my name is Ray Gilliom. I am a passionate developer and lifelong learner, '
            'excited to build and explore new technologies. Welcome to my About page!'
        )
        return context
