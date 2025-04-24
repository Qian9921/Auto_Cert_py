"""
生成示例证书模板
运行此脚本创建一个简单的证书模板图像
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_certificate_template():
    # 创建空白证书背景 (A4尺寸，横向)
    width, height = 842, 595  # A4尺寸 (72 DPI)
    background_color = (255, 255, 255)  # 白色背景
    
    # 创建图像
    image = Image.new('RGBA', (width, height), background_color)
    draw = ImageDraw.Draw(image)
    
    # 添加边框
    border_color = (0, 0, 128)  # 深蓝色
    border_width = 5
    draw.rectangle(
        [(border_width//2, border_width//2), 
         (width - border_width//2, height - border_width//2)],
        outline=border_color,
        width=border_width
    )
    
    # 添加装饰
    draw.rectangle(
        [(30, 30), (width - 30, height - 30)],
        outline=(0, 0, 100),
        width=1
    )
    
    # 添加标题
    title = "证书"
    try:
        # 尝试使用系统默认字体
        title_font = ImageFont.truetype("arial.ttf", 60)
    except:
        # 如果无法加载，使用默认字体
        title_font = ImageFont.load_default()
    
    # 获取文本大小以居中显示
    title_width = title_font.getbbox(title)[2]
    draw.text((width//2 - title_width//2, 50), title, fill=(0, 0, 128), font=title_font)
    
    # 保存模板
    template_path = os.path.join(os.path.dirname(__file__), "certificate_template.png")
    image.save(template_path)
    print(f"证书模板已保存至: {template_path}")
    return template_path

if __name__ == "__main__":
    create_certificate_template()