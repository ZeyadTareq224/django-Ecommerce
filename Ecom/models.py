from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

CATEGORY_CHOICES = (
	('Shirts', 'SH'),
	('Sport Wears', 'SW'),
	('Out Wears', 'OW')
	)

LABEL_CHOICES = (
	('primary', 'P'),
	('secondary', 'S'),
	('danger', 'D')
	)

ITEM_STATE_CHOICES = (
	('New', 'N'),
	('Bestseller', 'BS'),
	)
class Item(models.Model):
	title = models.CharField(max_length=100,null=True, blank=True)
	price = models.FloatField(null=True, blank=True)
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=12,null=True, blank=True)
	label = models.CharField(choices=LABEL_CHOICES, max_length=10,null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	item_state = models.CharField(choices=ITEM_STATE_CHOICES , max_length=10,null=True, blank=True)
	discount_price = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return self.title

class OrderItem(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	item = models.ForeignKey(Item,on_delete=models.CASCADE,null=True, blank=True)
	quantity = models.IntegerField(default=1,null=True, blank=True)
	ordered = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.quantity} of {self.item.title}"

	def get_total_item_price(self):
		return self.quantity * self.item.price

	def get_total_item_discount_price(self):
		return self.quantity * self.item.discount_price

	def get_amount_saved(self):
		return self.get_total_item_price() - self.get_total_item_discount_price()

	def get_final_price(self):
		if self.item.discount_price:
			return self.get_total_item_discount_price()
		else:
			return self.get_total_item_price()

class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered = models.BooleanField(default=False,null=True, blank=True)
	ordered_date = models.DateTimeField()
	billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, null=True, blank=True)
	def __str__(self):
		return self.user.username

	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total


class BillingAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	street_address = models.CharField(max_length=100,null=True, blank=True)
	appartment_address = models.CharField(max_length=100,null=True, blank=True)
	country = CountryField(multiple=False)
	zipcode = models.CharField(max_length=100)

	def __str__(self):
		return self.user.username