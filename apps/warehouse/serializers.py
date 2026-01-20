from rest_framework import serializers
from .models import Item, InboundRecord, OutboundRecord


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class InboundRecordSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.item_name', read_only=True)
    operator_name = serializers.CharField(source='operator.username', read_only=True)
    
    class Meta:
        model = InboundRecord
        fields = '__all__'
        read_only_fields = ['operator', 'created_at']
    
    def create(self, validated_data):
        validated_data['operator'] = self.context['request'].user
        return super().create(validated_data)


class OutboundRecordSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.item_name', read_only=True)
    operator_name = serializers.CharField(source='operator.username', read_only=True)
    
    class Meta:
        model = OutboundRecord
        fields = '__all__'
        read_only_fields = ['operator', 'created_at']
    
    def create(self, validated_data):
        validated_data['operator'] = self.context['request'].user
        return super().create(validated_data)
