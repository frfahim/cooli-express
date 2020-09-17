import uuid
from django.db.models import (
    Model,
    UUIDField,
    BooleanField,
    DateTimeField,
    Index,
    CharField,
)
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
        default=True, help_text=_("if False the record is not available")
    )

    class Meta:
        indexes = [Index(fields=["uuid"])]
        abstract = True


class TimeLog(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TimeLogBase(Base, TimeLog):

    class Meta:
        abstract = True


class NameBase(Base):
    name = CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
