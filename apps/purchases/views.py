from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Vendor, PurchaseOrder, PurchaseOrderLine, Bill, BillPayment
from .serializers import VendorSerializer, PurchaseOrderSerializer, PurchaseOrderLineSerializer, BillSerializer, BillPaymentSerializer
from apps.core.mixins import TenantQuerySetMixin


class VendorViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['is_active']
    search_fields = ['name', 'email', 'tax_id']


class PurchaseOrderViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = PurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'vendor', 'date']
    search_fields = ['po_number', 'vendor__name']
    
    def perform_create(self, serializer):
        company = getattr(self.request.user, 'company', None)
        if company:
            serializer.save(company=company, created_by=self.request.user)
        else:
            serializer.save(created_by=self.request.user)


class BillViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'vendor', 'date']
    search_fields = ['bill_number', 'vendor__name']
    
    def perform_create(self, serializer):
        company = getattr(self.request.user, 'company', None)
        if company:
            serializer.save(company=company, created_by=self.request.user)
        else:
            serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        bill = self.get_object()
        if bill.status == 'paid':
            return Response({'error': 'Bill is already paid'}, status=status.HTTP_400_BAD_REQUEST)
        
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        company = getattr(self.request.user, 'company', None)
        with transaction.atomic():
            BillPayment.objects.create(
                company=company,
                bill=bill,
                amount=amount,
                payment_date=request.data.get('payment_date'),
                payment_method=request.data.get('payment_method', 'cash'),
                reference=request.data.get('reference', ''),
                notes=request.data.get('notes', ''),
                created_by=request.user,
            )
            bill.status = 'paid'
            bill.save()
        
        return Response({'status': 'paid'})


class BillPaymentViewSet(TenantQuerySetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = BillPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
