
from django.contrib import admin
from .models import Category, MenuItem, Cart, Order

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(Order)
