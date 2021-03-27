import django_filters
from .models import Product
from django import forms


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['title']