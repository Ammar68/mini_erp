from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import FiscalYear, ChartOfAccount, JournalEntry, JournalEntryLine


@admin.register(FiscalYear)
class FiscalYearAdmin(ImportExportModelAdmin):
    list_display = ('name', 'company', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'company')
    search_fields = ('name', 'company__name')


@admin.register(ChartOfAccount)
class ChartOfAccountAdmin(ImportExportModelAdmin):
    list_display = ('code', 'name', 'account_type', 'company', 'is_active')
    list_filter = ('account_type', 'is_active', 'company')
    search_fields = ('code', 'name', 'company__name')


class JournalEntryLineInline(admin.TabularInline):
    model = JournalEntryLine
    extra = 1


@admin.register(JournalEntry)
class JournalEntryAdmin(ImportExportModelAdmin):
    list_display = ('entry_number', 'date', 'fiscal_year', 'status', 'company', 'created_by')
    list_filter = ('status', 'fiscal_year', 'date', 'company')
    search_fields = ('entry_number', 'description', 'company__name')
    inlines = [JournalEntryLineInline]
    readonly_fields = ('entry_number', 'created_by', 'posted_at')


@admin.register(JournalEntryLine)
class JournalEntryLineAdmin(ImportExportModelAdmin):
    list_display = ('journal_entry', 'account', 'debit', 'credit')
    list_filter = ('account__account_type',)
    search_fields = ('journal_entry__entry_number', 'account__code')
