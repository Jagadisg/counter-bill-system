from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator, RegexValidator


# Create your models here.
class Products(models.Model):
    product_name  = models.CharField(max_length=120)
    regular_price = models.DecimalField(max_digits=5, decimal_places=2 , validators=[MinValueValidator(0)])
    sale_price = models.DecimalField(max_digits=5, decimal_places=2 , validators=[MinValueValidator(0)])
    qauntity = models.DecimalField(max_digits=4, decimal_places=2 , validators=[MinValueValidator(1)])
    description = models.CharField(blank=True)
    
    def __str__(self):
        return self.product_name

    
class Customers(models.Model):
    customer_name = models.CharField(max_length=120)
    contact_no = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    email = models.EmailField()
    
    def __str__(self):
        return self.customer_name
    
    
class Bill(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='bills')
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], blank=True , null=True)   