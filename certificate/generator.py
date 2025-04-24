import os
import uuid
import requests
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple, Dict, Any

import config

def download_image(url: str) -> Image.Image:
    """从URL下载图片"""
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"无法下载图片，HTTP状态码: {response.status_code}")
    return Image.open(BytesIO(response.content))

def get_text_dimensions(text: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
    """计算文本尺寸"""
    ascent, descent = font.getmetrics()
    width = font.getmask(text).getbbox()[2]
    height = ascent + descent
    return width, height

def draw_text_aligned(
    draw: ImageDraw.ImageDraw,
    position: Tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: Tuple[int, int, int],
    align: str = "left"
) -> None:
    """绘制对齐的文本"""
    x, y = position
    width, height = get_text_dimensions(text, font)
    
    if align == "center":
        x -= width // 2
    elif align == "right":
        x -= width
    
    draw.text((x, y), text, font=font, fill=fill)

def draw_multiline_text(
    draw: ImageDraw.ImageDraw,
    position: Tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: Tuple[int, int, int],
    align: str = "left",
    max_width: int = None,
    line_spacing: int = 0
) -> None:
    """绘制多行文本，支持自动换行"""
    if not max_width:
        # 如果没有指定最大宽度，直接绘制
        draw_text_aligned(draw, position, text, font, fill, align)
        return
    
    x, y = position
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        # 尝试添加单词到当前行
        test_line = " ".join(current_line + [word])
        width, _ = get_text_dimensions(test_line, font)
        
        if width <= max_width:
            current_line.append(word)
        else:
            # 如果添加单词后超过最大宽度，保存当前行并开始新行
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                # 如果单词本身就超过最大宽度，直接添加
                lines.append(word)
    
    # 添加最后一行
    if current_line:
        lines.append(" ".join(current_line))
    
    # 绘制所有行
    _, line_height = get_text_dimensions("A", font)
    for i, line in enumerate(lines):
        line_y = y + i * (line_height + line_spacing)
        draw_text_aligned(draw, (x, line_y), line, font, fill, align)

def generate_certificate(
    student_name: str,
    ngo_name: str,
    contents: str,
    date: str,
    ngo_signature: Optional[str] = None,
    template_path: str = None
) -> str:
    """生成证书并返回文件路径
    
    Args:
        student_name: 学生姓名
        ngo_name: 组织名称
        contents: 证书内容
        date: 颁发日期
        ngo_signature: 签名图片URL或文本
        template_path: 自定义模板路径
        
    Returns:
        str: 生成的证书文件路径
    """
    # 使用默认模板或自定义模板
    template_path = template_path or config.DEFAULT_TEMPLATE
    
    # 检查模板是否存在
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板文件不存在: {template_path}")
    
    # 加载模板
    template = Image.open(template_path)
    draw = ImageDraw.Draw(template)
    
    # 尝试加载默认字体，如果不存在则使用默认
    try:
        font_path = config.DEFAULT_FONT
        if not os.path.exists(font_path):
            # 如果配置的字体不存在，使用PIL默认字体
            print(f"警告：字体文件不存在 {font_path}，将使用默认字体")
            font_path = None
    except Exception as e:
        print(f"加载字体出错: {e}")
        font_path = None
    
    # 处理学生姓名 - 主标题
    student_config = config.CERTIFICATE_CONFIG["student_name"]
    student_font_size = student_config.get("font_size", 40)
    student_font = ImageFont.truetype(font_path, size=student_font_size) if font_path else ImageFont.load_default()
    draw_text_aligned(
        draw,
        student_config["position"],
        student_name,
        student_font,
        student_config["color"],
        student_config["align"]
    )
    
    # 处理学生姓名 - 文中使用 (如果配置中存在)
    if "student_name_text" in config.CERTIFICATE_CONFIG:
        student_text_config = config.CERTIFICATE_CONFIG["student_name_text"]
        student_text_font_size = student_text_config.get("font_size", 40)
        student_text_font = ImageFont.truetype(font_path, size=student_text_font_size) if font_path else ImageFont.load_default()
        draw_text_aligned(
            draw,
            student_text_config["position"],
            student_name,
            student_text_font,
            student_text_config["color"],
            student_text_config["align"]
        )
    
    # 处理NGO名称
    ngo_config = config.CERTIFICATE_CONFIG["ngo_name"]
    ngo_font_size = ngo_config.get("font_size", 30)
    ngo_font = ImageFont.truetype(font_path, size=ngo_font_size) if font_path else ImageFont.load_default()
    draw_text_aligned(
        draw,
        ngo_config["position"],
        ngo_name,
        ngo_font,
        ngo_config["color"],
        ngo_config["align"]
    )
    
    # 处理证书内容
    contents_config = config.CERTIFICATE_CONFIG["contents"]
    contents_font_size = contents_config.get("font_size", 24)
    contents_font = ImageFont.truetype(font_path, size=contents_font_size) if font_path else ImageFont.load_default()
    draw_multiline_text(
        draw,
        contents_config["position"],
        contents,
        contents_font,
        contents_config["color"],
        contents_config["align"],
        contents_config.get("max_width"),
        contents_config.get("line_spacing", 0)
    )
    
    # 处理日期
    date_config = config.CERTIFICATE_CONFIG["date"]
    date_font_size = date_config.get("font_size", 20)
    date_font = ImageFont.truetype(font_path, size=date_font_size) if font_path else ImageFont.load_default()
    draw_text_aligned(
        draw,
        date_config["position"],
        date,
        date_font,
        date_config["color"],
        date_config["align"]
    )
    
    # 处理签名（如果提供）
    if ngo_signature:
        signature_config = config.CERTIFICATE_CONFIG["ngo_signature"]
        try:
            # 尝试判断是否为URL
            if ngo_signature.startswith(('http://', 'https://')):
                # 下载签名图片
                signature_img = download_image(ngo_signature)
                
                # 调整签名尺寸
                max_width, max_height = signature_config["max_size"]
                width, height = signature_img.size
                
                # 保持宽高比
                if width > max_width:
                    ratio = max_width / width
                    width = max_width
                    height = int(height * ratio)
                
                if height > max_height:
                    ratio = max_height / height
                    height = max_height
                    width = int(width * ratio)
                
                signature_img = signature_img.resize((width, height), Image.LANCZOS)
                
                # 计算粘贴位置
                sig_x, sig_y = signature_config["position"]
                if signature_config["align"] == "center":
                    sig_x -= width // 2
                elif signature_config["align"] == "right":
                    sig_x -= width
                
                # 粘贴签名
                template.paste(signature_img, (sig_x, sig_y), signature_img if signature_img.mode == 'RGBA' else None)
            else:
                # 如果不是URL，假设是文本签名
                signature_font_size = signature_config.get("font_size", 30)
                signature_font = ImageFont.truetype(font_path, size=signature_font_size) if font_path else ImageFont.load_default()
                draw_text_aligned(
                    draw,
                    signature_config["position"],
                    ngo_signature,
                    signature_font,
                    signature_config.get("color", (0, 0, 0)),
                    signature_config["align"]
                )
        except Exception as e:
            print(f"处理签名时出错: {e}")
    
    # 生成唯一文件名
    unique_id = uuid.uuid4().hex
    output_filename = f"certificate_{unique_id}.pdf"
    output_path = os.path.join(config.TEMP_DIR, output_filename)
    
    # 保存为PDF
    template.convert('RGB').save(output_path, "PDF", resolution=100.0)
    
    return output_path 