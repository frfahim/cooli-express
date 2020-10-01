from django.http import request
from rest_framework.permissions import AllowAny, IsAuthenticated
from cooli_express.orders.models import Order, PickupCoverageZone
from cooli_express.orders.serializers import OrderCreateSerializer, OrderDetailsSerializer, OrderListSerializer, ZoneSerializers
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ZonesListCreateAPIView(ListCreateAPIView):

    read_permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.user.is_anonymous and self.request.method == 'GET':
            return [permission() for permission in self.read_permission_classes]
        return [permission() for permission in self.permission_classes]

    serializer_class = ZoneSerializers
    queryset = PickupCoverageZone.objects.filter(is_available=True)

    def perform_create(self, serializer):
        serializer.save()


class OrderListCreateApiView(ListCreateAPIView):

    write_permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permission() for permission in self.write_permission_classes]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(
            requestor__user_id=self.request.user.id,
            is_available=True,
        ).order_by('-id')
        return queryset

    def perform_create(self, serializer):
        kwargs = {}
        user = None
        if self.request.user.is_authenticated:
            user = self.request.user
            kwargs['created_by_id'] = user.id
            customer = user.customer.last()
            if customer:
                kwargs['requestor_id'] = customer.id

        if not user:
            kwargs['is_individual'] = True
        # TODO add service charge calculation / validation
        serializer.save(**kwargs)


class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    serializer_class = OrderDetailsSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(
            requestor__user_id=self.request.user.id,
            is_available=True,
        )
        return queryset
