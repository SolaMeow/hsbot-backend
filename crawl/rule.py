import time
from datetime import datetime, timedelta
import mysql.connector
import crawl
import asyncio
import logging
import os
from logging.handlers import RotatingFileHandler

# 创建log目录
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 设置日志
log_file = os.path.join(log_dir, 'job.log')
handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=10)
logging.basicConfig(handlers=[handler], level=logging.INFO, format='%(asctime)s - %(message)s')

# 获取IP地址和端口
port = 3306
# 连接到数据库
db = mysql.connector.connect(
    host="db",
    port=port,
    user="root",
    password="HsbotDb",
    database="mydb"
)

# 创建一个游标对象
cursor = db.cursor()

def job():
    # 爬取数据
    try:
        asyncio.run(crawl.crawl_data())
    except Exception as e:
        logging.error(f"Error in crawl_data: {e}")

    # 记录保存的数据量
    try:
        cursor.execute("SELECT COUNT(*) FROM Ranking")
        count = cursor.fetchone()[0]
        logging.info(f"Saved {count} data")
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")

    # 删除6小时前的数据
    six_hours_ago = datetime.now() - timedelta(hours=6)
    try:
        cursor.execute("DELETE FROM Ranking WHERE timestamp < %s", (six_hours_ago,))
        db.commit()
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")

    # 记录删除的数据量
    try:
        cursor.execute("SELECT COUNT(*) FROM Ranking")
        count_after_delete = cursor.fetchone()[0]
        delta = count - count_after_delete
        if delta > 0:
            logging.info(f"Deleted {delta} data")
        elif delta < 0:
            logging.info(f"Increased {-delta} data")
        else:
            logging.info("No data change")
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")

# 每小时执行一次任务
while True:
    time.sleep(60)  # 等待数据库启动
    job()
    logging.info("Job done")
    time.sleep(1200)  # 暂停1200秒
    