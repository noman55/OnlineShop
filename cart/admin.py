from django.contrib import admin

# Register your models here.
from .models import OrderItem, Order
admin.site.register(OrderItem)
admin.site.register(Order)