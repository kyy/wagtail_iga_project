from django.contrib import admin

# Register your models here.
from wagtail.contrib.modeladmin.options import ModelAdmin

from products.models import ProductCategory

class ProductCategoryAdmin(admin.ModelAdmin):
    model = ProductCategory
    prepopulated_fields = {'slug': ['name']}


admin.site.register(ProductCategory,  ProductCategoryAdmin)