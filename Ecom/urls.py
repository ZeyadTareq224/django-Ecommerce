from django.urls import path
from . import views

urlpatterns = [
	path('', views.products_list, name='products_list'),
	path('product-detail/', views.product_details, name='products_details'),
	path('checkout/', views.checkout, name='checkout'),
]