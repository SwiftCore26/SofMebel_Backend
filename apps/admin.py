from django.contrib import admin
from django.contrib.admin import TabularInline, ModelAdmin

from apps.models import ProductImage, Product, Category, Contact, TelegramGroup


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 3
    min_num = 1
    validate_min = True


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'name')
    ordering = ('id',)
    readonly_fields = ('id', 'slug',)
    inlines = (ProductImageInline,)
    list_display_links = ('id', 'name')


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    ordering = ('id',)
    readonly_fields = ('id', 'slug',)
    list_display_links = ('id', 'name')


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('name', 'surname', 'email', 'created_at')
    search_fields = ('name', 'email', 'surname')
    ordering = ('id',)

@admin.register(TelegramGroup)
class TelegramGroupAdmin(ModelAdmin):
    list_display = ('group_name', 'group_id')
    ordering = ('id',)


