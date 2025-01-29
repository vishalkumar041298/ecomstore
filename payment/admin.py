from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'address1')

admin.site.register(Order)
admin.site.register(OrderItem)
