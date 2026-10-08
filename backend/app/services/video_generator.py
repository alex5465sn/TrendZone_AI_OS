"""
TrendZone AI OS — Gerador de vídeos de produto

Gera um vídeo curto (formato vertical, estilo Reels) a partir da
imagem do produto, com efeito de zoom e overlay de preço, desconto
e chamada para ação, pronto para publicar no Facebook/Instagram.
"""

import io
import uuid
from pathlib import Path

import imageio
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont

MEDIA_DIR = Path(__file__).resolve().parents[2] / "media" / "videos"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1080, 1920
FPS = 15
DURATION_SECONDS = 6
TOTAL_FRAMES = FPS * DURATION_SECONDS

BRAND_COLOR = (15, 23, 42)
ACCENT_COLOR = (16, 185, 129)
DISCOUNT_COLOR = (239, 68, 68)

THEMES = {
    "facebook": {
        "brand_color": (15, 23, 42),
        "accent_color": (16, 185, 129),
        "discount_color": (239, 68, 68),
        "hook": "🔥 OFERTA TRENDZONE",
        "duration_seconds": 6,
    },
    "shopee": {
        "brand_color": (238, 77, 45),
        "accent_color": (255, 255, 255),
        "discount_color": (255, 215, 0),
        "hook": "🛒 ACHADO SHOPEE",
        "duration_seconds": 10,
    },
}


class VideoGenerationError(Exception):
    pass


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _download_image(image_url: str) -> Image.Image:
    try:
        response = requests.get(image_url, timeout=15)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content)).convert("RGB")
    except Exception as exc:
        raise VideoGenerationError(f"Não foi possível baixar a imagem do produto: {exc}") from exc


def _fit_cover(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    src_ratio = img.width / img.height
    dst_ratio = target_w / target_h

    if src_ratio > dst_ratio:
        new_h = target_h
        new_w = int(new_h * src_ratio)
    else:
        new_w = target_w
        new_h = int(new_w / src_ratio)

    resized = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def _draw_text_center(draw: ImageDraw.ImageDraw, text: str, y: int, font, fill, max_width: int):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (WIDTH - text_w) / 2
    draw.text((x, y), text, font=font, fill=fill)


def generate_product_video(
    image_url: str,
    title: str,
    price: str,
    discount_rate: int | None = None,
    cta: str = "Compre agora - link na bio",
    theme: str = "facebook",
) -> Path:

    theme_cfg = THEMES.get(theme, THEMES["facebook"])
    brand_color = theme_cfg["brand_color"]
    accent_color = theme_cfg["accent_color"]
    discount_color = theme_cfg["discount_color"]
    hook_text = theme_cfg["hook"]
    total_frames = FPS * theme_cfg["duration_seconds"]

    photo_area_h = 1300
    base_photo = _fit_cover(_download_image(image_url), WIDTH, photo_area_h)

    short_title = title if len(title) <= 60 else title[:57] + "..."

    font_hook = _load_font(64, bold=True)
    font_price = _load_font(84, bold=True)
    font_cta = _load_font(48, bold=True)
    font_discount = _load_font(56, bold=True)

    output_path = MEDIA_DIR / f"{uuid.uuid4().hex}.mp4"
    writer = imageio.get_writer(str(output_path), fps=FPS, codec="libx264", quality=8)

    try:
        for i in range(total_frames):
            progress = i / max(total_frames - 1, 1)
            zoom = 1.0 + 0.18 * progress

            zoomed_w = int(WIDTH * zoom)
            zoomed_h = int(photo_area_h * zoom)
            zoomed = base_photo.resize((zoomed_w, zoomed_h), Image.LANCZOS)
            left = (zoomed_w - WIDTH) // 2
            top = (zoomed_h - photo_area_h) // 2
            photo_frame = zoomed.crop((left, top, left + WIDTH, top + photo_area_h))

            canvas = Image.new("RGB", (WIDTH, HEIGHT), brand_color)
            canvas.paste(photo_frame, (0, 0))

            draw = ImageDraw.Draw(canvas)

            draw.rectangle([0, 0, WIDTH, 130], fill=(0, 0, 0))
            _draw_text_center(draw, hook_text, 35, font_hook, (255, 255, 255), WIDTH - 80)

            bottom_y = photo_area_h
            draw.rectangle([0, bottom_y, WIDTH, HEIGHT], fill=brand_color)

            _draw_text_center(draw, short_title, bottom_y + 30, font_cta, (255, 255, 255), WIDTH - 80)

            price_text = f"R$ {price}"
            _draw_text_center(draw, price_text, bottom_y + 140, font_price, accent_color, WIDTH - 80)

            if discount_rate:
                _draw_text_center(
                    draw, f"{discount_rate}% OFF", bottom_y + 250, font_discount, discount_color, WIDTH - 80
                )

            _draw_text_center(draw, cta, HEIGHT - 90, font_cta, (255, 255, 255), WIDTH - 80)

            writer.append_data(np.array(canvas))
    finally:
        writer.close()

    return output_path
