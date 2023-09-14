from django.shortcuts import render, redirect, get_object_or_404
from store.models import Laptop, Image, Cart, CartItem
from django.contrib.auth.decorators import login_required
from store.models import *
# Create your views here.
@login_required(login_url='login_view')
def shop(request):
    laptops = Laptop.objects.prefetch_related('images').all()
    cart = Cart.objects.filter(customer=request.user).first()
    if not cart:
        cart = Cart(customer=request.user, total = 0)
        cart.save() 
    context = {'laptops': laptops, 'cart':cart}
    return render(request, 'shopping.html', context)

@login_required(login_url='login_view')
def cart_details(request, cart_id):
    if not request.user.is_customer:
        return redirect('login_view')
    else:
        cart = Cart.objects.get(customer=request.user)
        cart_item = CartItem.objects.filter(cart = cart_id )
        context = {'cart':cart, 'cart_item':cart_item}
        return render(request, 'cart_details.html', context) 

@login_required(login_url='login_view')
def add_to_cart(request, laptop_id):
    if not request.user.is_customer:
        return redirect('login_view')
    else:
        if request.method =="POST":
            cart = Cart.objects.get(customer=request.user)
            laptop = get_object_or_404(Laptop, id=laptop_id)
            try:
                cart_item = CartItem.objects.get(cart=cart, laptop=laptop)
                # CartItem exists in the cart
                cart_item.quantity+=1
                cart_item.price = cart_item.price * cart_item.quantity
                cart_item.save()
                print("CartItem already exists in the cart.")
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(cart = cart, laptop = laptop, price = laptop.price )
                cart_item.save()
                print("CartItem does not exist in the cart.")
            try:
                cart_item = CartItem.objects.filter(cart = cart )
                total = 0
                for item in cart_item:
                    total += item.price
                cart.total = total
                cart.save()
                context = {'cart':cart, 'cart_item':cart_item}
                return render(request, 'cart_details.html', context) 
            except CartItem.DoesNotExist:
                print("Error.")
        else:
            return redirect('shopping')

@login_required(login_url='login_view')
def delete_cart_item(request, cart_item_id):
    cart = Cart.objects.get(customer=request.user)
    cart_item = CartItem.objects.get(id=cart_item_id)
    if request.method == 'POST':
        cart_item.delete()
        cart_item = CartItem.objects.filter(cart = cart )
        total = 0
        for item in cart_item:
            total += item.price
        cart.total = total
        cart.save()
        context = {'cart':cart, 'cart_item':cart_item}
        return render(request, 'cart_details.html', context) 
    return redirect('shopping')

