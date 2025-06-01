import requests
import time
import random
import string
import pymysql

BASE_URL = "http://localhost:5000/api"
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'neon',
    'charset': 'utf8mb4'
}

def print_resp(resp):
    try:
        print(f"Status: {resp.status_code}")
        print("Response:", resp.json())
    except Exception:
        print(f"Status: {resp.status_code}")
        print("Response:", resp.text)

# 1. 用户唯一性冲突测试
def test_create_user_unique():
    print("\n[POST] /api/users - 新用户")
    user_id = f"auth0|edgecase_{int(time.time())}"
    email = f"edgecase_{int(time.time())}@example.com"
    data = {"email": email, "full_name": "Edge Case User", "user_id": user_id}
    resp = requests.post(f"{BASE_URL}/users", json=data)
    print_resp(resp)
    print("\n[POST] /api/users - 重复用户")
    resp2 = requests.post(f"{BASE_URL}/users", json=data)
    print_resp(resp2)

# 2. 技能类型唯一性冲突测试
def test_create_skill_type_unique():
    print("\n[POST] /api/skill-types - 新技能")
    skill_name = f"EdgeCaseSkill_{int(time.time())}"
    data = {"name": skill_name}
    resp = requests.post(f"{BASE_URL}/skill-types", json=data)
    print_resp(resp)
    print("\n[POST] /api/skill-types - 重复技能")
    resp2 = requests.post(f"{BASE_URL}/skill-types", json=data)
    print_resp(resp2)

# 3. 项目权限测试
def test_update_project_permission():
    print("\n[PUT] /api/projects/1 - 非创建者")
    data = {"name": "无权修改", "user_id": "not_creator_id"}
    resp = requests.put(f"{BASE_URL}/projects/1", json=data)
    print_resp(resp)
    print("\n[PUT] /api/projects/1 - 创建者")
    # 假设auth0|test123456789为创建者
    data2 = {"name": "有权修改", "user_id": "auth0|test123456789"}
    resp2 = requests.put(f"{BASE_URL}/projects/1", json=data2)
    print_resp(resp2)

# 4. 交付物详情404与正常
def test_deliverable_detail():
    print("\n[GET] /api/deliverables/999999 - 不存在")
    resp = requests.get(f"{BASE_URL}/deliverables/999999")
    print_resp(resp)
    # 尝试上传一个交付物再查详情
    print("\n[POST] /api/projects/1/deliverables - 上传文件")
    files = {'file': ('edgecase.txt', b'Edge case content')}
    data = {"uploader_id": "auth0|test123456789", "file_type": "text", "file_name": "edgecase.txt", "file_size": "18", "status": "0"}
    resp2 = requests.post(f"{BASE_URL}/projects/1/deliverables", data=data, files=files)
    print_resp(resp2)
    if resp2.status_code == 201:
        deliverable_id = resp2.json().get('data', {}).get('id')
        print(f"\n[GET] /api/deliverables/{deliverable_id} - 新交付物详情")
        resp3 = requests.get(f"{BASE_URL}/deliverables/{deliverable_id}")
        print_resp(resp3)

# 5. 文件下载404与正常
def test_download_deliverable():
    print("\n[GET] /api/static/deliverables/not_exist_file.txt - 不存在")
    resp = requests.get(f"{BASE_URL}/static/deliverables/not_exist_file.txt")
    print(f"Status: {resp.status_code}")
    print(f"Content-Type: {resp.headers.get('Content-Type')}")
    print(f"Content-Length: {resp.headers.get('Content-Length')}")
    # 上传一个文件再下载
    print("\n[POST] /api/projects/1/deliverables - 上传文件")
    files = {'file': ('edgecase2.txt', b'Edge case download')}
    data = {"uploader_id": "auth0|test123456789", "file_type": "text", "file_name": "edgecase2.txt", "file_size": "18", "status": "0"}
    resp2 = requests.post(f"{BASE_URL}/projects/1/deliverables", data=data, files=files)
    print_resp(resp2)
    if resp2.status_code == 201:
        file_name = resp2.json().get('data', {}).get('file_name')
        print(f"\n[GET] /api/static/deliverables/{file_name} - 新文件下载")
        resp3 = requests.get(f"{BASE_URL}/static/deliverables/{file_name}")
        print(f"Status: {resp3.status_code}")
        print(f"Content-Type: {resp3.headers.get('Content-Type')}")
        print(f"Content-Length: {resp3.headers.get('Content-Length')}")

