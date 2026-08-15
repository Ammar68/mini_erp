from rest_framework import serializers
from .models import Customer, SalesOrder, SalesOrderLine, Invoice, Payment


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('company',)


class SalesOrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderLine
        fields = ['id', 'product', 'quantity', 'unit_price']


class SalesOrderSerializer(serializers.ModelSerializer):
    lines = SalesOrderLineSerializer(many=True)
    
    class Meta:
        model = SalesOrder
        fields = '__all__'
        read_only_fields = ('company', 'created_by')
    
    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        sales_order = SalesOrder.objects.create(**validated_data)
        for line_data in lines_data:
            SalesOrderLine.objects.create(sales_order=sales_order, **line_data)
        return sales_order


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('company', 'created_by', 'paid_at')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('company', 'created_by')
