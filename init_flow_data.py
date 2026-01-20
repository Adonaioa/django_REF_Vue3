#!/usr/bin/env python
"""
初始化流程配置测试数据
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.system.models import FlowConfig

def init_flow_data():
    """初始化测试流程数据"""
    # 清空现有数据
    FlowConfig.objects.all().delete()
    
    # 创建测试流程
    flows = [
        {
            'name': '出库审批流程',
            'type': '出库审批',
            'description': '物品出库需要经过部门主管和仓库管理员的审批',
            'level': '普通',
            'timeout': 24,
            'auto_pass_condition': '',
            'allow_revoke': True,
            'allow_transfer': False,
            'enabled': True,
            'creator': '管理员',
            'nodes': [
                {'name': '开始', 'type': 'start'},
                {'name': '部门主管审批', 'type': 'approval', 'approvers': ['张三'], 'approvalType': 'or'},
                {'name': '仓库管理员审批', 'type': 'approval', 'approvers': ['李四'], 'approvalType': 'or'},
                {'name': '结束', 'type': 'end'}
            ]
        },
        {
            'name': '采购审批流程',
            'type': '采购审批',
            'description': '金额大于5000元的采购需要总经理审批',
            'level': '重要',
            'timeout': 48,
            'auto_pass_condition': 'amount > 5000',
            'allow_revoke': True,
            'allow_transfer': True,
            'enabled': True,
            'creator': '管理员',
            'nodes': [
                {'name': '开始', 'type': 'start'},
                {'name': '部门主管审批', 'type': 'approval', 'approvers': ['张三', '王五'], 'approvalType': 'or'},
                {'name': '财务审批', 'type': 'approval', 'approvers': ['李四'], 'approvalType': 'or', 'condition': 'amount > 5000'},
                {'name': '结束', 'type': 'end'}
            ]
        },
        {
            'name': '入库审批流程',
            'type': '入库审批',
            'description': '所有入库请求都需要仓库管理员审批',
            'level': '普通',
            'timeout': 12,
            'auto_pass_condition': '',
            'allow_revoke': True,
            'allow_transfer': False,
            'enabled': True,
            'creator': '管理员',
            'nodes': [
                {'name': '开始', 'type': 'start'},
                {'name': '仓库管理员审批', 'type': 'approval', 'approvers': ['李四'], 'approvalType': 'or'},
                {'name': '结束', 'type': 'end'}
            ]
        }
    ]
    
    for flow_data in flows:
        flow = FlowConfig.objects.create(**flow_data)
        print(f'✓ 创建流程: {flow.name}')
    
    print(f'\n✓ 成功初始化 {len(flows)} 个流程配置')

if __name__ == '__main__':
    init_flow_data()
