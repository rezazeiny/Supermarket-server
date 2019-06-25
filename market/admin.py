from django.contrib import admin

from .models import Market, Product, Role

admin.site.register(Market)
admin.site.register(Product)
admin.site.register(Role)
