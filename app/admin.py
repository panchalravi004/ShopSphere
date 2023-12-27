from django.contrib import admin

from app.models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)