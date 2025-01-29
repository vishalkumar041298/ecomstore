from django.http import JsonResponse
from django.shortcuts import render

from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart


# Create your views here.

def payment_success(request):
    # clear the cart
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]

    return render(request, 'payment/payment-success.html')

def payment_failed(request):
    return render(request, 'payment/payment-failed.html')

def checkout(request):
    context = None
    if request.user.is_authenticated:
        try:
            shipping = ShippingAddress.objects.get(user=request.user.id)
            if shipping:
                shipping.address2 = shipping.address2 if shipping.address2 is not None else ''
                shipping.state = shipping.state if shipping.state is not None else ''
                shipping.zipcode = shipping.zipcode if shipping.zipcode is not None else ''
            context = {'shipping': shipping}
            return render(request, 'payment/checkout.html', context)
        except:
            context = None
       
    return render(request, 'payment/checkout.html', context)


def complete_order(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        shipping_address = (address1 + '\n' + address2 + '\n' + city + '\n' + state + '\n' + zipcode)
        cart = Cart(request)

        total_cost = cart.get_total_price()

        # if request.user.is_authenticated:
        #     order = Order(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost, user=request.user)
        #     order.save()
        #     for item in cart:
        #         OrderItem.objects.create(order_id=order.pk, product=item['product'], quantity=item['qty'], price=item['price'], user=request.user)

        # else:
        #     order = Order(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost, user=request.user)
        #     order.save()
        #     for item in cart:
        #         OrderItem.objects.create(order_id=order.pk, product=item['product'], quantity=item['qty'], price=item['price'])
        user = request.user if request.user.is_authenticated else None
        order = Order(full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost, user=request.user)
        order.save()
        for item in cart:
            OrderItem.objects.create(order_id=order.pk, product=item['product'], quantity=item['qty'], price=item['price'], user=user)
        
        order_success = True

        response = JsonResponse({'success': order_success})
        return response