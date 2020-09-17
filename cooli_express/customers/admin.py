from django.contrib import admin

from .models import Customer, PaymentInfo


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')

admin.site.register(Customer, CustomerAdmin)


class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'payment_option')

admin.site.register(PaymentInfo, PaymentInfoAdmin)
