from django.contrib import admin
from .models import Commodity, Category, Market, AcceptedPaymentMethod


admin.site.register(Market)
admin.site.register(Commodity)
admin.site.register(Category)
admin.site.register(AcceptedPaymentMethod)
