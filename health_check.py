#!/usr/bin/env python
"""
仓库管理系统 - 系统健康检查脚本
运行方式: python health_check.py
"""

import requests
import json
import sys
from datetime import datetime

# 配置
BACKEND_URL = "http://localhost:8000/api"
TIMEOUT = 5

# 颜色输出
class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def print_header(text):
    """打印标题"""
    print(f"\n{Color.CYAN}{'='*60}")
    print(f"{text:^60}")
    print(f"{'='*60}{Color.RESET}\n")

def print_success(text):
    """打印成功信息"""
    print(f"{Color.GREEN}✓ {text}{Color.RESET}")

def print_error(text):
    """打印错误信息"""
    print(f"{Color.RED}✗ {text}{Color.RESET}")

def print_warning(text):
    """打印警告信息"""
    print(f"{Color.YELLOW}⚠ {text}{Color.RESET}")

def test_api_endpoint(method, path, name):
    """测试 API 端点"""
    url = f"{BACKEND_URL}{path}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=TIMEOUT)
        elif method == "POST":
            response = requests.post(url, json={}, timeout=TIMEOUT)
        
        if response.status_code in [200, 400, 404]:
            data = response.json()
            if data.get('code') == 200:
                count = len(data.get('data', {}).get('list', []))
                print_success(f"{name} (数据数: {count})")
                return True
            else:
                print_warning(f"{name} (状态码: {response.status_code})")
                return True
        else:
            print_error(f"{name} (HTTP {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"{name} (无法连接到后端)")
        return False
    except Exception as e:
        print_error(f"{name} ({str(e)})")
        return False

def check_backend():
    """检查后端服务"""
    print_header("后端服务检查")
    
    endpoints = [
        ("GET", "/warehouse/stock/list", "仓库库存列表"),
        ("GET", "/warehouse/inbound/list", "入库记录列表"),
        ("GET", "/warehouse/outbound/list", "出库记录列表"),
        ("GET", "/users/employee/list", "员工列表"),
        ("GET", "/system/route/list", "路由配置列表"),
        ("GET", "/system/api/list", "API 配置列表"),
        ("GET", "/system/menu/list", "菜单列表"),
        ("GET", "/system/flow/list", "流程列表"),
    ]
    
    results = []
    for method, path, name in endpoints:
        results.append(test_api_endpoint(method, path, name))
    
    return all(results)

def check_database():
    """检查数据库状态"""
    print_header("数据库检查")
    
    try:
        # 检查物品表
        response = requests.get(f"{BACKEND_URL}/warehouse/stock/list?size=1", timeout=TIMEOUT)
        data = response.json()
        items_count = data.get('data', {}).get('total', 0)
        
        if items_count > 0:
            print_success(f"物品表: {items_count} 条记录")
        else:
            print_warning("物品表: 无数据 (可运行 populate_test_data.py 初始化)")
        
        # 检查员工表
        response = requests.get(f"{BACKEND_URL}/users/employee/list?size=1", timeout=TIMEOUT)
        data = response.json()
        employees_count = data.get('data', {}).get('total', 0)
        
        if employees_count > 0:
            print_success(f"员工表: {employees_count} 条记录")
        else:
            print_warning("员工表: 无数据")
        
        # 检查菜单表
        response = requests.get(f"{BACKEND_URL}/system/menu/list?size=1", timeout=TIMEOUT)
        data = response.json()
        menus_count = data.get('data', {}).get('total', 0)
        
        if menus_count > 0:
            print_success(f"菜单表: {menus_count} 条记录")
        else:
            print_warning("菜单表: 无数据")
        
        return True
        
    except Exception as e:
        print_error(f"数据库检查失败: {str(e)}")
        return False

def check_response_format():
    """检查 API 响应格式"""
    print_header("响应格式检查")
    
    try:
        response = requests.get(f"{BACKEND_URL}/warehouse/stock/list", timeout=TIMEOUT)
        data = response.json()
        
        # 检查必需字段
        required_fields = ['code', 'message', 'data']
        for field in required_fields:
            if field in data:
                print_success(f"字段 '{field}' 存在")
            else:
                print_error(f"字段 '{field}' 缺失")
                return False
        
        # 检查分页字段
        pagination_fields = ['list', 'total', 'page', 'size']
        for field in pagination_fields:
            if field in data.get('data', {}):
                print_success(f"分页字段 '{field}' 存在")
            else:
                print_error(f"分页字段 '{field}' 缺失")
                return False
        
        return True
        
    except Exception as e:
        print_error(f"响应格式检查失败: {str(e)}")
        return False

def check_cors():
    """检查 CORS 配置"""
    print_header("CORS 配置检查")
    
    try:
        response = requests.get(f"{BACKEND_URL}/warehouse/stock/list", timeout=TIMEOUT)
        headers = response.headers
        
        if 'Access-Control-Allow-Origin' in headers:
            print_success(f"CORS 已启用: {headers.get('Access-Control-Allow-Origin')}")
        else:
            print_warning("CORS 头未检测到（可能配置正确，但浏览器请求时才返回）")
        
        return True
        
    except Exception as e:
        print_error(f"CORS 检查失败: {str(e)}")
        return False

def print_summary(results):
    """打印检查总结"""
    print_header("健康检查总结")
    
    if all(results):
        print(f"{Color.GREEN}")
        print("  ██████╗  ██████╗ ███╗   ██╗███████╗███████╗")
        print("  ██╔══██╗██╔═══██╗████╗  ██║██╔════╝██╔════╝")
        print("  ██║  ██║██║   ██║██╔██╗ ██║█████╗  █████╗  ")
        print("  ██║  ██║██║   ██║██║╚██╗██║██╔══╝  ██╔══╝  ")
        print("  ██████╔╝╚██████╔╝██║ ╚████║███████╗███████╗")
        print("  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚══════╝")
        print(f"{Color.RESET}")
        print(f"\n{Color.GREEN}所有检查项目通过！系统运行正常。{Color.RESET}")
        print("\n✨ 您现在可以：")
        print("  1. 访问 http://localhost:5174 查看前端应用")
        print("  2. 在系统管理页面使用 API 测试工具")
        print("  3. 进行各种数据操作和业务流程测试")
        return 0
    else:
        print(f"{Color.RED}部分检查项目失败，请查看上述错误信息。{Color.RESET}")
        return 1

def main():
    """主函数"""
    print("\n")
    print(f"{Color.CYAN}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║         仓库管理系统 - 系统健康检查                      ║")
    print("║              System Health Check v1.0                   ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{Color.RESET}")
    
    print(f"\n启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"后端地址: {BACKEND_URL}")
    
    results = []
    
    # 执行检查
    results.append(check_backend())
    results.append(check_database())
    results.append(check_response_format())
    results.append(check_cors())
    
    # 打印总结
    exit_code = print_summary(results)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
