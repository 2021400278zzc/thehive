#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试删除项目API
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def test_delete_project():
    """测试删除项目API"""
    print("\n=== 测试删除项目API ===")
    
    # 直接删除项目ID为5的项目
    project_id = 3
    user_id = "test_user_1"  # 使用创建该项目的用户ID
    
    # 删除项目
    response = requests.delete(f"{BASE_URL}/projects/{project_id}?user_id={user_id}")
    print("\n删除项目响应:", response.json())
    
    # 验证项目是否已被删除
    response = requests.get(f"{BASE_URL}/projects/{project_id}")
    print("\n获取已删除项目响应:", response.json())

if __name__ == "__main__":
    test_delete_project() 