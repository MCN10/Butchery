from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm

from django.conf import settings

from .models import *
from .forms import *
from .utils import cookieCart, cartData, guestOrder

# Create your views here.
def store(request, category_slug=None):
    data = cartData(request)
    cartItems = data['cartItems']

    category = None
    products = Product.objects.all()
    categorylist = Category.objects.annotate(total_products=Count('product'))
    context = {'cartItems': cartItems, 'products':products , 'category_list' : categorylist ,'category' : category , 'shipping': False}

    return render(request, 'store/store.html', context)



def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems': cartItems, 'items': items , 'order': order}

    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems': cartItems , 'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)

def contact(request):
    if request.method == 'POST':
        message = request.POST['message']
        if request.user.is_authenticated:
            name = request.user.first_name + request.user.last_name
            email = request.user.email
            message = name + "\n" + email + "\n"+ message
            send_mail('Contact Form', message, settings.EMAIL_HOST_USER, ['django10.foxx@gmail.com', 'mcn10.foxx@gmail.com'], fail_silently="false" )
            messages.success(request, ("Your message has been sent successfully..."))
        else:
            name = request.POST['name']
            email = request.POST['email']
            message = name + "\n" + email + "\n"+ message
            send_mail('Contact Form', message, settings.EMAIL_HOST_USER, ['django10.foxx@gmail.com', 'mcn10.foxx@gmail.com'], fail_silently="false" )
            messages.success(request, ("Your message has been sent successfully..."))
        return redirect('store')

    return render(request, 'store/contact.html', {})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    print('Data: ', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()


    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Payment Complete', safe=False)
