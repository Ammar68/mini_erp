from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Product, Warehouse, StockMovement


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'company', 'description')
    list_filter = ('company',)
    search_fields = ('name', 'company__name')


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'sku', 'category', 'sale_price', 'current_stock', 'company', 'is_active')
    list_filter = ('category', 'is_active', 'unit', 'company')
    search_fields = ('name', 'sku', 'description', 'company__name')


@admin.register(Warehouse)
class WarehouseAdmin(ImportExportModelAdmin):
    list_display = ('name', 'location', 'company', 'is_active')
    list_filter = ('is_active', 'company')
    search_fields = ('name', 'location', 'company__name')


@admin.register(StockMovement)
class StockMovementAdmin(ImportExportModelAdmin):
    list_display = ('product', 'warehouse', 'movement_type', 'quantity', 'company', 'created_at')
    list_filter = ('movement_type', 'warehouse', 'created_at', 'company')
    search_fields = ('product__name', 'reference', 'company__name')
