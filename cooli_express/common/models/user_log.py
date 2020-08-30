from django.db import models
from cooli_express.users.models import User
# from .base import Base, TimeLog

class UserLog(models.Model):
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


# class UserLogBase(Base, UserLog):

#     class Meta:
#         abstract = True


# class FullLogBase(Base, TimeLog, UserLog):

#     class Meta:
#         abstract = True

