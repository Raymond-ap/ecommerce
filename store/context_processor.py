from .models import *

def globalData(request):
    items = OrderItem.objects.all()

    return {
       'items':items
    }