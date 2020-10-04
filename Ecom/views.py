import json
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist

#auth imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

#file imports
from .forms import CheckoutForm
from .models import Item, Order, OrderItem, ShippingAddress

#stripe payment imports
from django.conf import settings
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
import stripe


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
        context = {'form': form}
        return render(self.request, 'Ecom/checkout-page.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            country = form.cleaned_data.get('country')
            city = form.cleaned_data.get('city')
            zipcode = form.cleaned_data.get('zipcode')
            phone_number = form.cleaned_data.get('phone')
            #create shipping address instance and saving it in the database

            shipping_details = ShippingAddress(
                street_address = street_address,
                country = country,
                city = city,
                zipcode = zipcode,
                user = self.request.user,
                phone_number = phone_number
            )
            shipping_details.save()
            messages.info(self.request, "shipping details saved successfully")
            return redirect('payment')

class PaymentView(TemplateView):
    template_name = 'Ecom/payment.html'


@csrf_exempt
def createpayment(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, ordered=False)[0]
        total = order.get_total() * 100
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if request.method == "POST":

            data = json.loads(request.body)
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=total,
                currency=data['currency'],
                metadata={'integration_check': 'accept_a_payment'},
            )
            try:

                return JsonResponse({'publishableKey':
                                         settings.STRIPE_PUBLISHABLE_KEY, 'clientSecret': intent.client_secret})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=403)

def paymentcomplete(request):
    if request.method=="POST":
        data = json.loads(request.POST.get("payload"))
        if data["status"] == "succeeded":
            order = Order.objects.filter(user=request.user, ordered=False)[0]
            shipping_details = ShippingAddress.objects.filter(user=request.user)[0]
            order.ordered = True
            order.shipping_details = shipping_details
            order.save()
            print('payment completed')
            messages.success(request, "Your payment was successful")
            return render(request, "Ecom/payment_complete.html")
    return HttpResponse('IDK')

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