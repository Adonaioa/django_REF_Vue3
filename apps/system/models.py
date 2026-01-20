from django.db import models


class Menu(models.Model):
    """菜单模型"""
    TYPE_CHOICES = [
        ('menu', '菜单'),
        ('button', '按钮'),
    ]
    
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                               related_name='children', verbose_name='父级菜单')
    name = models.CharField(max_length=50, verbose_name='菜单名称')
    path = models.CharField(max_length=200, blank=True, verbose_name='路由路径')
    component = models.CharField(max_length=200, blank=True, verbose_name='组件路径')
    icon = models.CharField(max_length=50, blank=True, verbose_name='图标')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='menu', verbose_name='类型')
    permission = models.CharField(max_length=100, blank=True, verbose_name='权限标识')
    sort = models.IntegerField(default=0, verbose_name='排序')
    visible = models.BooleanField(default=True, verbose_name='是否显示')
    is_external = models.BooleanField(default=False, verbose_name='是否外链')
    keep_alive = models.BooleanField(default=False, verbose_name='是否缓存')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'system_menu'
        verbose_name = '菜单'
        verbose_name_plural = '菜单列表'
        ordering = ['sort', 'created_at']
    
    def __str__(self):
        return self.name


class ApiConfig(models.Model):
    """API配置模型"""
    METHOD_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='接口名称')
    path = models.CharField(max_length=200, verbose_name='接口路径')
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, verbose_name='请求方法')
    category = models.CharField(max_length=50, verbose_name='接口分类')
    description = models.TextField(blank=True, verbose_name='描述')
    params = models.TextField(blank=True, verbose_name='请求参数')
    headers = models.TextField(blank=True, verbose_name='请求头')
    response = models.TextField(blank=True, verbose_name='响应示例')
    timeout = models.IntegerField(default=5000, verbose_name='超时时间(ms)')
    permission = models.CharField(max_length=100, blank=True, verbose_name='权限标识')
    require_auth = models.BooleanField(default=True, verbose_name='需要认证')
    enabled = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'system_api'
        verbose_name = 'API配置'
        verbose_name_plural = 'API配置列表'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.method} {self.name}"


class RouteConfig(models.Model):
    """路由配置"""
    path = models.CharField(max_length=200, verbose_name='路由路径')
    name = models.CharField(max_length=100, verbose_name='路由名称')
    component = models.CharField(max_length=200, verbose_name='组件路径')
    icon = models.CharField(max_length=50, blank=True, verbose_name='图标')
    title = models.CharField(max_length=100, blank=True, verbose_name='标题')
    hidden = models.BooleanField(default=False, verbose_name='是否隐藏')
    keep_alive = models.BooleanField(default=True, verbose_name='是否缓存')
    sort = models.IntegerField(default=1, verbose_name='排序')
    enabled = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'system_route'
        ordering = ['sort', '-created_at']

    def __str__(self):
        return self.name


class FlowConfig(models.Model):
    """流程配置"""
    LEVEL_CHOICES = [
        ('普通', '普通审批'),
        ('重要', '重要审批'),
        ('紧急', '紧急审批'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='流程名称')
    type = models.CharField(max_length=50, blank=True, verbose_name='流程类型')
    description = models.TextField(blank=True, verbose_name='描述')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='普通', verbose_name='审批级别')
    timeout = models.IntegerField(default=24, verbose_name='超时时间(小时)')
    auto_pass_condition = models.CharField(max_length=200, blank=True, verbose_name='自动通过条件')
    allow_revoke = models.BooleanField(default=True, verbose_name='是否允许撤回')
    allow_transfer = models.BooleanField(default=False, verbose_name='是否允许转审')
    enabled = models.BooleanField(default=True, verbose_name='是否启用')
    nodes = models.JSONField(default=list, verbose_name='节点配置')
    creator = models.CharField(max_length=100, blank=True, verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'system_flow'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
