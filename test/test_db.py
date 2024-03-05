import mysql.connector

# 获取IP地址和端口
ip_address = "127.0.0.1"
port = 3306
# 连接到数据库
db = mysql.connector.connect(
    host=ip_address,
    port=port,
    user="root",
    password="HsbotDb",
    database="mydb"
)

# 创建一个游标对象
cursor = db.cursor()

# 查询Player表的结构
cursor.execute("DESCRIBE Player")
print("Player table structure:")
for row in cursor:
    print(row)

# 查询Ranking表的结构
cursor.execute("DESCRIBE Ranking")
print("\nRanking table structure:")
for row in cursor:
    print(row)

# 关闭连接
cursor.close()
db.close()