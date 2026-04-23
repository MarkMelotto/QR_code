import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from PIL import Image, ImageDraw, ImageFont
import sys
import os


def make_qr(
    url: str,
    caption: str = "",
    output_file: str = "QR_code.png",
    fg_color: tuple = (30, 30, 80),
    bg_color: tuple = (255, 255, 255),
    caption_color: tuple = (30, 30, 80),
):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=RadialGradiantColorMask(
            center_color=fg_color,
            edge_color=tuple(min(c + 60, 255) for c in fg_color),
            back_color=bg_color,
        ),
    ).convert("RGBA")

    qr_w, qr_h = qr_img.size
    padding = 24
    caption_area = 0

    try:
        font = ImageFont.truetype("arialbd.ttf", 42)
    except OSError:
        try:
            font = ImageFont.truetype("arial.ttf", 42)
        except OSError:
            font = ImageFont.load_default()

    if caption:
        dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        bbox = dummy.textbbox((0, 0), caption, font=font)
        caption_area = bbox[3] - bbox[1] + padding * 2

    canvas_w = qr_w + padding * 2
    canvas_h = qr_h + padding * 2 + caption_area

    # LinkedIn-tinted background (very faint blue-white)
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (*bg_color, 255))
    bg_draw = ImageDraw.Draw(canvas)
    bg_draw.rounded_rectangle(
        [0, 0, canvas_w, canvas_h], radius=20, fill=(*bg_color, 255)
    )

    # Drop shadow for the QR block (LinkedIn blue-tinted shadow)
    shadow = Image.new("RGBA", (qr_w + 12, qr_h + 12), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle([5, 5, qr_w + 12, qr_h + 12], fill=(0, 119, 181, 55))
    canvas.alpha_composite(shadow, dest=(padding - 3, padding - 3))
    canvas.alpha_composite(qr_img, dest=(padding, padding))

    # Bold LinkedIn-blue rounded border
    border_draw = ImageDraw.Draw(canvas)
    border_draw.rounded_rectangle(
        [padding - 8, padding - 8, padding + qr_w + 8, padding + qr_h + 8],
        radius=18,
        outline=(*fg_color, 220),
        width=5,
    )

    if caption:
        draw = ImageDraw.Draw(canvas)
        bbox = draw.textbbox((0, 0), caption, font=font)
        text_w = bbox[2] - bbox[0]
        text_x = (canvas_w - text_w) // 2
        text_y = padding + qr_h + padding

        draw.text((text_x, text_y), caption, font=font, fill=(*caption_color, 255))

    final = canvas.convert("RGB")
    final.save(output_file, quality=95)
    print(f"Saved: {output_file}  ({canvas_w}x{canvas_h}px)")


if __name__ == "__main__":
    # --- Edit these values ---
    URL = "https://www.linkedin.com/in/mark-melotto-393478144/"
    CAPTION = "LinkedIn"
    OUTPUT = "QR_code_v2.png"
    # LinkedIn brand blue foreground, clean white background
    FG = (0, 119, 181)   # #0077B5
    BG = (255, 255, 255)
    # -------------------------

    make_qr(URL, caption=CAPTION, output_file=OUTPUT, fg_color=FG, bg_color=BG)
