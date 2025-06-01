import requests
import os
import json
from datetime import datetime
import tempfile
import time
from contextlib import contextmanager

BASE_URL = "http://localhost:5000"

# 使用已存在的用户ID
TEST_USER_ID = "auth0|test123456789"  # 从init_db.py中的初始用户数据中获取

def check_server():
    """检查服务器是否运行"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

@contextmanager
def create_test_file():
    """创建测试文件并确保正确清理"""
    fd, path = tempfile.mkstemp(suffix='.txt')
    try:
        with os.fdopen(fd, 'w') as f:
            f.write("Test deliverable content")
        yield path
    finally:
        try:
            os.remove(path)
        except OSError:
            pass  # 忽略删除错误

def get_deliverable_detail(deliverable_id):
    """获取交付物详情"""
    url = f"{BASE_URL}/api/deliverables/{deliverable_id}"
    response = requests.get(url)
    print("\n获取交付物详情:")
    print("Status:", response.status_code)
    print("Response:", response.json())
    return response.json().get('data', {})

def test_upload_deliverable():
    """测试上传交付物（文件）"""
    url = f"{BASE_URL}/api/projects/1/deliverables"
    
    with create_test_file() as test_file_path:
        data = {
            "uploader_id": TEST_USER_ID,  # 使用已存在的用户ID
            "file_type": "text",
            "file_name": os.path.basename(test_file_path),
            "file_size": str(os.path.getsize(test_file_path)),
            "status": "0"  # 草稿状态
        }
        
        with open(test_file_path, "rb") as f:
            files = {
                "file": f
            }
            response = requests.post(url, data=data, files=files)
            print("\n测试上传交付物（文件）:")
            print("Status:", response.status_code)
            print("Response:", response.json())
            
            if response.status_code == 201:
                return response.json().get('data', {}).get('id')
            else:
                print("上传失败，错误信息:", response.json().get('error'))
                return None

def test_upload_deliverable_url():
    """测试上传交付物（URL）"""
    url = f"{BASE_URL}/api/projects/1/deliverables"
    
    data = {
        "uploader_id": TEST_USER_ID,  # 使用已存在的用户ID
        "file_type": "url",
        "link_url": "https://example.com/test",
        "status": "0"  # 草稿状态
    }
    
    response = requests.post(url, data=data)
    print("\n测试上传交付物（URL）:")
    print("Status:", response.status_code)
    print("Response:", response.json())
    
    if response.status_code == 201:
        return response.json().get('data', {}).get('id')
    else:
        print("上传失败，错误信息:", response.json().get('error'))
        return None

def test_get_deliverables(project_id):
    """测试获取项目交付物列表"""
    url = f"{BASE_URL}/api/projects/{project_id}/deliverables"
    
    response = requests.get(url)
    print("\n测试获取项目交付物列表:")
    print("Status:", response.status_code)
    print("Response:", response.json())

def test_update_deliverable_status(deliverable_id):
    """测试更新交付物状态"""
    url = f"{BASE_URL}/api/deliverables/{deliverable_id}/status"
    
    # 测试提交
    data = {
        "status": 1  # 已提交
    }
    response = requests.put(url, json=data)
    print("\n测试更新交付物状态（提交）:")
    print("Status:", response.status_code)
    print("Response:", response.json())
    
    # 测试审核
    data = {
        "status": 2,  # 已审核
        "reviewer_id": "reviewer_123"
    }
    response = requests.put(url, json=data)
    print("\n测试更新交付物状态（审核）:")
    print("Status:", response.status_code)
    print("Response:", response.json())

def test_delete_deliverable(deliverable_id):
    """测试删除交付物"""
    url = f"{BASE_URL}/api/deliverables/{deliverable_id}"
    params = {
        "uploader_id": TEST_USER_ID  # 使用已存在的用户ID
    }
    
    response = requests.delete(url, params=params)
    print("\n测试删除交付物:")
    print("Status:", response.status_code)
    print("Response:", response.json())

def test_download_deliverable(filename):
    """测试下载交付物文件"""
    url = f"{BASE_URL}/api/static/deliverables/{filename}"
    
    response = requests.get(url)
    print("\n测试下载交付物文件:")
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get('Content-Type'))
    print("Content-Length:", response.headers.get('Content-Length'))
    
    if response.status_code == 200:
        # 保存文件到临时目录
        temp_dir = "temp_downloads"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"文件已保存到: {file_path}")
        return file_path
    else:
        print("下载失败，错误信息:", response.text)
        return None

def main():
    """运行所有测试"""
    print("开始测试项目交付物功能...")
    
    # 检查服务器是否运行
    if not check_server():
        print("错误: Flask服务器未运行！请先启动服务器。")
        return
    
    try:
        # 测试上传文件交付物
        file_deliverable_id = test_upload_deliverable()
        if file_deliverable_id:
            # 获取交付物详情
            deliverable_detail = get_deliverable_detail(file_deliverable_id)
            if deliverable_detail:
                # 使用实际文件名进行下载测试
                file_name = deliverable_detail.get('file_name')
                if file_name:
                    test_download_deliverable(file_name)
        
        # 测试上传URL交付物
        url_deliverable_id = test_upload_deliverable_url()
        
        # 测试获取交付物列表
        test_get_deliverables(1)
        
        # 测试更新交付物状态
        if file_deliverable_id:
            test_update_deliverable_status(file_deliverable_id)
        
        # 测试删除交付物
        if file_deliverable_id:
            test_delete_deliverable(file_deliverable_id)
        if url_deliverable_id:
            test_delete_deliverable(url_deliverable_id)
            
        print("\n所有测试完成！")
    except Exception as e:
        print(f"\n测试过程中发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    main()