"""
Props Lab OGP image generator.
Outputs assets/ogp.jpg at 1200x630.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "ogp.jpg"

W, H = 1200, 630

# Brand palette (from site)
BG          = (245, 241, 232)   # #F5F1E8
BG_ALT      = (236, 230, 216)   # #ECE6D8
TEXT_MAIN   = (61, 40, 23)      # #3D2817
TEXT_SUB    = (122, 115, 104)   # #7A7368
ACCENT_RED  = (184, 69, 47)     # #B8452F
HAIRLINE    = (210, 200, 184)   # ~ rgba(61,40,23,0.15) on cream

FONTS = "C:/Windows/Fonts"
F_SERIF   = f"{FONTS}/NotoSerifJP-VF.ttf"
F_SANS    = f"{FONTS}/NotoSansJP-VF.ttf"
F_MINCHO  = f"{FONTS}/yumindb.ttf"  # Yu Mincho Demibold fallback


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f, spacing=0):
    if spacing == 0:
        return draw.textlength(s, font=f)
    # manual letter spacing
    total = 0
    for i, ch in enumerate(s):
        total += draw.textlength(ch, font=f)
        if i < len(s) - 1:
            total += spacing
    return total


def draw_spaced(draw, xy, s, f, fill, spacing):
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + spacing


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ── Header row ────────────────────────────────────────
    f_label = font(F_SANS, 18)

    # Top-left: brand with red dot
    d.ellipse([(80, 84), (92, 96)], fill=ACCENT_RED)
    draw_spaced(d, (104, 80), "PROPS LAB", f_label, TEXT_MAIN, spacing=4)

    # Top-right: issue tag (on cream)
    issue_text = "ISSUE 001"
    place_text = "別府 大分 / BEPPU, OITA"
    fr = font(F_SANS, 13)
    fr_jp = font(F_SANS, 13)
    iw = text_w(d, issue_text, fr, spacing=3)
    pw = text_w(d, place_text, fr_jp, spacing=2)
    draw_spaced(d, (W - 80 - iw, 80), issue_text, fr, TEXT_SUB, spacing=3)
    draw_spaced(d, (W - 80 - pw, 104), place_text, fr_jp, TEXT_SUB, spacing=2)

    # ── Main headline (left zone) ────────────────────────
    f_h1 = font(F_SERIF, 80)
    headline_x = 80
    headline_y1 = 240

    # Big headline: "別府発、月額の社外IT担当" with red on "社外IT担当"
    parts = [
        ("別府発、月額の", TEXT_MAIN),
        ("社外IT担当",   ACCENT_RED),
    ]
    cx = headline_x
    for s, color in parts:
        d.text((cx, headline_y1), s, font=f_h1, fill=color)
        cx += d.textlength(s, font=f_h1)

    # Short red accent rule under the headline
    rule_y = headline_y1 + 130
    d.line([(headline_x, rule_y), (headline_x + 64, rule_y)], fill=ACCENT_RED, width=3)

    # Sub (痛点)
    f_sub = font(F_SERIF, 34)
    sub_y = rule_y + 32
    d.text((headline_x, sub_y), "IT担当を雇うほどじゃない、でも頼みたい", font=f_sub, fill=TEXT_MAIN)

    # ── Footer row ────────────────────────────────────────
    f_foot = font(F_SANS, 14)
    f_foot_jp = font(F_SERIF, 17)

    # Bottom-left: era + founded
    d.text((80, H - 71), "令和八年　創業", font=f_foot_jp, fill=TEXT_SUB)

    # Bottom-right (in alt band): URL
    url = "props-lab.com"
    uw = text_w(d, url, f_foot, spacing=2)
    draw_spaced(d, (W - 80 - uw, H - 68), url, f_foot, TEXT_MAIN, spacing=2)

    # Faint bottom hairline across full width
    d.line([(80, H - 90), (W - 80, H - 90)], fill=HAIRLINE, width=1)

    img.save(OUT, "JPEG", quality=92, optimize=True)
    print(f"wrote {OUT}  ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
