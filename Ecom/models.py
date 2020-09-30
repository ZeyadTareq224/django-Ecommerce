from django.db import models
from django.conf import settings


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

class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered = models.BooleanField(default=False,null=True, blank=True)
	ordered_date = models.DateTimeField()
	def __str__(self):
		return self.user.username
