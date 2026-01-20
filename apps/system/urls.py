from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (
    ApiConfigViewSet,
    FlowConfigViewSet,
    MenuViewSet,
    RouteConfigViewSet,
    api_add,
    api_detail,
    api_list,
    api_test,
    flow_add,
    flow_detail,
    flow_list,
    flow_status,
    menu_add,
    menu_detail,
    menu_list,
    menu_user,
    route_add,
    route_detail,
    route_list,
)

router = DefaultRouter()
router.register('menus', MenuViewSet, basename='menu')
router.register('apis', ApiConfigViewSet, basename='api')
router.register('routes', RouteConfigViewSet, basename='route')
router.register('flows', FlowConfigViewSet, basename='flow')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^route/list/?$', route_list, name='route-list'),
    re_path(r'^route/add/?$', route_add, name='route-add'),
    re_path(r'^route/(?P<pk>[^/]+)/?$', route_detail, name='route-detail'),

    re_path(r'^api/list/?$', api_list, name='api-list'),
    re_path(r'^api/add/?$', api_add, name='api-add'),
    re_path(r'^api/(?P<pk>[^/]+)/?$', api_detail, name='api-detail'),
    re_path(r'^api/test/?$', api_test, name='api-test'),

    re_path(r'^flow/list/?$', flow_list, name='flow-list'),
    re_path(r'^flow/add/?$', flow_add, name='flow-add'),
    re_path(r'^flow/(?P<pk>[^/]+)/status/?$', flow_status, name='flow-status'),
    re_path(r'^flow/(?P<pk>[^/]+)/?$', flow_detail, name='flow-detail'),

    re_path(r'^menu/list/?$', menu_list, name='menu-list'),
    re_path(r'^menu/add/?$', menu_add, name='menu-add'),
    re_path(r'^menu/(?P<pk>[^/]+)/?$', menu_detail, name='menu-detail'),
    re_path(r'^menu/user/?$', menu_user, name='menu-user'),
]
