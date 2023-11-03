from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Product

class ProductAdmin(admin.ModelAdmin):
    actions = ['custom_redirect_action']

    def custom_redirect_action(self, request, queryset):
        # Implement your custom action logic here.
        # For example, let's redirect to the "Add" page in the admin.
        url = reverse('product-list')
        return HttpResponseRedirect(url)

    custom_redirect_action.short_description = "Redirect to Other Page"

admin.site.register(Product, ProductAdmin)
