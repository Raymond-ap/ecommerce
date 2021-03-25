from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from decimal import Decimal
from .models import *


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


def addCart(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=pk)
        order_item, created = OrderItem.objects.get_or_create(
            user=request.user,
            item=product,
            ordered=False
        )

        order_set = Order.objects.filter(user=request.user, ordered=False)
        if order_set.exists():
            order = order_set[0]
            # check if order item is in order
            if order.items.filter(item_id=product.id).exists():
                # update qunatity
                order_item.quantity += 1
                order_item.save()
            else:
                order.items.add(order_item)
                messages.info(request, 'Item added')
        else:
            order = Order.objects.create(user=request.user)
            order.items.add(order_item)

    return redirect('checkout')


def removeCartItem(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_set = Order.objects.filter(user=request.user, ordered=False)
    orderItems = OrderItem.objects.filter(user=request.user, item=product)
    if orderItems:
        orderItems.delete()

    return redirect('checkout')


def checkOutView(request):
    items = OrderItem.objects.all()
    context = {
        'items': items
    }
    return render(request, 'store/checkout.html', context)


def blogView(request):
    return render(request, 'store/blog.html')


def aboutView(request):
    return render(request, 'store/about.html')
