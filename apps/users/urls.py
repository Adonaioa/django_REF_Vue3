from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, EmployeeViewSet, employee_list, employee_add, employee_detail

router = DefaultRouter()
router.register('', UserViewSet, basename='user')
router.register('employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^employee/list/?$', employee_list, name='employee-list'),
    re_path(r'^employee/add/?$', employee_add, name='employee-add'),
    re_path(r'^employee/(?P<pk>[^/]+)/?$', employee_detail, name='employee-detail'),
]
