from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from cooli_express.common.models.base import Base
from cooli_express.users.managers import CustomUserManager


class User(AbstractUser, Base):
    """Default user for Cooli Express.
    """

    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    # username = None
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        help_text=_('Phone number')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} - {self.name}"

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"uuid": self.uuid})
