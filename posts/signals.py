from notifications.utils import send_notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def notify_on_new_post(sender, instance, created, **kwargs):
    if created:
        # Notify all users except the author (example)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        for user in User.objects.exclude(id=instance.author.id):
            send_notification(user.id, {
                'message': f'New post: {instance.title} by {instance.author.username}',
                'post_id': instance.id,
            })
