from rest_framework import viewsets, permissions
from django.db import transaction
from .models import Category, Product, Warehouse, StockMovement
from .serializers import CategorySerializer, ProductSerializer, WarehouseSerializer, StockMovementSerializer
from apps.core.mixins import TenantQuerySetMixin


class CategoryViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']


class ProductViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['category', 'is_active', 'unit']
    search_fields = ['name', 'sku', 'description']


class WarehouseViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['is_active']
    search_fields = ['name', 'location']


class StockMovementViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['movement_type', 'warehouse', 'product']
    search_fields = ['reference', 'product__name']
    
    def perform_create(self, serializer):
        movement_type = serializer.validated_data['movement_type']
        quantity = serializer.validated_data['quantity']
        product = serializer.validated_data['product']
        company = getattr(self.request.user, 'company', None)
        
        with transaction.atomic():
            serializer.save(company=company)
            if movement_type == 'in':
                product.current_stock += quantity
            elif movement_type == 'out':
                product.current_stock -= quantity
            product.save()
