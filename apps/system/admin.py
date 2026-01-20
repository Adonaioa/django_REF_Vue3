from django.contrib import admin
from .models import Menu, ApiConfig


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'path', 'type', 'sort', 'visible']
    list_filter = ['type', 'visible']
    search_fields = ['name', 'path']


@admin.register(ApiConfig)
class ApiConfigAdmin(admin.ModelAdmin):
    list_display = ['name', 'path', 'method', 'category', 'enabled']
    list_filter = ['method', 'category', 'enabled']
    search_fields = ['name', 'path']
