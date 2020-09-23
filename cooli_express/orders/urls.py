from django.urls import path
from .views import (
    OrderDetailAPIView, ZonesListCreateAPIView,
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
        "<uuid:uuid>/",
        OrderDetailAPIView.as_view(),
        name="order-details"
    ),
    path(
        "zones/",
        ZonesListCreateAPIView.as_view(),
        name="zone-list-create"
    ),
]
