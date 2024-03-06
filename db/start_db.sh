#!/bin/bash

# 启动Docker服务
docker-compose up -d

# 等待MySQL服务启动
echo "Waiting for MySQL to start..."
sleep 30

# 创建数据库表
echo "Creating tables..."
cat init.sql | docker exec -i $(docker-compose ps -q db) mysql -uroot -pHsbotDb