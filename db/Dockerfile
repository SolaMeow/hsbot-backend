# 使用官方的MySQL镜像作为基础镜像
FROM mysql:latest

# 将init.sql文件复制到/docker-entrypoint-initdb.d目录下
COPY init.sql /docker-entrypoint-initdb.d/