def test_deliverable_confirmation():
    print("\n=== 交付物确认相关接口测试 ===")
    BASE_URL = "http://localhost:5000/api"
    user_id = "auth0|test123456789"
    # 1. 上传并审核一个交付物
    print("\n[POST] /api/projects/1/deliverables - 上传文件")
    files = {'file': ('confirmtest.txt', b'Confirm test content')}
    data = {"uploader_id": user_id, "file_type": "text", "file_name": "confirmtest.txt", "file_size": "20", "status": "0"}
    resp = requests.post(f"{BASE_URL}/projects/1/deliverables", data=data, files=files)
    print_resp(resp)
    deliverable_id = None
    if resp.status_code == 201:
        deliverable_id = resp.json().get('data', {}).get('id')
    if not deliverable_id:
        print("交付物上传失败，无法继续测试")
        return
    # 2. 审核交付物（模拟管理员/审核者）
    print(f"\n[PUT] /api/deliverables/{deliverable_id}/status - 审核交付物")
    data = {"status": 2, "reviewer_id": "reviewer_123"}
    resp2 = requests.put(f"{BASE_URL}/deliverables/{deliverable_id}/status", json=data)
    print_resp(resp2)
    # 3. 贡献者确认交付物
    print(f"\n[POST] /api/deliverables/{deliverable_id}/confirm - 贡献者确认")
    data = {"user_id": user_id}
    resp3 = requests.post(f"{BASE_URL}/deliverables/{deliverable_id}/confirm", json=data)
    print_resp(resp3)
    # 4. 查询确认状态
    print(f"\n[GET] /api/deliverables/{deliverable_id}/confirm-status?user_id={user_id}")
    resp4 = requests.get(f"{BASE_URL}/deliverables/{deliverable_id}/confirm-status?user_id={user_id}")
    print_resp(resp4)
    # 5. 查询项目整体确认状态
    print(f"\n[GET] /api/projects/1/confirm-status?user_id={user_id}")
    resp5 = requests.get(f"{BASE_URL}/projects/1/confirm-status?user_id={user_id}")
    print_resp(resp5)

def clear_deliverable_confirmations():
    print("\n=== 清空 deliverable_confirmations 表 ===")
    conn = pymysql.connect(**DB_CONFIG)
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM deliverable_confirmations")
    conn.commit()
    conn.close()
    print("deliverable_confirmations 表已清空")

def register_test_users():
    print("\n=== 注册所有测试用户 ===")
    users = [
        {"user_id": "auth0|test_contributor2", "email": f"test_contributor2_{int(time.time())}@example.com", "full_name": "测试用户2"},
        {"user_id": "auth0|edgecase_1748696801", "email": f"edgecase_{int(time.time())}@example.com", "full_name": "测试用户3"}
    ]
    for user in users:
        resp = requests.post(f"{BASE_URL}/users", json=user)
        print_resp(resp)

def test_project_auto_complete_on_all_confirmed():
    print("\n=== 项目所有贡献者全部确认后自动完成测试 ===")
    project_id = 1
    user_ids = ["auth0|test_contributor2", "auth0|edgecase_1748696801"]
    deliverable_ids = []
    # 上传并审核两个交付物
    for i in range(2):
        files = {'file': (f'auto_complete_{i}.txt', b'Auto complete test')}
        data = {"uploader_id": user_ids[0], "file_type": "text", "file_name": f"auto_complete_{i}.txt", "file_size": "20", "status": "0"}
        resp = requests.post(f"{BASE_URL}/projects/{project_id}/deliverables", data=data, files=files)
        print_resp(resp)
        if resp.status_code == 201:
            deliverable_id = resp.json().get('data', {}).get('id')
            deliverable_ids.append(deliverable_id)
            # 审核交付物
            review_data = {"status": 2}
            resp2 = requests.put(f"{BASE_URL}/deliverables/{deliverable_id}/status", json=review_data)
            print_resp(resp2)
    # 两个用户分别确认所有交付物
    for user_id in user_ids:
        for deliverable_id in deliverable_ids:
            confirm_data = {"user_id": user_id}
            resp = requests.post(f"{BASE_URL}/deliverables/{deliverable_id}/confirm", json=confirm_data)
            print(f"用户 {user_id} 确认交付物 {deliverable_id}")
            print_resp(resp)
    # 检查项目状态
    resp = requests.get(f"{BASE_URL}/projects/{project_id}")
    print("\n项目状态:")
    print_resp(resp)

def main():
    clear_deliverable_confirmations()
    register_test_users()
    test_create_user_unique()
    test_create_skill_type_unique()
    test_update_project_permission()
    test_deliverable_detail()
    test_download_deliverable()
    test_deliverable_confirmation()
    test_project_auto_complete_on_all_confirmed()
    print("\n边界/异常接口测试完成！")

if __name__ == "__main__":
    main() 