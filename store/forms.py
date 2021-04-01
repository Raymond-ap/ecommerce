import django_filters
from .models import *
from django import forms


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ('title',)

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                    'widget': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search product'})
                },
            },

        }


class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = '__all__'
