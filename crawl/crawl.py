import aiohttp
import json
import asyncio
import sys
import mysql.connector
from datetime import datetime

async def total_page(session, url):
    async with session.get(url) as response:
        info = await response.text()
        json_dict = json.loads(info)
        page_size = json_dict["leaderboard"]["pagination"]["totalPages"]

        return int(page_size)

async def fetch_page(session, url):
    async with session.get(url) as response:
        info = await response.text()
        json_dict = json.loads(info)
        rank_name = json_dict["leaderboard"]["rows"]
        page_results = []
        for item in rank_name:
            rank, name = item['rank'], item['accountid']
            page_results.append((rank, name))
        return page_results


async def reqRankLev(region: str, leaderboardId: str):
    all_results = []
    test_url = f"https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region={region}&leaderboardId={leaderboardId}&page=1"
    async with aiohttp.ClientSession() as session:
        page_size = await total_page(session, test_url)
        tasks = []
        for i in range(1, page_size + 1):
            html = f"https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region={region}&leaderboardId={leaderboardId}&page={i}"
            tasks.append(fetch_page(session, html))
        results = await asyncio.gather(*tasks)
        for page_results in results:
            all_results.extend(page_results)

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

    # 将数据插入数据库
    for rank, name in all_results:
        cursor.execute(
            "INSERT INTO Player (name, region, mode) VALUES (%s, %s, %s)",
            (name, region, leaderboardId)
        )
        player_id = cursor.lastrowid
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前的日期和时间
        cursor.execute(
            "INSERT INTO Ranking (player_id, `rank`, timestamp) VALUES (%s, %s, %s)",
            (player_id, rank, now)
        )

    # 提交事务
    db.commit()

    # 关闭连接
    cursor.close()
    db.close()

# 定义main函数
async def main():
    await crawl_data()

async def crawl_data():
    await reqRankLev("EU", "standard")
    await reqRankLev("EU", "wild")

    await reqRankLev("US", "standard")
    await reqRankLev("US", "wild")

    await reqRankLev("AP", "standard")
    await reqRankLev("AP", "wild")

# 运行main函数
asyncio.run(main())