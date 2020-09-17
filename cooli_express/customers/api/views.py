from cooli_express.common.helpers import get_object_or_none
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import UpdateModelMixin
from cooli_express.users.api.serializers import UserDetailsSerializer

from cooli_express.customers.models import Customer, PaymentInfo
from .serializers import (
    CompanyInfoSerializer, CustomerInfoSerializer, CustomerPickupPaymentSerializer,
    CustomerSerializer,
    MeCustomerSerializer,
    BankInfoSerializerClass,
)


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    lookup_field = 'uuid'

    @action(detail=False, methods=['put'])
    def company_info(self, request, uuid=None):
        customer = self.get_object()
        serializer = CompanyInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeCustomerAPIView(RetrieveAPIView):
    serializer_class = MeCustomerSerializer

    def get_object(self):
        filter_kwargs = {'user_id': self.request.user.id}
        obj = get_object_or_none(Customer, **filter_kwargs)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            serializer = UserDetailsSerializer(request.user)
        else:
            serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MeCustomerDetailsAPIView(MeCustomerAPIView):
    serializer_class = MeCustomerSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CustomerAPIView(ListAPIView):
    serializer_class = CustomerSerializer


class CustomerBaseCreateUpdateAPIView(CreateAPIView, UpdateModelMixin):
    serializer_class = CustomerSerializer

    def get_object(self):
        filter_kwargs = {
            'user_id': self.request.user.id
        }
        obj = get_object_or_none(Customer, **filter_kwargs)
        return obj

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomerBaseUpdateAPIView(RetrieveUpdateAPIView):

    serializer_class = CustomerSerializer

    def get_object(self):
        return self.request.user.customer.last()



class CustomerInfoAPIView(CustomerBaseUpdateAPIView):
    serializer_class = CustomerInfoSerializer


class CustomerPickupPaymentApiView(CustomerBaseUpdateAPIView):
    serializer_class = CustomerPickupPaymentSerializer


class BankInfoAPIView(RetrieveUpdateAPIView):
    serializer_class = BankInfoSerializerClass
    # to get payment object set payment option
    payment_option = None

    def get_object(self):
        # get default bank data
        if not self.payment_option:
            self.payment_option = self.request.query_params.get('payment_option', 'bank')

        filter_kwargs = {
            'customer__user_id': self.request.user.id,
            'payment_option': self.payment_option
        }
        obj = get_object_or_none(PaymentInfo, **filter_kwargs)
        return obj

    def put(self, request, *args, **kwargs):
        self.payment_option = request.data['payment_option']
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user.customer.last())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
