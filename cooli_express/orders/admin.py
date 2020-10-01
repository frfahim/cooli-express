from django.contrib import admin
from django.http import request

from .models import (
    Order,
    OrderTracker,
    PickupCoverageDistrict,
    PickupCoverageZone,
)


class OrderTrackerInline(admin.TabularInline):
    model = OrderTracker
    verbose_name = 'Order Status'
    verbose_name_plural = 'Orders Status'
    extra = 1
    fields = ['status', 'assigned', 'changed_by']
    readonly_fields = ['changed_by']
    autocomplete_fields = ['assigned']

    def changed_by(self, obj):
        return obj.created_by.name

    # def has_add_permission(self, request, obj=None):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override the formset function in order to remove the add and change buttons beside the foreign key pull-down
        menus in the inline.
        """
        formset = super(OrderTrackerInline, self).get_formset(request, obj, **kwargs)
        form = formset.form
        widget = form.base_fields['assigned'].widget
        widget.can_add_related = False
        widget.can_change_related = False
        widget.can_delete_related = False
        return formset


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
                'service_name',
                'product_weight',
                'service_charge',
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
        'service_name',
        'product_weight',
        'service_charge',
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

    inlines = [
        OrderTrackerInline,
    ]
    view_on_site = False
    autocomplete_fields = ['pickedup_by', 'deliverd_by']

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
