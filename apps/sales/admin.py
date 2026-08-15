from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Customer, SalesOrder, SalesOrderLine, Invoice, Payment


class SalesOrderLineInline(admin.TabularInline):
    model = SalesOrderLine
    extra = 1


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'is_active')
    list_filter = ('is_active', 'company')
    search_fields = ('name', 'email', 'tax_id', 'company__name')


@admin.register(SalesOrder)
class SalesOrderAdmin(ImportExportModelAdmin):
    list_display = ('so_number', 'customer', 'date', 'status', 'company', 'created_by')
    list_filter = ('status', 'date', 'company')
    search_fields = ('so_number', 'customer__name', 'company__name')
    inlines = [SalesOrderLineInline]


@admin.register(Invoice)
class InvoiceAdmin(ImportExportModelAdmin):
    list_display = ('invoice_number', 'customer', 'date', 'due_date', 'amount', 'status', 'company')
    list_filter = ('status', 'date', 'customer', 'company')
    search_fields = ('invoice_number', 'customer__name', 'company__name')


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    list_display = ('invoice', 'amount', 'payment_date', 'payment_method', 'company')
    list_filter = ('payment_date', 'payment_method', 'company')
    search_fields = ('invoice__invoice_number', 'company__name')
