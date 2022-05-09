from .models import Address, Config, Order
from django.contrib import admin

# Register your models here.

admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Config)
