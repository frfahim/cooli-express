import secrets
from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, OrderTracker


def get_uniquie_order_reference(id):
    return f"{settings.ORDER_PREFEX}{id}-{secrets.token_hex(4)}"


@transaction.atomic
@receiver(post_save, sender=Order)
def update_order(sender, instance, created, **kwargs):
    if created:
        instance.reference = get_uniquie_order_reference(instance.id)
        instance.save(update_fields=['reference'])
    if not created and instance.field_tracker.has_changed('status'):
        assigned = None # request user
        if instance.deliverd_by and instance.field_tracker.has_changed('deliverd_by_id'):
            assigned = instance.deliverd_by
        elif instance.pickedup_by and instance.field_tracker.has_changed('pickedup_by_id'):
            assigned = instance.pickedup_by
        create_data = {
            'order_id': instance.id,
            'status': instance.status,
            'assigned': assigned,
        }
        if instance.field_tracker.changed()['status']:
            create_data['pre_status'] = instance.field_tracker.changed()['status'],

        OrderTracker.objects.create(**create_data)
