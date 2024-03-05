import time
from datetime import datetime, timedelta
import mysql.connector
import crawl
import asyncio
import logging
import os

# 创建log目录
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 设置日志
log_file = os.path.join(log_dir, 'job.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

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

def job():
    # 爬取数据
    asyncio.run(crawl.crawl_data())

    # 记录保存的数据量
    cursor.execute("SELECT COUNT(*) FROM Ranking")
    count = cursor.fetchone()[0]
    logging.info(f"Saved {count} data")

    # 删除6小时前的数据
    six_hours_ago = datetime.now() - timedelta(hours=6)
    cursor.execute("DELETE FROM Ranking WHERE timestamp < %s", (six_hours_ago,))
    db.commit()

    # 记录删除的数据量
    cursor.execute("SELECT COUNT(*) FROM Ranking")
    count_after_delete = cursor.fetchone()[0]
    logging.info(f"Deleted {count - count_after_delete} data")

# 每小时执行一次任务
while True:
    job()
    print("Job done")
    time.sleep(3600)  # 暂停3600秒