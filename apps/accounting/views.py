from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import FiscalYear, ChartOfAccount, JournalEntry
from .serializers import FiscalYearSerializer, ChartOfAccountSerializer, JournalEntrySerializer
from apps.core.mixins import TenantQuerySetMixin


class FiscalYearViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = FiscalYearSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChartOfAccountViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = ChartOfAccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['account_type', 'is_active']
    search_fields = ['code', 'name']


class JournalEntryViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'fiscal_year', 'date']
    search_fields = ['entry_number', 'description']
    
    def perform_create(self, serializer):
        company = getattr(self.request.user, 'company', None)
        if company:
            serializer.save(company=company, created_by=self.request.user)
        else:
            serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def post(self, request, pk=None):
        journal_entry = self.get_object()
        if journal_entry.status != 'draft':
            return Response({'error': 'Only draft entries can be posted'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            journal_entry.status = 'posted'
            journal_entry.save()
        
        return Response({'status': 'posted'})
    
    @action(detail=True, methods=['post'])
    def void(self, request, pk=None):
        journal_entry = self.get_object()
        if journal_entry.status != 'posted':
            return Response({'error': 'Only posted entries can be voided'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            journal_entry.status = 'void'
            journal_entry.save()
        
        return Response({'status': 'voided'})
