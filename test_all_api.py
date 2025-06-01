import requests
import json

BASE_URL = "http://localhost:5000/api"

# 请根据实际情况填写这些ID
TEST_USER_ID = "auth0|test123456789"
TEST_PROJECT_ID = 1
TEST_APPLICATION_ID = 1
TEST_DELIVERABLE_ID = 1
TEST_FILENAME = "test.txt"


def print_resp(resp):
    try:
        print(f"Status: {resp.status_code}")
        print("Response:", resp.json())
    except Exception:
        print(f"Status: {resp.status_code}")
        print("Response:", resp.text)


def test_health():
    print("\n[GET] /api/health")
    resp = requests.get(f"{BASE_URL}/health")
    print_resp(resp)

def test_create_user():
    print("\n[POST] /api/users")
    data = {
        "email": "apitestuser@example.com",
        "full_name": "API Test User",
        "user_id": TEST_USER_ID
    }
    resp = requests.post(f"{BASE_URL}/users", json=data)
    print_resp(resp)

def test_get_users():
    print("\n[GET] /api/users")
    resp = requests.get(f"{BASE_URL}/users")
    print_resp(resp)

def test_get_user_by_id():
    print("\n[GET] /api/users/<user_id>")
    resp = requests.get(f"{BASE_URL}/users/1")
    print_resp(resp)

def test_get_user_by_auth_id():
    print("\n[GET] /api/users/by-auth-id/<auth_id>")
    resp = requests.get(f"{BASE_URL}/users/by-auth-id/{TEST_USER_ID}")
    print_resp(resp)

def test_get_participant_user_list():
    print("\n[GET] /api/users/participant")
    resp = requests.get(f"{BASE_URL}/users/participant?project_id={TEST_PROJECT_ID}")
    print_resp(resp)

def test_get_skill_types():
    print("\n[GET] /api/skill-types")
    resp = requests.get(f"{BASE_URL}/skill-types")
    print_resp(resp)

def test_create_skill_type():
    print("\n[POST] /api/skill-types")
    data = {"name": "API测试技能"}
    resp = requests.post(f"{BASE_URL}/skill-types", json=data)
    print_resp(resp)

def test_create_project():
    print("\n[POST] /api/projects")
    data = {
        "name": "API测试项目",
        "project_type": "开发",
        "end_time": "2099-12-31 23:59:59",
        "user_id": TEST_USER_ID
    }
    resp = requests.post(f"{BASE_URL}/projects", json=data)
    print_resp(resp)

def test_get_projects():
    print("\n[GET] /api/projects")
    resp = requests.get(f"{BASE_URL}/projects")
    print_resp(resp)

def test_get_founder_projects():
    print("\n[GET] /api/projects/founder")
    resp = requests.get(f"{BASE_URL}/projects/founder?user_id={TEST_USER_ID}")
    print_resp(resp)

def test_get_participant_projects():
    print("\n[GET] /api/projects/participant")
    resp = requests.get(f"{BASE_URL}/projects/participant?user_id={TEST_USER_ID}")
    print_resp(resp)

def test_get_project_detail():
    print("\n[GET] /api/projects/<project_id>")
    resp = requests.get(f"{BASE_URL}/projects/{TEST_PROJECT_ID}")
    print_resp(resp)

def test_update_project():
    print("\n[PUT] /api/projects/<project_id>")
    data = {"name": "API测试项目-更新", "user_id": TEST_USER_ID}
    resp = requests.put(f"{BASE_URL}/projects/{TEST_PROJECT_ID}", json=data)
    print_resp(resp)

def test_get_project_applications():
    print("\n[GET] /api/projects/<project_id>/applications")
    resp = requests.get(f"{BASE_URL}/projects/{TEST_PROJECT_ID}/applications")
    print_resp(resp)

def test_get_project_deliverables():
    print("\n[GET] /api/projects/<project_id>/deliverables")
    resp = requests.get(f"{BASE_URL}/projects/{TEST_PROJECT_ID}/deliverables")
    print_resp(resp)

def test_get_deliverable_detail():
    print("\n[GET] /api/deliverables/<deliverable_id>")
    resp = requests.get(f"{BASE_URL}/deliverables/{TEST_DELIVERABLE_ID}")
    print_resp(resp)

def test_get_my_applications():
    print("\n[GET] /api/my-applications")
    resp = requests.get(f"{BASE_URL}/my-applications?user_id={TEST_USER_ID}")
    print_resp(resp)

def test_download_deliverable():
    print("\n[GET] /api/static/deliverables/<filename>")
    resp = requests.get(f"{BASE_URL}/static/deliverables/{TEST_FILENAME}")
    print(f"Status: {resp.status_code}")
    print(f"Content-Type: {resp.headers.get('Content-Type')}")
    print(f"Content-Length: {resp.headers.get('Content-Length')}")

def main():
    test_health()
    test_create_user()
    test_get_users()
    test_get_user_by_id()
    test_get_user_by_auth_id()
    test_get_participant_user_list()
    test_get_skill_types()
    test_create_skill_type()
    test_create_project()
    test_get_projects()
    test_get_founder_projects()
    test_get_participant_projects()
    test_get_project_detail()
    test_update_project()
    test_get_project_applications()
    test_get_project_deliverables()
    test_get_deliverable_detail()
    test_get_my_applications()
    test_download_deliverable()
    print("\n所有主要接口测试完成！")

if __name__ == "__main__":
    main() 