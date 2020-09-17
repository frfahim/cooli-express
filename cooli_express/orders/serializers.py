from django.db.models import fields
from rest_framework import serializers

from .models import Order, PickupCoverageZone


class ZoneSerializers(serializers.ModelSerializer):

    class Meta:
        model = PickupCoverageZone
        fields = (
            'id',
            'name',
            'district',
        )


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            'requestor_name',
            'requestor_phone',
            'requestor_zone',
            'requestor_address',
            'pickup_date',
            'product_type',
            'description',
            'invoice_number',
            'invoice_value',
            'cash_amount',
            'amount',
            'total_amount',
            'receiver_name',
            'receiver_phone',
            'receiver_zone',
            'receiver_address',
            'delivery_date',
            'delivery_note',
        )


class OrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            'reference',
            'status',
            'requestor_name',
            'requestor_phone',
            'pickup_date',
            'product_type',
            # 'invoice_number',
            # 'invoice_value',
            'cash_amount',
            'amount',
            'total_amount',
            'receiver_name',
            'receiver_phone',
            # 'receiver_zone',
            'receiver_address',
            # 'delivery_date',
            # 'delivery_note',
        )
