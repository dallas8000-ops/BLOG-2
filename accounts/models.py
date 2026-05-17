from django.db import models
from django.contrib.auth.models import User


AVATAR_CHOICES = [
    ('images/avatar-default.svg', 'Default'),
    ('images/avatar-alt.svg', 'Amber'),
    ('images/avatar-dark.svg', 'Green'),
    ('images/avatar-accent.svg', 'Accent'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=64, default='images/avatar-default.svg')
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('author', 'Author'),
        ('reader', 'Reader'),
    ]
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='reader')

    def __str__(self):
        return f"{self.user.username} Profile"


# Signals to create or update Profile automatically
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
