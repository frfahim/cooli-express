from cooli_express.orders.config import OrderStatus, ProductTypes
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from model_utils import FieldTracker
from django_currentuser.db.models import CurrentUserField
from cooli_express.common.models.user_log import UserLog

from cooli_express.common.models.base import NameBase, TimeLogBase


User = get_user_model()
# class ProductType(NameBase):

#     def __str__(self) -> str:
#         return f"{self.pk} - {self.name}"


class PickupCoverageDistrict(NameBase):

    class Meta:
        verbose_name = "Pickup District"
        verbose_name_plural = "Pickup Districts"

    def __str__(self) -> str:
        return f"{self.name}"


class PickupCoverageZone(NameBase):
    # coverage upozilla/area
    district = models.ForeignKey(
        PickupCoverageDistrict,
        related_name="zones",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Pickup Zone"
        verbose_name_plural = "Pickup Zones"

    def __str__(self) -> str:
        return f"{self.name}"


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
    service_name = models.CharField(
        max_length=255,
        verbose_name=_("Service Name"),
        blank=True,
    )
    product_weight = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=Decimal("1.00"),
        verbose_name=_("Product Weight"),
    )
    service_charge = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        default=Decimal("0.00"),
        verbose_name=_("Service Charge"),
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
        verbose_name=_("Cash Collection Amount"),
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
    is_individual = models.BooleanField(
        default=False,
        verbose_name='Is individual Order'
    )
    pickedup_by = models.ForeignKey(
        User,
        related_name='orders_pickedup_by',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    pickedup_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Picked up time"),
    )
    deliverd_by = models.ForeignKey(
        User,
        related_name='orders_deliverd_by',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Delivered time"),
    )
    field_tracker = FieldTracker()

    # def individual_order(self):
    #     return 'YES' if self.is_available else 'NO'


    def __str__(self) -> str:
        return f"{self.pk} - Requestor: {self.requestor_name},  Reciever: {self.receiver_name}"


class OrderTracker(TimeLogBase):
    created_by = CurrentUserField()
    status = models.CharField(
        max_length=80,
        choices=OrderStatus.choices,
    )
    pre_status = models.CharField(
        max_length=80,
        choices=OrderStatus.choices,
        verbose_name=_("Previous Status"),
    )
    assigned = models.ForeignKey(
        User,
        related_name="tracker",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    order = models.ForeignKey(
        Order,
        related_name="tracker",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.pk}"
