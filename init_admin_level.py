#!/usr/bin/env python
"""
初始化员工管理员级别数据
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import Employee

def init_admin_level():
    """初始化管理员级别"""
    # 更新现有员工的管理员级别
    total = Employee.objects.count()
    
    # 设置第一个员工为超级管理员
    employees = Employee.objects.all().order_by('created_at')
    
    if employees:
        first_employee = employees.first()
        first_employee.level = '超级管理员'
        first_employee.save()
        print(f'✓ {first_employee.name} 设置为超级管理员')
    
    # 设置其他员工为用户（默认值已设置）
    for employee in employees[1:]:
        if not employee.level or employee.level == '':
            employee.level = '用户'
            employee.save()
    
    print(f'✓ 成功初始化 {total} 个员工的管理员级别')
    
    # 显示统计
    stats = {}
    for level, _ in Employee.LEVEL_CHOICES:
        count = Employee.objects.filter(level=level).count()
        if count > 0:
            stats[level] = count
    
    print('\n管理员级别分布:')
    for level, count in stats.items():
        print(f'  {level}: {count}')

if __name__ == '__main__':
    init_admin_level()
