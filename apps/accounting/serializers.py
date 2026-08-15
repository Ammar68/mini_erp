from rest_framework import serializers
from .models import FiscalYear, ChartOfAccount, JournalEntry, JournalEntryLine


class FiscalYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalYear
        fields = '__all__'
        read_only_fields = ('company',)


class ChartOfAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartOfAccount
        fields = '__all__'
        read_only_fields = ('company',)


class JournalEntryLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntryLine
        fields = ['id', 'account', 'description', 'debit', 'credit']


class JournalEntrySerializer(serializers.ModelSerializer):
    lines = JournalEntryLineSerializer(many=True)
    
    class Meta:
        model = JournalEntry
        fields = '__all__'
        read_only_fields = ('entry_number', 'company', 'created_by', 'posted_at')
    
    def create(self, validated_data):
        lines_data = validated_data.pop('lines')
        journal_entry = JournalEntry.objects.create(**validated_data)
        for line_data in lines_data:
            JournalEntryLine.objects.create(journal_entry=journal_entry, **line_data)
        return journal_entry
    
    def update(self, instance, validated_data):
        lines_data = validated_data.pop('lines', None)
        instance = super().update(instance, validated_data)
        if lines_data is not None:
            instance.lines.all().delete()
            for line_data in lines_data:
                JournalEntryLine.objects.create(journal_entry=instance, **line_data)
        return instance
