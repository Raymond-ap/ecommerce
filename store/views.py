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
    categories = Category.objects.all().order_by('-created')

    # Get Category
    category = request.GET.get('category')
    if category == None:
        products = Product.objects.filter(published=True).order_by('created')
    else:
        products = Product.objects.filter(
            published=True, category__category=category)

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'store/product.html', context)


def productDetail(request, slug):
    product = Product.objects.get(slug=slug)
    product_images = product.images.all()

    products = Product.objects.filter(published=True).order_by('created')[:4]

    context = {
        'product': product,
        'product_images': product_images,
        'products': products
    }
    return render(request, 'store/product-details.html', context)


def aboutView(request):
    return render(request, 'store/about.html')


def checkOutView(request):
    return render(request, 'store/checkout.html')


def blogView(request):
    return render(request, 'store/blog.html')
