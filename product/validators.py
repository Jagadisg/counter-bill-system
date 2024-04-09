from rest_framework.validators import UniqueValidator

from .models import Customers,Products


unique_customer_name = UniqueValidator(queryset=Customers.objects.all())
unique_Product_name = UniqueValidator(queryset=Products.objects.all())