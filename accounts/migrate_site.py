from django.contrib.sites.models import Site

# Set default site domain and name for allauth
Site.objects.update_or_create(
    id=1,
    defaults={
        'domain': 'localhost:8000',
        'name': 'localhost',
    }
)
