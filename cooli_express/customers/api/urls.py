from django.urls import path
from .views import (
    CustomerAPIView,
    CustomerInfoAPIView,
    CustomerPickupPaymentApiView,
    BankInfoAPIView,
    CustomerViewSet,
    MeCustomerAPIView,
    MeCustomerDetailsAPIView,
)


app_name = "customers"

urlpatterns = [
    path(
        "",
        CustomerAPIView.as_view(),
        name="customers"
    ),
    path(
        "info/",
        CustomerInfoAPIView.as_view(),
        name="customers-info"
    ),
    path(
        "pickup-payment/",
        CustomerPickupPaymentApiView.as_view(),
        name="customers-pickup-paymen"
    ),
    path(
        "bank/",
        BankInfoAPIView.as_view(),
        name="customer-payment"
    ),
    path(
        "me/",
        MeCustomerAPIView.as_view(),
        name="customers-me"
    ),
    path(
        "me/details/",
        MeCustomerDetailsAPIView.as_view(),
        name="customers-me-details"
    ),
    path(
        "viewset/",
        CustomerViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }),
        name="customers-viewset"
    ),
    path(
        "viewset/<uuid:uuid>/",
        CustomerViewSet.as_view({
            'patch': 'partial_update',
            'get': 'retrieve',
        }),
        name="customers-details"
    ),
]
