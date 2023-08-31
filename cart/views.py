from django.core.exceptions import ObjectDoesNotExist 
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Cart, CartItem

#Getting cart of that session
def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

#Incrementing product to cart 
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.cart_quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product, 
            cart_quantity=1, 
            cart=cart
        )

    cart_item.save()
    return redirect('cart')

#Decrementing product from cart
def remove_cart(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
        if cart_item.cart_quantity > 1:
            cart_item.cart_quantity -= 1
            cart_item.save() 
        else:
            cart_item.delete()

        return redirect('cart')
    except ObjectDoesNotExist:
        return redirect('cart')

#Removing product from cart
def remove_product(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
        cart_item.delete()
        return redirect('cart')
    except ObjectDoesNotExist:
        return redirect('cart')

#Displaying the cart
def cart(request):
    total = 0
    cart_quantity = 0
    cart_items = None

    try:
        cart_obj = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart_obj, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.cart_quantity)
            cart_quantity += cart_item.cart_quantity 

        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'cart_quantity': cart_quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)
