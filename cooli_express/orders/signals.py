import secrets
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


def get_uniquie_order_reference(id):
    return f"{settings.ORDER_PREFEX}{id}-{secrets.token_hex(4)}"


@receiver(post_save, sender=Order)
def update_order(sender, instance, created, **kwargs):
    if created:
        instance.reference = get_uniquie_order_reference(instance.id)
        instance.save(update_fields=['reference'])
