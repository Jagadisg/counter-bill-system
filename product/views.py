from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework import routers, viewsets, mixins
from django.db.models import Sum, Count, Max
from rest_framework.response import Response

from .serializer import UserSerializer, ProductSerializers, CustomerSerializers, BillSerializers
from .models import Products, Customers, Bill
from .permissions import StaffPermission

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [StaffPermission]

class CustomerViewset(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializers
    permission_classes = [StaffPermission]

class BillViewset(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializers
    permission_classes = [StaffPermission]
    
    def perform_create(self, serializer):
        employee = self.request.user
        products = serializer.validated_data.get('products')
        total = sum(product.regular_price for product in products)
        serializer.save(employee=employee,total=total)


class AnalyticDetails(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializers
    permission_classes = [StaffPermission]
    
    def list(self, request, *args, **kwargs):
        max_total_per_employee = Bill.objects.values('employee__username').annotate(
            total=Sum('total')
        ).order_by('-total')

        most_sold_product_per_employee = Bill.objects.values('employee__username', 'products__product_name').annotate(
            total_sales=Count('products')
        ).order_by('-total_sales')

        result = {}
        for item in max_total_per_employee:
            employee = item['employee__username']
            total = item['total']
            most_sold_product = most_sold_product_per_employee.filter(employee__username=employee).first()

            result[employee] = {
                'max_total': total,
                'most_sold_product': most_sold_product['products__product_name'] if most_sold_product else None
            }

        return Response(result)

    
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'product', ProductViewSet)
router.register(r'customer', CustomerViewset)
router.register(r'bill',BillViewset)
router.register(r'Analytics-api',AnalyticDetails,basename='analytic-details')