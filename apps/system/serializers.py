from rest_framework import serializers
from .models import Menu, ApiConfig, RouteConfig, FlowConfig


class MenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Menu
        fields = '__all__'
    
    def get_children(self, obj):
        if obj.children.exists():
            return MenuSerializer(obj.children.all(), many=True).data
        return []


class ApiConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiConfig
        fields = '__all__'


class RouteConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteConfig
        fields = '__all__'


class FlowConfigSerializer(serializers.ModelSerializer):
    autoPassCondition = serializers.CharField(source='auto_pass_condition', required=False, allow_blank=True)
    allowRevoke = serializers.BooleanField(source='allow_revoke', required=False)
    allowTransfer = serializers.BooleanField(source='allow_transfer', required=False)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta:
        model = FlowConfig
        fields = [
            'id', 'name', 'type', 'description', 'level', 'timeout',
            'autoPassCondition', 'allowRevoke', 'allowTransfer', 'enabled',
            'nodes', 'creator', 'createdAt', 'updatedAt'
        ]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 确保使用驼峰命名返回
        if 'auto_pass_condition' in data:
            data['autoPassCondition'] = data.pop('auto_pass_condition')
        if 'allow_revoke' in data:
            data['allowRevoke'] = data.pop('allow_revoke')
        if 'allow_transfer' in data:
            data['allowTransfer'] = data.pop('allow_transfer')
        if 'created_at' in data:
            data['createdAt'] = data.pop('created_at')
        if 'updated_at' in data:
            data['updatedAt'] = data.pop('updated_at')
        return data
