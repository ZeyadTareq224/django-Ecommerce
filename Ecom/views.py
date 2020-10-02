from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order, OrderItem, BillingAddress
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm



class HomeView(ListView):
    model = Item
    template_name = 'Ecom/home-page.html'
    paginate_by = 10


class ItemDetailView(DetailView):
    model = Item
    template_name = 'Ecom/product-page.html'


class OrderSummaryVeiw(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {'object': order}
            return render(self.request, 'Ecom/order_summary.html', context)

        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order")
            return redirect('/')

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
        'object': order,
        'form': form
        }
        return render(self.request, 'Ecom/checkout-page.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                appartment_address = form.cleaned_data.get('appartment_address')
                country = form.cleaned_data.get('country')
                zipcode = form.cleaned_data.get('zipcode')

                #add functionality later
                #same_shipping_address = form.cleaned_data.get('same_shipping_address')
                #save_info = form.cleaned_data.get('save_info')

                payment_option = form.cleaned_data.get('payment_option')

                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    appartment_address = appartment_address,
                    country = country,
                    zipcode = zipcode
                    )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                # Add redirect to the selected payment option

                return redirect('checkout')
            messages.warning(self.request, "Checkout incomplete")
            return redirect('checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order")    


@login_required
def add_to_cart(request, id):
    item = get_object_or_404(Item, pk=id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(Item, pk=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("products_details", pk=id)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("products_details", pk=id)

@login_required
def remove_single_item_from_cart(request, id):
    item = get_object_or_404(Item, pk=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__pk=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1 
                order_item.save()
            else:
                order.items.remove(order_item)

            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("products_details", pk=id)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("products_details", pk=id)        