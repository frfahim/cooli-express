import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cooli_express.users.models import User


class BaseModel(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("UUID"),
        help_text=_('Unique Identifier'),
    )
    is_available = models.BooleanField(
        default=False, help_text=_("if TRUE the record is available")
    )

    class Meta:
        abstract = True


class TimeLogBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserLogBase(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class FullLogBase(BaseModel, TimeLogBase, UserLogBase):

    class Meta:
        True
