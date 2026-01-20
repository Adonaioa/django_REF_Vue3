from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import UserProfile, Employee
from .serializers import UserSerializer, RegisterSerializer, EmployeeSerializer


def _success(data=None, message="success"):
    return {"code": 200, "message": message, "data": data}


class _Page(PageNumberPagination):
    page_size_query_param = "size"
    page_query_param = "page"


class UserViewSet(viewsets.ModelViewSet):
    """用户管理视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """用户注册"""
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': '注册成功'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """当前用户修改密码"""
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not all([old_password, new_password, confirm_password]):
            return Response(_success(None, "参数不完整"), status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response(_success(None, "两次密码不一致"), status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(old_password):
            return Response(_success(None, "原密码错误"), status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response(_success(None, "密码修改成功"))

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """管理员重置指定用户密码"""
        if not request.user.is_staff and not request.user.is_superuser:
            return Response(_success(None, "没有权限"), status=status.HTTP_403_FORBIDDEN)

        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password:
            return Response(_success(None, "参数不完整"), status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response(_success(None, "两次密码不一致"), status=status.HTTP_400_BAD_REQUEST)

        target = self.get_object()
        target.set_password(new_password)
        target.save()
        return Response(_success(None, "密码已重置"))


class EmployeeViewSet(viewsets.ModelViewSet):
    """员工管理视图集"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]
    ordering_fields = ['work_id', 'name', 'created_at']


# ====== Custom endpoints for employee management ======


@api_view(['GET'])
@permission_classes([AllowAny])
def employee_list(request):
    paginator = _Page()
    qs = Employee.objects.all().order_by('-created_at')
    page = paginator.paginate_queryset(qs, request)
    serializer = EmployeeSerializer(page, many=True)
    payload = {
        "list": serializer.data,
        "total": paginator.page.paginator.count if paginator.page else qs.count(),
        "page": paginator.page.number if paginator.page else 1,
        "size": paginator.get_page_size(request),
    }
    return Response(_success(payload))


@api_view(['POST'])
@permission_classes([AllowAny])
def employee_add(request):
    serializer = EmployeeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(_success(serializer.data, "添加成功"))


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def employee_detail(request, pk: int):
    instance = get_object_or_404(Employee, pk=pk)
    
    if request.method in ['PUT', 'PATCH']:
        serializer = EmployeeSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_success(serializer.data, "更新成功"))
    
    if request.method == 'DELETE':
        instance.delete()
        return Response(_success(None, "删除成功"))
    
    serializer = EmployeeSerializer(instance)
    return Response(_success(serializer.data))
