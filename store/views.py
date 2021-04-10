import json
from decimal import Decimal


from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def logoutUser(request):
    logout(request)
    return redirect('products')


def homePage(request):
    featured = Product.objects.filter(published=True).order_by('created')[:4]
    blogs = Blog.objects.filter(published=True).order_by('-created')
    new_arrival = Product.objects.filter(
        published=True).order_by('-created')[:8]

    quaries = manageQuary(request)

    context = {
        'featured': featured,
        'new_arrival': new_arrival,
        'blogs': blogs
    }
    if quaries and request.GET:
        return redirect('products')

    return render(request, 'store/index.html', context)


def productsView(request):
    categories = Category.objects.all().order_by('-created')
    quaries = manageQuary(request)

    # FILTER PRODUCT ON CATEGORY
    category = request.GET.get('category')
    if category == None:
        products = Product.objects.filter(published=True).order_by('created')
    else:
        products = Product.objects.filter(
            published=True, category__category=category)

    # PAGINATOR
    paginator = Paginator(products, 16)
    page_number = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_number)

    filters = ProductFilter(request.GET, queryset=products)
    products = filters.qs

    context = {
        'products': products,
        'categories': categories,
        'quaries': quaries,
        'page_objects': page_objects,
        'paginator': paginator,
    }
    return render(request, 'store/product.html', context)


def productDetail(request, slug):
    products = Product.objects.filter(published=True).order_by('created')[:4]
    form = CommentForm()

    try:
        product = Product.objects.get(slug=slug, published=True)
        product_images = product.images.all()
    except Exception:
        return redirect('404')

    comments = Comment.objects.filter(
        product=product, approved=True).order_by('-date')

    if request.method == 'POST':
        data = request.POST
        comment = Comment(
            product=product,
            name=data['name'],
            email=data['email'],
            review=data['review']
        )

        if not Comment.objects.filter(product=product,
                                      name=data['name'], email=data['email'], review=data['review']).exists():
            comment.save()
            return redirect('detail', slug=slug)

    context = {
        'product': product,
        'product_images': product_images,
        'products': products,
        'form': form,
        'comments': comments
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
                messages.success(request, 'Cart updated')
        else:
            order = Order.objects.create(user=request.user)
            order.items.add(order_item)

    return redirect('checkout')


def decreaseQuantity(request, pk):
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
                order_item.quantity -= 1
                order_item.save()
            if order_item.quantity < 1:
                order_item.delete()
            else:
                order.items.add(order_item)
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
        messages.info(request, 'Cart updated')

    return redirect('checkout')


def blogView(request):
    blogs = Blog.objects.filter(published=True).order_by('-created')

    # Paginator
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_number)

    context = {
        'blogs': blogs,
        'page_objects': page_objects
    }
    return render(request, 'store/blog.html', context)


def blogDetail(request, slug):
    blogs = Blog.objects.filter(published=True).order_by('created')

    try:
        blog = Blog.objects.get(slug=slug, published=True)
    except Exception:
        return redirect('404')

    context = {
        'blog': blog,
        'blogs': blogs
    }
    return render(request, 'store/blog-details.html', context)


def aboutView(request):
    return render(request, 'store/about.html')


def pageNotFound(request):
    return render(request, 'store/404.html')


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        data = request.POST
        form = ContactForm(request.POST)
        if form.is_valid():
            if not Contact.objects.filter(fullname=data['fullname'], email=data['email'], subject=data['subject'], message=data['message']).exists():
                form.save()
                messages.info(request, 'We will get back to you soon')
                return redirect('contact')

    context = {
        'form': form
    }
    return render(request, 'store/contact.html', context)


def manageQuary(request):
    products = Product.objects.filter(published=True)
    if request.method == "GET":
        filters = ProductFilter(request.GET, queryset=products)
        products = filters.qs
    return products


def checkOutView(request):
    items = OrderItem.objects.all()

    context = {
        'items': items,
    }
    if not request.user.is_authenticated:
        messages.info(request, 'Login required')
        return redirect('products')
    else:
        return render(request, 'store/checkout.html', context)


# ============== PAYSTACK
