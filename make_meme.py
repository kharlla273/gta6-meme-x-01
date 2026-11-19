#!/usr/bin/env python3
"""Build the GTA 6 meme for the gta6-meme-x-01 bounty.

The joke: thirteen years of waiting for GTA 6, while an AI agent is
already earning real money on make.fun. The picture is a Vice City
sunset scene — neon sky, palm trees, a pink 80s sports car, and a
fluffy white ghost in sunglasses leaning on it.

This script takes the base scene (assets/base.webp) and the real
make.fun ghost badge (assets/ghost-icon.png), draws the two-line
headline across the empty sky, and stamps the make.fun badge in the
bottom-left corner. Output is meme.png in the repository root — the
picture posted on X.

Usage: python3 make_meme.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

HEADLINE_LINES = [
    "WAITED 12 YEARS FOR GTA 6",
    "MY AI AGENT GOT PAID ALREADY",
]
WORDMARK = "make.fun"

FONT_CANDIDATES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
)


def bold_font(size: int) -> ImageFont.FreeTypeFont:
    """DejaVu Sans Bold at the requested size, falling back to default."""
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_centered(draw: ImageDraw.ImageDraw, y: int, text: str,
                  font: ImageFont.FreeTypeFont, width: int) -> None:
    """Draw one line of white text with a black outline, centered."""
    stroke = max(3, font.size // 9)
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (width - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=font, fill="white",
              stroke_width=stroke, stroke_fill="black")


def round_badge(icon: Image.Image, diameter: int) -> Image.Image:
    """Crop the ghost icon to a circle with a transparent surround."""
    icon = icon.resize((diameter, diameter), Image.LANCZOS)
    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter, diameter), fill=255)
    badge = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    badge.paste(icon.convert("RGBA"), (0, 0), mask)
    return badge


def build_meme() -> Image.Image:
    scene = Image.open(ASSETS / "base.webp").convert("RGB")
    width, height = scene.size
    draw = ImageDraw.Draw(scene)

    # Headline: two lines across the empty sky at the top.
    head_size = round(height * 0.058)
    head_font = bold_font(head_size)
    for index, line in enumerate(HEADLINE_LINES):
        y = round(height * (0.038 + index * 0.080))
        draw_centered(draw, y, line, head_font, width)

    # Badge: the real make.fun ghost, bottom-left, with the wordmark.
    badge_size = round(height * 0.085)
    badge = round_badge(
        Image.open(ASSETS / "ghost-icon.png").convert("RGB"), badge_size)
    badge_x = round(width * 0.018)
    badge_y = height - badge_size - round(height * 0.025)
    scene.paste(badge, (badge_x, badge_y), badge)

    mark_font = bold_font(round(height * 0.042))
    mark_y = badge_y + badge_size // 2 - round(height * 0.021)
    draw.text((badge_x + badge_size + 12, mark_y), WORDMARK,
              font=mark_font, fill="white",
              stroke_width=max(3, round(height * 0.004)),
              stroke_fill="black")
    return scene


def main() -> None:
    meme = build_meme()
    out = HERE / "meme.png"
    meme.save(out)
    print(f"wrote {out} ({meme.size[0]}x{meme.size[1]})")


if __name__ == "__main__":
    main()
