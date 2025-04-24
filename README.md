# 证书生成服务

这是一个用Python实现的证书生成服务，可以接收来自FlutterFlow的POST请求，根据提供的信息在证书模板上生成个性化证书。

## 功能特点

- 基于FastAPI构建的REST API
- 支持在证书模板上添加文本和图片
- 可自定义字体、颜色、位置等属性
- 支持签名图片URL或文本
- 生成PDF格式的证书
- 针对Google Cloud Run优化部署

## 快速开始 (Windows)

### 自动设置（推荐）

1. 双击运行 `setup.cmd` 脚本
   - 此脚本会自动安装所有依赖
   - 生成证书模板

2. 运行 `start_service.cmd` 启动服务
   - 服务将在 http://localhost:8000 运行

3. 访问 http://localhost:8000/docs 查看API文档

### 手动设置

1. 确保安装了Python 3.9或更高版本
   ```
   py -3.9 --version
   ```

2. 安装依赖
   ```
   py -3.9 -m pip install -r requirements.txt
   ```

3. 生成证书模板
   ```
   py -3.9 templates/certificate_template.py
   ```

4. 启动服务
   ```
   py -3.9 -m uvicorn main:app --reload
   ```

## Docker部署

1. 构建Docker镜像
   ```
   docker build -t certificate-service .
   ```

2. 运行容器
   ```
   docker run -p 8080:8080 certificate-service
   ```

## 部署到Google Cloud Run

1. 构建Docker镜像并推送到Google Container Registry
   ```
   gcloud builds submit --tag gcr.io/[PROJECT_ID]/certificate-service
   ```

2. 部署到Cloud Run
   ```
   gcloud run deploy certificate-service --image gcr.io/[PROJECT_ID]/certificate-service --platform managed
   ```

## API接口

### 生成证书

**端点**: `/generate-certificate`

**方法**: POST

**请求体**:
```json
{
  "studentName": "学生姓名",
  "ngoSignature": "签名URL或文本",
  "ngoName": "组织名称",
  "contents": "证书内容",
  "date": "颁发日期"
}
```

**响应**: 生成的证书文件(PDF)

## 自定义

### 证书模板

替换 `templates/certificate_template.png` 文件以使用自定义模板。

### 布局配置

在 `config.py` 文件中修改 `CERTIFICATE_CONFIG` 字典可以自定义各元素的位置和样式。

### 字体

系统会自动检测Windows系统中可用的中文字体。如需使用特定字体，请将字体文件放在 `fonts` 目录下，并在 `config.py` 中更新 `DEFAULT_FONT` 路径。

## 常见问题

### 字体问题

如果没有合适的中文字体，会使用PIL默认字体，这可能导致中文显示为方块。解决方法：
1. 将中文字体（如微软雅黑msyh.ttf）复制到fonts目录
2. 或在config.py中指定系统中已有的字体路径

### 临时文件

生成的证书会临时存储在 `temp` 目录中。在Cloud Run环境中，这些文件会在实例重启后删除。

## FlutterFlow集成

在FlutterFlow中，可以使用HTTP请求部件向此服务发送POST请求。确保将所有必需的字段包含在请求体中。

```dart
// FlutterFlow HTTP请求示例代码
final response = await HttpClient().post(
  'https://your-service-url/generate-certificate',
  body: {
    'studentName': studentName,
    'ngoSignature': ngoSignature,
    'ngoName': ngoName,
    'contents': contents,
    'date': date,
  },
);
```

## 系统要求

- Python 3.9或更高版本
- Windows、MacOS或Linux操作系统

## 许可证

MIT 