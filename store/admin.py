from django.contrib import admin
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'email', 'approved', 'date')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'created')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'subject', 'viewed','created')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Comment, CommentAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Blog, BlogAdmin)