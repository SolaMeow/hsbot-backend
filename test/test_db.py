import mysql.connector
from datetime import datetime

# 获取IP地址和端口
ip_address = "localhost"
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
    
# 如果Player表中有数据，选择第一行
cursor.execute("SELECT * FROM Player")
print("\nFirst row of Player table:")
rows = cursor.fetchall()  # 读取所有结果
if rows:
    print(rows[0])  # 打印第一行

# 如果Ranking表中有数据，选择第一行
cursor.execute("SELECT * FROM Ranking")
print("\nFirst row of Ranking table:")
rows = cursor.fetchall()  # 读取所有结果
if rows:
    print(rows[0])  # 打印第一行

# 查询Player表的行数量
cursor.execute("SELECT COUNT(*) FROM Player")
num_rows = cursor.fetchone()[0]
print(f"\nPlayer table has {num_rows} rows")

# 查询Ranking表的行数量
cursor.execute("SELECT COUNT(*) FROM Ranking")
num_rows = cursor.fetchone()[0]
print(f"\nRanking table has {num_rows} rows")

# 查询每个batch的数量和timestamp平均时间
cursor.execute("""
    SELECT batch, COUNT(*), AVG(TIMESTAMPDIFF(SECOND, '1970-01-01 00:00:00', timestamp)) as avg_timestamp
    FROM Ranking
    GROUP BY batch
""")
print("\nBatch counts and average timestamps:")
for row in cursor:
    batch = row[0]
    count = row[1]
    avg_timestamp = row[2]

    # 将时间戳转换为datetime对象
    avg_date = datetime.fromtimestamp(avg_timestamp)

    # 将datetime对象格式化为yyyymmdd:mm:ss
    avg_date_str = avg_date.strftime('%Y%m%d:%H:%M:%S')

    print(batch, count, avg_date_str)

# 关闭连接
cursor.close()
db.close()