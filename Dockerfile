FROM python:3.9-slim

# 安装必要的依赖和中文字体
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    fonts-dejavu \
    fontconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 更新字体缓存
RUN fc-cache -fv

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 确保必要的目录存在
RUN mkdir -p temp fonts templates

# 复制自定义字体到fonts目录（如果有的话）
# COPY custom_fonts/ fonts/

# 将项目附带的示例字体复制到fonts目录
# COPY templates/fonts/* fonts/

# 预先生成证书模板
#RUN python templates/certificate_template.py

# 列出当前可用的字体，用于调试
RUN echo "Available fonts:" && fc-list | grep -i chinese || echo "No Chinese fonts found"
RUN echo "Fonts directory contents:" && ls -la /app/fonts || echo "Fonts directory not found or empty"

# 设置环境变量
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV DEBUG_FONT=1

# 暴露端口
EXPOSE ${PORT}

# 启动命令
CMD exec gunicorn --bind :${PORT} --workers 1 --worker-class uvicorn.workers.UvicornWorker --threads 8 main:app 