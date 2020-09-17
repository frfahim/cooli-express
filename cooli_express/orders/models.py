from cooli_express.orders.config import OrderStatus, ProductTypes
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from cooli_express.common.models.user_log import UserLog

from cooli_express.common.models.base import NameBase, TimeLogBase


# class ProductType(NameBase):

#     def __str__(self) -> str:
#         return f"{self.pk} - {self.name}"


class PickupCoverageDistrict(NameBase):

    def __str__(self) -> str:
        return f"{self.pk} - {self.name}"


class PickupCoverageZone(NameBase):
    # coverage upozilla/area
    district = models.ForeignKey(
        PickupCoverageDistrict,
        related_name="zones",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.pk} - {self.name}"


class Order(TimeLogBase, UserLog):
    requestor = models.ForeignKey(
        "customers.Customer",
        related_name='orders',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requestor_name = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Request Person name"),
    )
    requestor_phone = models.CharField(
        max_length=15,
        blank=True,
        help_text=_('Request Person Phone')
    )
    requestor_zone = models.ForeignKey(
        PickupCoverageZone,
        related_name="order",
        on_delete=models.SET_NULL,
        null=True,
        help_text=_('Request Person pickup zone')
    )
    requestor_address = models.CharField(
        max_length=255,
        help_text=_('Request Person pickup address')
    )
    pickup_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Pickup date and time"),
    )
    product_type = models.CharField(
        max_length=120,
        choices=ProductTypes.choices
    )
    description = models.CharField(
        max_length=255,
        blank=True
    )
    invoice_number = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    invoice_value = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    cash_amount = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        default=Decimal("0.00"),
        verbose_name=_("Amount"),
        help_text=_("Cash Collection Amount"),
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        default=Decimal("0.00"),
        verbose_name=_("Amount"),
        help_text=_("Amount without delivery charge."),
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        default=Decimal("0.00"),
        verbose_name=_("Total Amount"),
        help_text=_("Amount with delivery charge."),
    )

    # ------------------ #
    # delivery info
    receiver_name = models.CharField(
        max_length=255,
        blank=True,
        help_text=_("Receiver name"),
    )
    receiver_phone = models.CharField(
        max_length=15,
        blank=True,
        help_text=_('Receiver Phone')
    )
    receiver_zone = models.ForeignKey(
        PickupCoverageZone,
        related_name="orders",
        on_delete=models.SET_NULL,
        null=True,
        help_text=_('Receiver Zone')
    )
    receiver_address = models.CharField(
        max_length=255,
        help_text=_('Receiver address')
    )
    delivery_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Delivery date and time"),
    )
    delivery_note = models.CharField(
        max_length=255,
        blank=True
    )

    # ------------------ #
    reference = models.CharField(
        max_length = 20,
        editable=False,
        unique=True,
        help_text=_('Unique order number'),
        verbose_name=_('Order Reference')
    )
    status = models.CharField(
        max_length=80,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    is_individual = models.BooleanField(default=False)
    pickedup_by = models.ForeignKey(
        "customers.Customer",
        related_name='orders_pickedup_by',
        on_delete=models.SET_NULL,
        null=True
    )
    pickedup_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Picked up time"),
    )
    deliverd_by = models.ForeignKey(
        "customers.Customer",
        related_name='orders_deliverd_by',
        on_delete=models.SET_NULL,
        null=True
    )
    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Delivered time"),
    )

    def __str__(self) -> str:
        return f"{self.pk} - Requestor: {self.requestor_name},  Reciever: {self.receiver_name}"
