import aiohttp
import json
import asyncio
import mysql.connector
from datetime import datetime
import logging

# 创建一个日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建一个日志处理器，将日志输出到控制台
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# 添加处理器到记录器
logger.addHandler(handler)

async def total_page(session, url, headers):
    async with session.get(url, headers=headers) as response:
        info = await response.text()
        json_dict = json.loads(info)
        page_size = json_dict["leaderboard"]["pagination"]["totalPages"]
        return int(page_size)

async def fetch_page(session, url, headers):
    async with session.get(url, headers=headers) as response:
        info = await response.text()
        json_dict = json.loads(info)
        rank_name = json_dict["leaderboard"]["rows"]
        page_results = []
        for item in rank_name:
            rank, name = item['rank'], item['accountid']
            page_results.append((rank, name))
        return page_results


BATCH_SIZE = 5000  # 每批数据的大小

async def reqRankLev(region: str, leaderboardId: str, new_batch: int):
    all_results = []
    test_url = f"https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region={region}&leaderboardId={leaderboardId}&page=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        page_size = await total_page(session, test_url, headers)
        tasks = []
        for i in range(1, page_size + 1):
            html = f"https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region={region}&leaderboardId={leaderboardId}&page={i}"
            tasks.append(fetch_page(session, html, headers))
        results = await asyncio.gather(*tasks)
        for page_results in results:
            all_results.extend(page_results)
    
    # size of all_results
    logger.info(f"size of all_results: {len(all_results)}")

    # 将数据分成多个批次
    batches = [all_results[i:i + BATCH_SIZE] for i in range(0, len(all_results), BATCH_SIZE)]

    for batch in batches:
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

        # 将数据插入数据库
        for rank, name in batch:
            cursor.execute(
                "INSERT INTO Player (name, region, mode) VALUES (%s, %s, %s)",
                (name, region, leaderboardId)
            )
            player_id = cursor.lastrowid
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前的日期和时间
            cursor.execute(
                "INSERT INTO Ranking (player_id, `rank`, timestamp, batch) VALUES (%s, %s, %s, %s)",
                (player_id, rank, now, new_batch)
            )

        # 提交事务
        db.commit()

        # 关闭连接
        cursor.close()
        db.close()

async def crawl_data():
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

    # 获取当前最大的batch number
    cursor.execute("SELECT MAX(batch) FROM Ranking")
    result = cursor.fetchone()
    max_batch = result[0] if result[0] is not None else 0
    new_batch = max_batch + 1
    
    # 提交事务
    db.commit()

    # 关闭连接
    cursor.close()
    db.close()
    
    await reqRankLev("EU", "standard", new_batch)
    await reqRankLev("EU", "wild", new_batch)

    await reqRankLev("US", "standard", new_batch)
    await reqRankLev("US", "wild", new_batch)

    await reqRankLev("AP", "standard", new_batch)
    await reqRankLev("AP", "wild", new_batch)

# 定义main函数
async def main():
    await crawl_data()

# 只有在脚本作为主程序运行时才执行main函数
if __name__ == "__main__":
    asyncio.run(main())