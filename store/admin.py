from django.contrib import admin
from .models import Category, Product, ProductImage, Color, Comment


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'approved', 'date')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Comment, CommentAdmin)
