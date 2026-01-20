#!/usr/bin/env python
"""
仓库管理系统 - 测试数据初始化脚本
运行方式: python populate_test_data.py
"""

import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from apps.warehouse.models import Item, InboundRecord, OutboundRecord
from apps.users.models import Employee
from apps.system.models import RouteConfig, Menu, ApiConfig
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from decimal import Decimal


def populate_warehouse_data():
    """创建仓库管理测试数据"""
    print("创建仓库数据...")
    
    # 创建默认用户（用于 operator 字段）
    operator, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'first_name': '管理员',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    # 清空现有数据
    Item.objects.all().delete()
    
    items_data = [
        {
            'item_code': 'ELEC001',
            'item_name': '笔记本电脑',
            'category': '电子产品',
            'specification': '15.6寸 Intel i7',
            'unit': '台',
            'initial_stock': 10,
            'current_stock': 8,
            'min_stock': 3,
            'location': 'A库-01',
            'remark': '高配置笔记本'
        },
        {
            'item_code': 'ELEC002',
            'item_name': '显示器',
            'category': '电子产品',
            'specification': '27寸 4K',
            'unit': '台',
            'initial_stock': 15,
            'current_stock': 12,
            'min_stock': 5,
            'location': 'A库-02',
            'remark': '高分辨率显示器'
        },
        {
            'item_code': 'OFFICE001',
            'item_name': 'A4 纸张',
            'category': '办公用品',
            'specification': '80g 白纸',
            'unit': '盒',
            'initial_stock': 100,
            'current_stock': 75,
            'min_stock': 20,
            'location': 'B库-01',
            'remark': '标准办公用纸'
        },
        {
            'item_code': 'OFFICE002',
            'item_name': '办公椅',
            'category': '办公用品',
            'specification': '人体工学设计',
            'unit': '把',
            'initial_stock': 20,
            'current_stock': 18,
            'min_stock': 5,
            'location': 'B库-02',
            'remark': '舒适办公椅'
        },
        {
            'item_code': 'MECH001',
            'item_name': '铣床',
            'category': '机械设备',
            'specification': '立式数控',
            'unit': '台',
            'initial_stock': 3,
            'current_stock': 3,
            'min_stock': 1,
            'location': 'C库-01',
            'remark': '精密加工设备'
        },
        {
            'item_code': 'DAILY001',
            'item_name': '洗手液',
            'category': '日用品',
            'specification': '500ml',
            'unit': '瓶',
            'initial_stock': 50,
            'current_stock': 35,
            'min_stock': 10,
            'location': 'D库-01',
            'remark': '消毒用品'
        },
    ]
    
    items = []
    for data in items_data:
        item = Item.objects.create(**data)
        items.append(item)
        print(f"  ✓ 创建物品: {item.item_name}")
    
    # 创建入库记录
    InboundRecord.objects.all().delete()
    for i, item in enumerate(items[:3]):
        InboundRecord.objects.create(
            item=item,
            quantity=5,
            supplier=f'供应商{i+1}',
            price=Decimal('100.00'),
            inbound_date=datetime.now().date() - timedelta(days=1),
            operator=operator,
            remark='定期补货'
        )
        print(f"  ✓ 创建入库记录: {item.item_name}")
    
    # 创建出库记录
    OutboundRecord.objects.all().delete()
    for i, item in enumerate(items[:2]):
        OutboundRecord.objects.create(
            item=item,
            quantity=2,
            receiver=f'员工{i+1}',
            outbound_date=datetime.now().date(),
            reason='日常使用',
            operator=operator
        )
        print(f"  ✓ 创建出库记录: {item.item_name}")
    
    print(f"✓ 仓库数据创建完成 (共 {len(items)} 个物品)\n")


