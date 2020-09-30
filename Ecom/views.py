from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order, OrderItem
from django.contrib import messages
from django.utils import timezone

def products_list(request):

	context = {
	'items': Item.objects.all()
	}
	return render(request, 'Ecom/home-page.html', context)

def	product_details(request, id):
	item = get_object_or_404(Item, id=id)
	context = {
	'item': item
	}
	return render(request, 'Ecom/product-page.html', context)

def checkout(request):

	context = {}
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
            return redirect("products_list")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("products_list")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("products_list")