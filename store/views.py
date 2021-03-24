from django.shortcuts import render
from .models import Product, Category


def homePage(request):
    featured = Product.objects.filter(published=True).order_by('created')[:4]
    new_arrival = Product.objects.filter(
        published=True).order_by('-created')[:8]

    context = {
        'featured': featured,
        'new_arrival': new_arrival
    }
    return render(request, 'store/index.html', context)


def productsView(request):
    products = Product.objects.filter(published=True).order_by('created')
    categories = Category.objects.all().order_by('-created')

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'store/product.html', context)


def productDetail(request, slug):
    return render(request, 'store/product-details.html')


def aboutView(request):
    return render(request, 'store/about.html')


def checkOutView(request):
    return render(request, 'store/checkout.html')


def blogView(request):
    return render(request, 'store/blog.html')
