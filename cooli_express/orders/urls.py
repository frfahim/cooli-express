from django.urls import path
from .views import (
    ZonesListCreateAPIView,
    OrderListCreateApiView
)


app_name = "customers"

urlpatterns = [
    path(
        "",
        OrderListCreateApiView.as_view(),
        name="order-list-create"
    ),
    path(
        "zones/",
        ZonesListCreateAPIView.as_view(),
        name="zone-list-create"
    ),
]
