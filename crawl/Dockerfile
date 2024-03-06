# 使用包含Conda的Python镜像作为基础镜像
FROM continuumio/miniconda3

# 将工作目录设置为/app
WORKDIR /app

# 复制crawl.py和environment.yml文件到容器的/app目录下
COPY crawl.py rule.py environment.yml /app/

# 使用Conda创建一个新的环境并安装environment.yml中指定的所有依赖
RUN conda env create -f environment.yml
RUN echo "source activate crawl" > ~/.bashrc
ENV PATH /opt/conda/envs/crawl/bin:$PATH

# 设置容器的默认命令为运行crawl.py
CMD ["conda", "run", "-n", "crawl", "python", "rule.py"]