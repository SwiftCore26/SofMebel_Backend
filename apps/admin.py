from django.contrib import admin
from django.contrib.admin import TabularInline, ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.models import ProductImage, Product, Category, Contact, TelegramGroup, Footer, User


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 3
    min_num = 1
    validate_min = True


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = 'id', 'name', 'price', 'category'
    search_fields = 'name', 'category__name'
    list_filter = 'category', 'name'
    ordering = ('id',)
    readonly_fields = 'id', 'slug'
    inlines = (ProductImageInline,)
    list_display_links = 'id', 'name'


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = 'id', 'name', 'slug'
    search_fields = ('name',)
    ordering = ('id',)
    readonly_fields = 'id', 'slug'
    list_display_links = 'id', 'name'


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = 'name', 'surname', 'email', 'created_at'
    search_fields = 'name', 'email', 'surname'
    ordering = ('id',)


@admin.register(TelegramGroup)
class TelegramGroupAdmin(ModelAdmin):
    list_display = 'group_name', 'group_id'
    ordering = ('id',)


@admin.register(Footer)
class FooterAdmin(ModelAdmin):
    list_display = 'instagram_link', 'facebook_link', 'twitter_link', 'linkedin_link'
    ordering = ('id',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = 'id', 'username', 'email', 'is_staff', 'is_active', 'is_worker'
    list_filter = 'is_staff', 'is_active', 'is_worker'
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_worker', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_worker'),
        }),
    )
    search_fields = 'username', 'email'
    ordering = ('id',)
