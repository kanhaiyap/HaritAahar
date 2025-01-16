from django.contrib import admin

# Register your models here.
from .models import Product,CustomUser,Order,Payment
from .models import Orders

admin.site.register(Orders)

admin.site.register(Product)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(Payment)