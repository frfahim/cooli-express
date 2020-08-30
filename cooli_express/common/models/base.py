import uuid
from django.db.models import Model, UUIDField, BooleanField, DateTimeField
from django.utils.translation import gettext_lazy as _


class Base(Model):
    uuid = UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("UUID"),
        help_text=_('Unique Identifier'),
    )
    is_available = BooleanField(
        default=False, help_text=_("if TRUE the record is available")
    )

    class Meta:
        abstract = True


class TimeLog(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimeLogBase(Base, TimeLog):

    class Meta:
        abstract = True