def populate_employee_data():
    """创建人员管理测试数据"""
    print("创建员工数据...")
    
    # 清空现有数据
    Employee.objects.all().delete()
    
    employees_data = [
        {
            'work_id': 'E001',
            'name': '张三',
            'department': '仓库管理部',
            'category': '正式员工',
            'phone': '13800138000',
            'enabled': True,
            'remark': '资深仓管员'
        },
        {
            'work_id': 'E002',
            'name': '李四',
            'department': '仓库管理部',
            'category': '正式员工',
            'phone': '13800138001',
            'enabled': True,
            'remark': '仓管员'
        },
        {
            'work_id': 'E003',
            'name': '王五',
            'department': '物流配送部',
            'category': '临时员工',
            'phone': '13800138002',
            'enabled': True,
            'remark': '配送专员'
        },
        {
            'work_id': 'E004',
            'name': '赵六',
            'department': '技术部',
            'category': '正式员工',
            'phone': '13800138003',
            'enabled': True,
            'remark': '系统管理员'
        },
        {
            'work_id': 'E005',
            'name': '孙七',
            'department': '人事部',
            'category': '正式员工',
            'phone': '13800138004',
            'enabled': False,
            'remark': '已离职'
        },
    ]
    
    for data in employees_data:
        Employee.objects.create(**data)
        print(f"  ✓ 创建员工: {data['name']} ({data['work_id']})")
    
    print(f"✓ 员工数据创建完成 (共 {len(employees_data)} 个员工)\n")


def populate_system_data():
    """创建系统管理测试数据"""
    print("创建系统配置数据...")
    
    # 创建菜单
    Menu.objects.all().delete()
    
    menus_data = [
        {
            'name': '仓库管理',
            'path': '/kucun',
            'icon': 'Box',
            'sort': 1,
            'visible': True,
            'remark': '仓库相关功能'
        },
        {
            'name': '当前库存',
            'path': '/kucun',
            'icon': 'List',
            'sort': 1,
            'visible': True,
        },
        {
            'name': '物品入库',
            'path': '/ruku',
            'icon': 'Plus',
            'sort': 2,
            'visible': True,
        },
        {
            'name': '物品出库',
            'path': '/chuku',
            'icon': 'Minus',
            'sort': 3,
            'visible': True,
        },
        {
            'name': '系统管理',
            'path': '/system',
            'icon': 'Setting',
            'sort': 10,
            'visible': True,
            'remark': '系统配置和管理'
        },
    ]
    
    for data in menus_data:
        Menu.objects.create(**data)
        print(f"  ✓ 创建菜单: {data['name']}")
    
    # 创建 API 配置
    ApiConfig.objects.all().delete()
    
    apis_data = [
        {
            'name': '库存列表',
            'path': '/warehouse/stock/list',
            'method': 'GET',
            'category': 'warehouse',
            'description': '获取所有物品库存',
            'enabled': True,
        },
        {
            'name': '添加物品',
            'path': '/warehouse/stock/add',
            'method': 'POST',
            'category': 'warehouse',
            'description': '添加新物品到库存',
            'enabled': True,
        },
        {
            'name': '员工列表',
            'path': '/users/employee/list',
            'method': 'GET',
            'category': 'users',
            'description': '获取所有员工信息',
            'enabled': True,
        },
    ]
    
    for data in apis_data:
        ApiConfig.objects.create(**data)
        print(f"  ✓ 创建 API 配置: {data['name']}")
    
    print(f"✓ 系统配置数据创建完成\n")


def main():
    """主函数"""
    print("=" * 60)
    print("仓库管理系统 - 测试数据初始化")
    print("=" * 60)
    print()
    
    try:
        populate_warehouse_data()
        populate_employee_data()
        populate_system_data()
        
        print("=" * 60)
        print("✓ 所有测试数据初始化完成！")
        print("=" * 60)
        print()
        print("现在您可以:")
        print("  1. 打开浏览器访问 http://localhost:5174")
        print("  2. 浏览各个页面查看导入的测试数据")
        print("  3. 进行添加、编辑、删除等操作")
        print()
        
    except Exception as e:
        print(f"\n✗ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
