from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Products, Customers, Bill
from .validators import unique_Product_name,unique_customer_name


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        password_confirm = validated_data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match")
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    
class ProductSerializers(serializers.ModelSerializer):
    product_name = serializers.CharField(validators=[unique_Product_name])
    class Meta:
        model = Products
        fields = ['id', 'product_name', 'regular_price', 'sale_price', "qauntity", 'description']
        
        
class CustomerSerializers(serializers.ModelSerializer):
    customer_name = serializers.CharField(validators=[unique_customer_name])
    class Meta:
        model = Customers
        fields = ["id", "customer_name", "contact_no", "email"]
        
        
class BillSerializers(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    product_names = serializers.SerializerMethodField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def get_customer_name(self, obj):
        return obj.customer.customer_name if obj.customer else None

    def get_product_names(self, obj):
        return [product.product_name for product in obj.products.all()]
    
    class Meta:
        model = Bill
        fields = ["id","customer", "products", "customer_name", "product_names", "total"]
        extra_kwargs = {
            'customer': {'write_only': True},
            'products': {'write_only': True}
        }
        
    
    