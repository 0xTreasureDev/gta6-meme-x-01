#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme from the generated diptych artwork.

Takes the two-panel illustration (a 2013 teen gamer over his 2026 dad self,
baby in one arm, controller in the other), mounts make.fun's real ghost mark
(press kit mark-1024.png) over the neon ring sign on the living-room wall,
and stamps the two caption lines in classic meme lettering.

Usage: python3 make_meme.py <base-image> <mark-png> <out-png>
Deterministic: same inputs, same bytes out.
"""

import sys

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

TOP_CAPTION = "2013: \u201cGTA 6 WILL BE OUT BY COLLEGE\u201d"
BOTTOM_CAPTION = "2026: \u201cTHE BABY CAN WAIT. DADDY WAITED 13 YEARS.\u201d"

# Where the neon ring sign hangs in the base art, as fractions of the canvas,
# and the badge diameter as a fraction of the canvas width.
BADGE_CENTER = (0.863, 0.645)
BADGE_DIAMETER = 0.207


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int) -> ImageFont.FreeTypeFont:
    size = 96
    while size > 20:
        font = ImageFont.truetype(FONT_PATH, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(FONT_PATH, size)


def caption_band(base: Image.Image, text: str, at_top: bool) -> None:
    w, h = base.size
    band_h = int(h * 0.105)
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    y0 = 0 if at_top else h - band_h
    od.rectangle([0, y0, w, y0 + band_h], fill=(0, 0, 0, 168))
    base.paste(Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB"), (0, 0))

    draw = ImageDraw.Draw(base)
    font = fit_font(draw, text, int(w * 0.94))
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=3)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (w - tw) // 2 - bbox[0]
    y = y0 + (band_h - th) // 2 - bbox[1]
    draw.text((x, y), text, font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))


def main() -> None:
    base_path, mark_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    base = Image.open(base_path).convert("RGB")
    w, h = base.size

    mark = Image.open(mark_path).convert("RGBA")
    d = int(w * BADGE_DIAMETER)
    mark = mark.resize((d, d), Image.LANCZOS)
    cx, cy = int(w * BADGE_CENTER[0]), int(h * BADGE_CENTER[1])
    base.paste(mark, (cx - d // 2, cy - d // 2), mark)

    caption_band(base, TOP_CAPTION, at_top=True)
    caption_band(base, BOTTOM_CAPTION, at_top=False)

    base.save(out_path, format="PNG")
    print(f"wrote {out_path} ({w}x{h})")


if __name__ == "__main__":
    main()
