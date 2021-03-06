from django.urls import path
from . import views

urlpatterns = [
	path('', views.HomeView.as_view(), name='products_list'),
	path('product-detail/<int:pk>', views.ItemDetailView.as_view(), name='products_details'),
	path('checkout/', views.CheckoutView.as_view(), name='checkout'),
	path('order-summary/', views.OrderSummaryVeiw.as_view(), name='order-summary'),
	path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
	path('remove_from_cart/<int:id>', views.remove_from_cart, name='remove_from_cart'),
	path('remove_single_item_from_cart/<int:id>', views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
	path('payment/', views.PaymentView.as_view(), name='payment'),
	path("create-payment-intent", views.createpayment, name="create-payment-intent"),
	path("payment-complete", views.paymentcomplete, name="payment-complete"),

]