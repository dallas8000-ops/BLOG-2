from django.db import models
from django.contrib.auth.models import User


AVATAR_CHOICES = [
    ('avatars/boy.png', 'Boy'),
    ('avatars/black.png', 'Black'),
    ('avatars/older.png', 'Older'),
    ('avatars/woman.png', 'Woman'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=64, choices=AVATAR_CHOICES, default='avatars/A47.png')

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
