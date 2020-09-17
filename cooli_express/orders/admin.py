from django.contrib import admin

from .models import Order, PickupCoverageDistrict, PickupCoverageZone

admin.site.register(Order)
admin.site.register(PickupCoverageDistrict)
admin.site.register(PickupCoverageZone)
