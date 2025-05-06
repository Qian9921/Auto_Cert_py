import os
from pathlib import Path

# 项目基础路径
BASE_DIR = Path(__file__).resolve().parent

# 模板目录
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# 默认证书模板
DEFAULT_TEMPLATE = os.path.join(TEMPLATE_DIR, "1.png")

# 临时文件目录
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# 字体目录
FONT_DIR = os.path.join(BASE_DIR, "fonts")
os.makedirs(FONT_DIR, exist_ok=True)

# 尝试使用系统中可能存在的字体
system_fonts = [
    os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts\\simhei.ttf"),  # 黑体
    os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts\\simsun.ttc"),  # 宋体
    os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts\\msyh.ttf"),    # 微软雅黑
    os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts\\arial.ttf"),   # Arial
    os.path.join(FONT_DIR, "msyh.ttf"),  # 本地字体目录中的微软雅黑
]

# 默认字体 - 找到第一个存在的字体
DEFAULT_FONT = None
for font_path in system_fonts:
    if os.path.exists(font_path):
        DEFAULT_FONT = font_path
        break

# 如果没有找到字体，则使用None，程序会回退到使用默认字体
if DEFAULT_FONT is None:
    print("警告：未找到任何可用字体，将使用PIL默认字体")

# 证书字段位置配置 - 根据SVG坐标更新
CERTIFICATE_CONFIG = {
    # 学生姓名 - 主标题 (x="1004", y="660")
    "student_name": {
        "position": (1004, 555),
        "font_size": 100,
        "color": (139, 69, 19),  # #8B4513 (棕色)
        "align": "center",
        "font_style": "bold_italic"  # 粗斜体
    },
    # 学生姓名 - 文中使用 (x="1106", y="810")
    "student_name_text": {
        "position": (1106, 763),
        "font_size": 40,
        "color": (139, 69, 19),  # #8B4513 (棕色)
        "align": "center"
    },
    # NGO名称 (x="1337", y="1250")
    "ngo_name": {
        "position": (1337, 1170),
        "font_size": 70,
        "color": (0, 0, 0),  # 黑色
        "align": "center"
    },
    # 证书内容 (x="979", y="915")
    "contents": {
        "position": (979, 865),
        "font_size": 40,
        "color": (0, 0, 0),  # 黑色
        "align": "center",
        "max_width": 1400,  # 最大宽度，超过将自动换行
        "line_spacing": 15  # 行间距
    },
    # 日期 (x="1337", y="1190")
    "date": {
        "position": (1337, 1110),
        "font_size": 60,
        "color": (0, 0, 0),  # 黑色
        "align": "center"
    },
    # NGO签名 (x="689", y="1200")
    "ngo_signature": {
        "position": (689, 1135),
        "font_size": 60,
        "color": (0, 0, 0),  # 黑色
        "align": "center",
        "max_size": (300, 150),  # 最大尺寸 (宽度, 高度)
        "font_style": "italic"  # 斜体
    }
}

# API设置
API_SETTINGS = {
    "allowed_origins": ["*"],  # 允许的CORS来源
    "max_upload_size": 10 * 1024 * 1024,  # 最大上传文件大小（10MB）
} 