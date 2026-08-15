from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Vendor, PurchaseOrder, PurchaseOrderLine, Bill, BillPayment


class PurchaseOrderLineInline(admin.TabularInline):
    model = PurchaseOrderLine
    extra = 1


@admin.register(Vendor)
class VendorAdmin(ImportExportModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'is_active')
    list_filter = ('is_active', 'company')
    search_fields = ('name', 'email', 'tax_id', 'company__name')


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(ImportExportModelAdmin):
    list_display = ('po_number', 'vendor', 'date', 'status', 'company', 'created_by')
    list_filter = ('status', 'date', 'company')
    search_fields = ('po_number', 'vendor__name', 'company__name')
    inlines = [PurchaseOrderLineInline]


@admin.register(Bill)
class BillAdmin(ImportExportModelAdmin):
    list_display = ('bill_number', 'vendor', 'date', 'due_date', 'amount', 'status', 'company')
    list_filter = ('status', 'date', 'vendor', 'company')
    search_fields = ('bill_number', 'vendor__name', 'company__name')


@admin.register(BillPayment)
class BillPaymentAdmin(ImportExportModelAdmin):
    list_display = ('bill', 'amount', 'payment_date', 'payment_method', 'company')
    list_filter = ('payment_date', 'payment_method', 'company')
    search_fields = ('bill__bill_number', 'company__name')
