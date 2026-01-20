from rest_framework import filters, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import ApiConfig, FlowConfig, Menu, RouteConfig
from .serializers import (
    ApiConfigSerializer,
    FlowConfigSerializer,
    MenuSerializer,
    RouteConfigSerializer,
)


def _success(data=None, message="success"):
    return {"code": 200, "message": message, "data": data}


class _Page(PageNumberPagination):
    page_size_query_param = "size"
    page_query_param = "page"


class MenuViewSet(viewsets.ModelViewSet):
    """菜单管理视图集"""
    queryset = Menu.objects.filter(parent__isnull=True)
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'visible']
    search_fields = ['name', 'path']
    ordering_fields = ['sort', 'created_at']
    permission_classes = [AllowAny]


class ApiConfigViewSet(viewsets.ModelViewSet):
    """API配置管理视图集"""
    queryset = ApiConfig.objects.all()
    serializer_class = ApiConfigSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['method', 'category', 'enabled']
    search_fields = ['name', 'path']
    ordering_fields = ['created_at']
    permission_classes = [AllowAny]


class RouteConfigViewSet(viewsets.ModelViewSet):
    queryset = RouteConfig.objects.all()
    serializer_class = RouteConfigSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'path']
    ordering_fields = ['sort', 'created_at']
    permission_classes = [AllowAny]


class FlowConfigViewSet(viewsets.ModelViewSet):
    queryset = FlowConfig.objects.all()
    serializer_class = FlowConfigSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']
    permission_classes = [AllowAny]


# ====== Custom endpoints for frontend expectations ======


@api_view(['GET'])
@permission_classes([AllowAny])
def route_list(request):
    paginator = _Page()
    qs = RouteConfig.objects.all().order_by('sort', '-created_at')
    page = paginator.paginate_queryset(qs, request)
    serializer = RouteConfigSerializer(page, many=True)
    payload = {
        "list": serializer.data,
        "total": paginator.page.paginator.count if paginator.page else qs.count(),
        "page": paginator.page.number if paginator.page else 1,
        "size": paginator.get_page_size(request),
    }
    return Response(_success(payload))


@api_view(['POST'])
@permission_classes([AllowAny])
def route_add(request):
    serializer = RouteConfigSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(_success(None, "添加成功"))


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def route_detail(request, pk: int):
    instance = RouteConfig.objects.filter(pk=pk).first()
    if not instance:
        return Response(_success(None, "未找到"))
    if request.method in ['PUT', 'PATCH']:
        serializer = RouteConfigSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_success(None, "更新成功"))
    if request.method == 'DELETE':
        instance.delete()
        return Response(_success(None, "删除成功"))
    serializer = RouteConfigSerializer(instance)
    return Response(_success(serializer.data))


@api_view(['GET'])
@permission_classes([AllowAny])
def api_list(request):
    paginator = _Page()
    qs = ApiConfig.objects.all().order_by('-created_at')
    page = paginator.paginate_queryset(qs, request)
    serializer = ApiConfigSerializer(page, many=True)
    payload = {
        "list": serializer.data,
        "total": paginator.page.paginator.count if paginator.page else qs.count(),
        "page": paginator.page.number if paginator.page else 1,
        "size": paginator.get_page_size(request),
    }
    return Response(_success(payload))


@api_view(['POST'])
@permission_classes([AllowAny])
def api_add(request):
    serializer = ApiConfigSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(_success(None, "添加成功"))


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def api_detail(request, pk: int):
    instance = ApiConfig.objects.filter(pk=pk).first()
    if not instance:
        return Response(_success(None, "未找到"))
    if request.method in ['PUT', 'PATCH']:
        serializer = ApiConfigSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_success(None, "更新成功"))
    if request.method == 'DELETE':
        instance.delete()
        return Response(_success(None, "删除成功"))
    serializer = ApiConfigSerializer(instance)
    return Response(_success(serializer.data))


@api_view(['POST'])
@permission_classes([AllowAny])
def api_test(request):
    # 简单回显，用于前端测试
    return Response(_success({"echo": request.data}, "测试成功"))


@api_view(['GET'])
@permission_classes([AllowAny])
def flow_list(request):
    paginator = _Page()
    qs = FlowConfig.objects.all().order_by('-created_at')
    page = paginator.paginate_queryset(qs, request)
    serializer = FlowConfigSerializer(page, many=True)
    payload = {
        "list": serializer.data,
        "total": paginator.page.paginator.count if paginator.page else qs.count(),
        "page": paginator.page.number if paginator.page else 1,
        "size": paginator.get_page_size(request),
    }
    return Response(_success(payload))


@api_view(['POST'])
@permission_classes([AllowAny])
def flow_add(request):
    serializer = FlowConfigSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(_success(None, "添加成功"))


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def flow_detail(request, pk: int):
    instance = FlowConfig.objects.filter(pk=pk).first()
    if not instance:
        return Response(_success(None, "未找到"))
    if request.method in ['PUT', 'PATCH']:
        serializer = FlowConfigSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_success(serializer.data, "更新成功"))
    if request.method == 'DELETE':
        instance.delete()
        return Response(_success(None, "删除成功"))
    serializer = FlowConfigSerializer(instance)
    return Response(_success(serializer.data))


@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def flow_status(request, pk: int):
    instance = FlowConfig.objects.filter(pk=pk).first()
    if not instance:
        return Response(_success(None, "未找到"))
    enabled = request.data.get('enabled', instance.enabled)
    instance.enabled = enabled
    instance.save()
    return Response(_success(None, f"流程已{'启用' if enabled else '禁用'}"))



@api_view(['GET'])
@permission_classes([AllowAny])
def menu_list(request):
    data = MenuSerializer(Menu.objects.filter(parent__isnull=True).order_by('sort'), many=True).data
    return Response(_success(data))


@api_view(['POST'])
@permission_classes([AllowAny])
def menu_add(request):
    serializer = MenuSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(_success(None, "添加成功"))


@api_view(['PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def menu_detail(request, pk: int):
    instance = Menu.objects.filter(pk=pk).first()
    if not instance:
        return Response(_success(None, "未找到"))
    if request.method in ['PUT', 'PATCH']:
        serializer = MenuSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_success(None, "更新成功"))
    if request.method == 'DELETE':
        instance.delete()
        return Response(_success(None, "删除成功"))
    serializer = MenuSerializer(instance)
    return Response(_success(serializer.data))


@api_view(['GET'])
@permission_classes([AllowAny])
def menu_user(request):
    data = MenuSerializer(Menu.objects.filter(visible=True).order_by('sort'), many=True).data
    return Response(_success(data))
