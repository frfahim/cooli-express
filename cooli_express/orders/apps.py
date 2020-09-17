from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class OrdersConfig(AppConfig):
    name = 'cooli_express.orders'
    verbose_name = _("Orders")

    def ready(self):
        # super(OrdersConfig, self).ready()
        from . import signals
