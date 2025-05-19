import pymysql
import traceback

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456'
}

def create_database():
    """创建neon数据库"""
    conn = None
    try:
        # 连接MySQL
        print("正在连接MySQL服务器...")
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 创建数据库
        print("正在创建数据库...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS neon DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("数据库'neon'创建成功")
        
        # 关闭连接
        cursor.close()
    except Exception as e:
        print(f"创建数据库失败，错误: {str(e)}")
        traceback.print_exc()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()
    print("现在可以运行 python init_db.py 创建表和初始数据") 