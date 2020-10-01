from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order, OrderItem
from django.contrib import messages
from django.utils import timezone


def get_total_quantity_in_cart(request):
	current_cart = Order.objects.get(user=request.user)
	items = current_cart.items.all()

	total_quantity = 0
	for item in items:
		total_quantity += item.quantity

	return total_quantity
	

def products_list(request):
	
	
	total_quantity = get_total_quantity_in_cart(request)
	
	context = {
	'total_quantity': total_quantity,
	'items': Item.objects.all(),
	}
	return render(request, 'Ecom/home-page.html', context)

def	product_details(request, id):
	#nav cart items
	total_quantity = get_total_quantity_in_cart(request)
	#end nav cart items

	item = get_object_or_404(Item, id=id)
	context = {
	'item': item,
	'total_quantity': total_quantity
	}
	return render(request, 'Ecom/product-page.html', context)

def checkout(request):
	#nav cart items
	total_quantity = get_total_quantity_in_cart(request)
	#end nav cart items

	context = {'total_quantity': total_quantity}
	return render(request, 'Ecom/checkout-page.html', context)


def add_to_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("products_details", id=id)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("products_details", id=id)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("products_details", id=id)

def remove_from_cart(request, id):
    item = get_object_or_404(Item, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("products_details", id=id)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("products_details", id=id)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("products_details", id=id)