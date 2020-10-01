from django.urls import path
from . import views

urlpatterns = [
	path('', views.products_list, name='products_list'),
	path('product-detail/<int:id>', views.product_details, name='products_details'),
	path('checkout/', views.checkout, name='checkout'),
	path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
	path('remove_from_cart/<int:id>', views.remove_from_cart, name='remove_from_cart'),
]