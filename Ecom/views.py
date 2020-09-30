from django.shortcuts import render

def products_list(request):

	context = {}
	return render(request, 'Ecom/home-page.html', context)

def	product_details(request):

	context = {}
	return render(request, 'Ecom/product-page.html', context)

def checkout(request):

	context = {}
	return render(request, 'Ecom/checkout-page.html', context)	