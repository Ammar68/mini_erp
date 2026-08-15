from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Customer, SalesOrder, SalesOrderLine, Invoice, Payment
from .serializers import CustomerSerializer, SalesOrderSerializer, SalesOrderLineSerializer, InvoiceSerializer, PaymentSerializer
from apps.core.mixins import TenantQuerySetMixin


class CustomerViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['is_active']
    search_fields = ['name', 'email', 'tax_id']


class SalesOrderViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'customer', 'date']
    search_fields = ['so_number', 'customer__name']
    
    def perform_create(self, serializer):
        company = getattr(self.request.user, 'company', None)
        if company:
            serializer.save(company=company, created_by=self.request.user)
        else:
            serializer.save(created_by=self.request.user)


class InvoiceViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'customer', 'date']
    search_fields = ['invoice_number', 'customer__name']
    
    def perform_create(self, serializer):
        company = getattr(self.request.user, 'company', None)
        if company:
            serializer.save(company=company, created_by=self.request.user)
        else:
            serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        invoice = self.get_object()
        if invoice.status != 'draft':
            return Response({'error': 'Only draft invoices can be sent'}, status=status.HTTP_400_BAD_REQUEST)
        invoice.status = 'sent'
        invoice.save()
        return Response({'status': 'sent'})
    
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        invoice = self.get_object()
        if invoice.status == 'paid':
            return Response({'error': 'Invoice is already paid'}, status=status.HTTP_400_BAD_REQUEST)
        
        amount = request.data.get('amount')
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        company = getattr(self.request.user, 'company', None)
        with transaction.atomic():
            Payment.objects.create(
                company=company,
                invoice=invoice,
                amount=amount,
                payment_date=request.data.get('payment_date'),
                payment_method=request.data.get('payment_method', 'cash'),
                reference=request.data.get('reference', ''),
                notes=request.data.get('notes', ''),
                created_by=request.user,
            )
            invoice.status = 'paid'
            invoice.save()
        
        return Response({'status': 'paid'})


class PaymentViewSet(TenantQuerySetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
