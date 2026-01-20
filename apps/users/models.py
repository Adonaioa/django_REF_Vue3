from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name='电话')
    department = models.CharField(max_length=50, blank=True, verbose_name='部门')
    position = models.CharField(max_length=50, blank=True, verbose_name='职位')
    avatar = models.CharField(max_length=200, blank=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料列表'
    
    def __str__(self):
        return self.user.username


class Employee(models.Model):
    """员工管理"""
    CATEGORY_CHOICES = [
        ('正式员工', '正式员工'),
        ('临时员工', '临时员工'),
        ('实习生', '实习生'),
        ('合同工', '合同工'),
    ]
    
    
    work_id = models.CharField(max_length=50, unique=True, verbose_name='工号')
    name = models.CharField(max_length=100, verbose_name='姓名')
    department = models.CharField(max_length=100, verbose_name='作业区/科室')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='人员类别')
    phone = models.CharField(max_length=20, verbose_name='手机号')
    enabled = models.BooleanField(default=True, verbose_name='是否启用')
    remark = models.TextField(blank=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        db_table = 'users_employee'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.work_id} - {self.name}"
