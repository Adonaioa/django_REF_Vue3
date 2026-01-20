from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (
    InboundRecordViewSet,
    ItemViewSet,
    OutboundRecordViewSet,
    inbound_add,
    inbound_list,
    outbound_add,
    outbound_list,
    stock_add,
    stock_detail,
    stock_export,
    stock_import,
    stock_list,
)

router = DefaultRouter()
router.register('items', ItemViewSet, basename='item')
router.register('inbound', InboundRecordViewSet, basename='inbound')
router.register('outbound', OutboundRecordViewSet, basename='outbound')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^stock/list/?$', stock_list, name='stock-list'),
    re_path(r'^stock/add/?$', stock_add, name='stock-add'),
    re_path(r'^stock/import/?$', stock_import, name='stock-import'),
    re_path(r'^stock/export/?$', stock_export, name='stock-export'),
    re_path(r'^stock/(?P<pk>[^/]+)/?$', stock_detail, name='stock-detail'),
    re_path(r'^inbound/list/?$', inbound_list, name='inbound-list'),
    re_path(r'^inbound/add/?$', inbound_add, name='inbound-add'),
    re_path(r'^outbound/list/?$', outbound_list, name='outbound-list'),
    re_path(r'^outbound/add/?$', outbound_add, name='outbound-add'),
]
