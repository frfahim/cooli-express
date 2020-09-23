from os import write
from cooli_express.users.api.serializers import UserDetailsSerializer
from rest_framework import serializers

from cooli_express.customers.models import Customer, PaymentInfo


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'uuid',
            'name',
            'phone',
            'pickup_phone',
            'email',
            'address',
            'pickup_address',
            'payment_method',
            'withdrawal',
            'user',
        ]


class CustomerInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'uuid',
            'name',
            'phone',
            'address',
            'website',
            'social_media',
        ]


class CustomerPickupPaymentSerializer(serializers.ModelSerializer):
    # zone = ZoneSerializers(read_only=True)

    class Meta:
        model = Customer
        fields = [
            'uuid',
            'pickup_address',
            'zone',
            'payment_method',
            'withdrawal',
        ]


class CompanyInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            'uuid',
            'name',
            'phone',
            'address',
            'website',
            'social_media',
        ]


class BankInfoSerializerClass(serializers.ModelSerializer):

    class Meta:
        model = PaymentInfo
        fields = (
            'payment_option',
            'phone_number',
            'bank_name',
            'branch',
            'routing_number',
            'account_type',
            'account_holder_name',
            'account_number',
        )


class MeCustomerSerializer(serializers.ModelSerializer):
    from cooli_express.orders.serializers import ZoneSerializers
    user = UserDetailsSerializer()
    payment = BankInfoSerializerClass(many=True)
    zone = ZoneSerializers()

    class Meta:
        model = Customer
        fields = [
            'uuid',
            'name',
            'phone',
            'pickup_phone',
            'email',
            'address',
            'pickup_address',
            'payment_method',
            'withdrawal',
            'user',
            'website',
            'social_media',
            'payment',
            'zone',
        ]
