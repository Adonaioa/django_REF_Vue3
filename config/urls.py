from django.contrib import admin
from django.urls import path, include

from apps.users.auth_views import (
    CustomTokenObtainPairView,
    refresh_token,
    user_info,
    logout_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT认证
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', refresh_token, name='token_refresh'),
    path('api/auth/userInfo/', user_info, name='user_info'),
    path('api/auth/logout/', logout_view, name='user_logout'),
    
    # 应用路由
    path('api/warehouse/', include('apps.warehouse.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/system/', include('apps.system.urls')),
]
