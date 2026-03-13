import os
from dotenv import load_dotenv

load_dotenv()

# 构建连接字符串
host = os.getenv('MYSQL_HOST')
port = os.getenv('MYSQL_PORT')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
db = os.getenv('MYSQL_DB')

# 打印各部分
print(f"Host: {host!r}")
print(f"Port: {port!r}")
print(f"User: {user!r}")
print(f"Password: {password!r}")
print(f"DB: {db!r}")

# 完整连接字符串
connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4"
print(f"\nConnection String: {connection_string!r}")

# 测试连接
import pymysql
try:
    conn = pymysql.connect(host=host, port=int(port), user=user, password=password, database=db)
    print("\n✅ Direct pymysql connection successful")
    conn.close()
except Exception as e:
    print(f"\n❌ Direct pymysql connection failed: {e}")
