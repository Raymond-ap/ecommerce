from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


def globalData(request):
    items = OrderItem.objects.all()

    #  User Registration
    if request.method == 'POST' and 'Registration' in request.POST:
        data = request.POST
        user = User.objects.create_user(
            username=data['username'],
            first_name=data['lname'],
            last_name=data['lname'],
            email=data['email'],
            password=data['password1'],
        )

        if data['password1'] != data['password2']:
            messages.warning(request, 'Password does not match')
        else:
            user.save()
            login(request, user)

   # user login
    if request.method == "POST" and 'Login' in request.POST:
        data = request.POST
        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if user is not None:
            login(request, user)
        else:
            messages.warning(request, 'Login failed. Try again')

    # search product
    if request.method == 'POST' and 'Search' in request.POST:
        data = request.POST
        seacrhInput = data['Search']
        search_results = Product.objects.filter(title__contains=seacrhInput)
        # print('Results is =====', search_results)

    return {
        'items': items
    }
