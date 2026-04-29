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

    # Subtle paper grain via alt-color band on right
    band = Image.new("RGB", (380, H), BG_ALT)
    img.paste(band, (W - 380, 0))

    # Vertical hairline separator between the two zones
    d.line([(W - 380, 60), (W - 380, H - 60)], fill=HAIRLINE, width=1)

    # ── Header row ────────────────────────────────────────
    f_label = font(F_SANS, 18)
    f_label_sm = font(F_SANS, 14)

    # Top-left: brand
    # Red dot
    d.ellipse([(80, 84), (92, 96)], fill=ACCENT_RED)
    draw_spaced(d, (104, 80), "PROPS LAB", f_label, TEXT_MAIN, spacing=4)

    # Top-right (in the alt band): issue tag
    issue_text = "ISSUE 001"
    place_text = "別府 大分 / BEPPU, OITA"
    fr = font(F_SANS, 13)
    fr_jp = font(F_SANS, 13)
    iw = text_w(d, issue_text, fr, spacing=3)
    pw = text_w(d, place_text, fr_jp, spacing=2)
    draw_spaced(d, (W - 80 - iw, 80), issue_text, fr, TEXT_SUB, spacing=3)
    draw_spaced(d, (W - 80 - pw, 104), place_text, fr_jp, TEXT_SUB, spacing=2)

    # ── Main headline (left zone) ────────────────────────
    f_h1 = font(F_SERIF, 72)
    headline_x = 80
    headline_y1 = 210

    # Line 1: "事業のITを、まるっと。" with red on "まるっと"
    parts1 = [
        ("事業のITを、", TEXT_MAIN),
        ("まるっと",   ACCENT_RED),
        ("。",         TEXT_MAIN),
    ]
    cx = headline_x
    for s, color in parts1:
        d.text((cx, headline_y1), s, font=f_h1, fill=color)
        cx += d.textlength(s, font=f_h1)

    # Line 2: subhead "別府発、月額の社外IT担当。"
    f_h2 = font(F_SERIF, 38)
    headline_y2 = headline_y1 + 110
    d.text((headline_x, headline_y2), "別府発、月額の社外IT担当。", font=f_h2, fill=TEXT_MAIN)

    # Short red accent rule under the headline group
    rule_y = headline_y2 + 70
    d.line([(headline_x, rule_y), (headline_x + 64, rule_y)], fill=ACCENT_RED, width=3)

    # Caption (sans)
    f_sub = font(F_SANS, 20)
    sub_y = rule_y + 24
    d.text((headline_x, sub_y), "IT担当者を雇うほどじゃない、でも誰かに頼みたい。", font=f_sub, fill=TEXT_MAIN)
    d.text((headline_x, sub_y + 30), "別府・大分の観光事業者と、ひとつの関係で長く伴走します。", font=f_sub, fill=TEXT_SUB)

    # ── Right zone (alt band) typography ──────────────────
    rzone_x = W - 380 + 50  # 870
    f_jp_label = font(F_SANS, 13)
    f_jp_pillar = font(F_SERIF, 32)
    f_jp_pillar_sm = font(F_SERIF, 18)

    # Vertical pillar: stacked Japanese typographic motif
    # "月額制" (vertical-feel by stacking)
    pillar_x = rzone_x + 40
    pillar_y = 200
    line_h = 44
    for i, ch in enumerate(["月", "額", "制", "", "の", "I", "T", "顧", "問"]):
        if not ch:
            pillar_y += line_h // 2
            continue
        # Use serif for Japanese, smaller for IT
        if ch in ("I", "T"):
            f = font(F_SERIF, 30)
            color = ACCENT_RED
        else:
            f = f_jp_pillar
            color = TEXT_MAIN
        bbox = d.textbbox((0, 0), ch, font=f)
        ch_w = bbox[2] - bbox[0]
        d.text((pillar_x - ch_w / 2, pillar_y), ch, font=f, fill=color)
        pillar_y += line_h

    # Right side small caption
    cap_x = rzone_x + 90
    cap_y = 220
    f_cap = font(F_SANS, 14)
    captions = [
        ("ADVISORY", ACCENT_RED),
        ("月額で伴走する", TEXT_MAIN),
        ("社外IT担当。", TEXT_MAIN),
        ("", TEXT_MAIN),
        ("ホームページ制作", TEXT_SUB),
        ("AI活用支援", TEXT_SUB),
        ("補助金活用サポート", TEXT_SUB),
    ]
    for s, color in captions:
        if s == "":
            cap_y += 16
            continue
        if color == ACCENT_RED:
            draw_spaced(d, (cap_x, cap_y), s, f_cap, color, spacing=3)
        else:
            d.text((cap_x, cap_y), s, font=f_cap, fill=color)
        cap_y += 26

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
