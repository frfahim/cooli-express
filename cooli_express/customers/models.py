import re
from cooli_express.orders.models import PickupCoverageZone
from django.db import models
from django.utils.translation import gettext_lazy as _

from cooli_express.common.models.base import TimeLogBase
from cooli_express.customers.config import PaymentOption, WithdrawalOptions
from cooli_express.users.models import User


class Customer(TimeLogBase):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer',
    )
    name = models.CharField(
        max_length=255,
        help_text=_("Business name"),
    )
    phone = models.CharField(
        max_length=15,
        help_text=_('Business Phone number')
    )
    pickup_phone = models.CharField(
        max_length=15,
        blank=True,
        help_text=_('Pickup Phone number')
    )
    email = models.EmailField(
        blank=True,
        help_text=_('Business email address'),
    )
    address = models.CharField(
        max_length=255,
        help_text=_('Business address')
    )
    zone = models.ForeignKey(
        PickupCoverageZone,
        related_name="customer",
        on_delete=models.SET_NULL,
        null=True,
    )
    pickup_address = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Pickup address')
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PaymentOption.CHOICES,
    )
    withdrawal = models.CharField(
        max_length=50,
        choices=WithdrawalOptions.CHOICES,
        default=WithdrawalOptions.WEEKLY,
    )
    website = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Business website address')
    )
    social_media = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Business social media')
    )
    referral_number = models.CharField(
        max_length=15,
        blank=True,
    )
    verification_number = models.CharField(
        max_length=15,
        blank=True,
        help_text=_("NID, Passport or Trade License.")
    )

    def __str__(self):
        return f"{self.pk}: {self.name}"


class PaymentInfo(TimeLogBase):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="payment",
    )
    payment_option = models.CharField(
        max_length=50,
        choices=PaymentOption.CHOICES,
        default=PaymentOption.CASH,
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        help_text=_('Mobile account number')
    )
    bank_name = models.CharField(
        max_length=60,
        blank=True,
    )
    branch = models.CharField(
        max_length=50,
        blank=True,
    )
    routing_number = models.CharField(
        max_length=20,
        blank=True,
    )
    account_type = models.CharField(
        max_length=15,
        blank=True,
    )
    account_holder_name = models.CharField(
        max_length=160,
        blank=True,
    )
    account_number = models.CharField(
        max_length=100,
        blank=True,
    )

    def __str__(self):
        return f"{self.pk}: {self.customer.name} - {self.payment_option}"

    class Meta:
        indexes = [
            models.Index(fields=['payment_option'])
        ]
