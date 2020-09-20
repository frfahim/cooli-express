from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


def get_uniquie_username(id):
    return f"{settings.USERNAME_PREFEX}{id:05d}"


@receiver(post_save, sender=User)
def update_user(sender, instance, created, **kwargs):
    if created:
        instance.username = get_uniquie_username(instance.id)
        instance.save(update_fields=['username'])
