from django.contrib import admin
from app1.models import product,cart,CartItem,Category
# Register your models here.
admin.site.register(product)
admin.site.register(cart)
admin.site.register(CartItem)
admin.site.register(Category)