from django.contrib import admin
from django.http import request

from .models import Order, PickupCoverageDistrict, PickupCoverageZone


class OrderAdmin(admin.ModelAdmin):
    actions = None
    list_per_page = 20
    list_filter = ('status', 'is_individual')
    list_display = ('reference','status', 'requestor_name', 'total_amount', 'receiver_name', 'receiver_phone')
    add_fieldsets = (
        (None, {
            'fields': (
                'is_individual',
                # 'reference',
                'status',
                # 'pickedup_by',
                # 'pickedup_at',
                # 'deliverd_by',
                # 'delivered_at'
            )
        }),
        ('Requestor Info', {
            'classes': ('horizontal_tabs',),
            'fields': (
                'requestor',
                'requestor_name',
                'requestor_phone',
                'requestor_address',
                'pickup_date',
                'product_type',
                'description',
                'invoice_number',
                'invoice_value',
            ),
        }),
        ('Amounts', {
            'classes': ('horizontal_tabs',) ,
            'fields': (
                'cash_amount',
                'amount',
                'total_amount',
            )
        }),
        ('Receiver Info', {
            'classes': ('horizontal_tabs',),
            'fields': (
                'receiver_zone',
                'receiver_name',
                'receiver_phone',
                'receiver_address',
                'delivery_date',
                'delivery_note',

            )
        })
    )
    edit_fieldsets = (
        (None, {
            'fields': (
                'individual_order',
                'reference',
                'status',
                'pickedup_by',
                'pickedup_at',
                'deliverd_by',
                'delivered_at'
            )
        }),
        ('Requestor Info', {
            'classes': ('horizontal_tabs',),
            'fields': (
                'requestor_name',
                'requestor_phone',
                'requestor_zone_name',
                'requestor_address',
                'pickup_date',
                'product_type',
                'description',
                'invoice_number',
                'invoice_value',
            ),
        }),
        ('Amounts', {
            'classes': ('horizontal_tabs',) ,
            'fields': (
                'cash_amount',
                'amount',
                'total_amount',
            )
        }),
        ('Receiver Info', {
            'classes': ('horizontal_tabs',),
            'fields': (
                'receiver_name',
                'receiver_phone',
                'receiver_zone_name',
                'receiver_address',
                'delivery_date',
                'delivery_note',

            )
        })
    )
    # fields = ('reference', 'status', 'requestor_name', 'total_amount', 'receiver_name', 'receiver_phone')
    edit_readonly_fields = [
        'individual_order',
        'reference',
        'requestor',
        'requestor_name',
        'requestor_phone',
        'requestor_zone_name',
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

        'receiver_name',
        'receiver_phone',
        'receiver_zone_name',
        'receiver_address',
        'delivery_date',
        'delivery_note',
    ]

    search_fields = ['reference', 'requestor_phone', 'receiver_phone']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.edit_readonly_fields
        else:
            return ['reference']

    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.edit_fieldsets
        return self.add_fieldsets

    def requestor_zone_name(self, obj):
        return obj.requestor_zone.name

    def receiver_zone_name(self, obj):
        return obj.receiver_zone.name

    def individual_order(self, obj):
        # return 'YES' if obj.is_available else 'NO'
        if obj.is_individual:
            return 'YES'
        return 'NO'

    def has_delete_permission(self, request, obj=None):
        return None

    def has_add_permission(self, request):
        return False

admin.site.register(Order, OrderAdmin)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('is_available', )
    search_fields = ('name', )

admin.site.register(PickupCoverageDistrict, DistrictAdmin)
admin.site.register(PickupCoverageZone, DistrictAdmin)
