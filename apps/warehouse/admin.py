from django.contrib import admin
from .models import Item, InboundRecord, OutboundRecord


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_code', 'item_name', 'category', 'current_stock', 'min_stock', 'location']
    list_filter = ['category']
    search_fields = ['item_code', 'item_name']


@admin.register(InboundRecord)
class InboundRecordAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'supplier', 'inbound_date', 'operator']
    list_filter = ['inbound_date']
    search_fields = ['item__item_name', 'supplier']


@admin.register(OutboundRecord)
class OutboundRecordAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'receiver', 'outbound_date', 'operator']
    list_filter = ['outbound_date']
    search_fields = ['item__item_name', 'receiver']
