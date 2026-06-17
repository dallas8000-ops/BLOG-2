from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health, name='health'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('resume/', views.resume, name='resume'),
    path('contact/', views.contact, name='contact'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]
