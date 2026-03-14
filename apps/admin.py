from django.contrib import admin
from django.contrib.admin import TabularInline

from apps.models import ProductImage, Product


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'name')
    ordering = ('id',)
    inlines = (ProductImageInline,)
