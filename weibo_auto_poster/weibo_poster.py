from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple

def get_system_font() -> str:
    """获取系统中可用的中文字体"""
    # Windows 常用字体路径
    windows_fonts = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyh.ttf",
        "C:/Windows/Fonts/simsun.ttc"
    ]
    # macOS 常用字体路径
    mac_fonts = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/PingFang.ttc"
    ]
    
    for font_path in windows_fonts + mac_fonts:
        if os.path.exists(font_path):
            return font_path
    
    raise FileNotFoundError("未找到可用的中文字体")

def draw_rounded_rectangle(draw: ImageDraw, xy: Tuple[int, int, int, int], 
                         radius: int, fill: Tuple[int, int, int]):
    """绘制圆角矩形"""
    x1, y1, x2, y2 = xy
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill)
    draw.ellipse([x1, y1, x1+2*radius, y1+2*radius], fill=fill)
    draw.ellipse([x2-2*radius, y1, x2, y1+2*radius], fill=fill)
    draw.ellipse([x1, y2-2*radius, x1+2*radius, y2], fill=fill)
    draw.ellipse([x2-2*radius, y2-2*radius, x2, y2], fill=fill)

def create_image(filename: str, title: str, subtitle: str, 
                bg_color: Tuple[int, int, int] = (255, 255, 255),
                accent_color: Tuple[int, int, int] = (0, 120, 215)):
    """
    生成一张 450x300 的图片，包含标题、副标题和装饰元素
    :param filename: 输出文件名
    :param title: 主标题
    :param subtitle: 副标题
    :param bg_color: 背景颜色
    :param accent_color: 强调色
    """
    # 创建图像（注意宽高已调整为 450x300）
    img = Image.new("RGB", (450, 300), bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font_path = get_system_font()
        font_title = ImageFont.truetype(font_path, 32)
        font_subtitle = ImageFont.truetype(font_path, 20)
    except Exception as e:
        print(f"加载字体失败: {e}")
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()

    # 添加装饰元素
    draw_rounded_rectangle(draw, (30, 30, 420, 270), 20, 
                         tuple(max(0, c - 10) for c in bg_color))

    # 绘制标题装饰线
    line_y = 120
    draw.line([(100, line_y), (350, line_y)], fill=accent_color, width=2)

    # 计算并绘制标题
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (450 - title_w) // 2
    draw.text((title_x, 80), title, fill=(0, 0, 0), font=font_title)

    # 计算并绘制副标题
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
    subtitle_w = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (450 - subtitle_w) // 2
    draw.text((subtitle_x, 150), subtitle, fill=(80, 80, 80), font=font_subtitle)

    # 添加装饰图案
    for i in range(3):
        x = 150 + i * 75
        draw.ellipse([x, 220, x+10, 230], fill=accent_color)

    # 保存图片，确保文件大小在2M以内
    img.save(filename, optimize=True, quality=85)
    
    # 检查文件大小并在需要时压缩
    while os.path.getsize(filename) > 2 * 1024 * 1024:  # 2MB
        img_quality = 85
        img.save(filename, optimize=True, quality=img_quality-10)
        img_quality -= 10
        if img_quality < 30:
            break

    print(f"图片已生成: {filename}")

if __name__ == "__main__":
    # 生成三张不同风格的图片
    create_image(
        "fut_news_1.png",
        "FUT新闻速报",
        "实时获取FUT最新内容",
        bg_color=(230, 240, 255),
        accent_color=(0, 120, 215)
    )

    create_image(
        "fut_news_2.png",
        "粉丝互动更便捷",
        "提升微博粉丝粘性与活跃度",
        bg_color=(245, 245, 245),
        accent_color=(64, 158, 255)
    )

    create_image(
        "fut_news_3.png",
        "一键分享 快速传播",
        "轻松将FUT资讯分享至微博",
        bg_color=(255, 255, 240),
        accent_color=(255, 136, 0)
    ) 