FROM python:3.9-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 确保必要的目录存在
RUN mkdir -p temp fonts templates

# 预先生成证书模板
RUN python templates/certificate_template.py

# 设置环境变量
ENV PORT=8080

# 暴露端口
EXPOSE ${PORT}

# 启动命令
CMD exec gunicorn --bind :${PORT} --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 main:app 