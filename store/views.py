from django.shortcuts import render

# Create your views here.


def homePage(request):
    return render(request, 'store/index.html')


def productsView(request):
    return render(request, 'store/product.html')


def productDetail(request, slug):
    return render(request, 'store/product-details.html')


def aboutView(request):
    return render(request, 'store/about.html')


def checkOutView(request):
    return render(request, 'store/checkout.html')


def blogView(request):
    return render(request, 'store/blog.html')
