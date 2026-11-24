"""4:3 homepage thumbnail for the Nature paper: a tournament photo of Ace filling the frame, with the
issue's cover inset at the top right, over the backdrop lettering and clear of robot, ball and player.

Inputs (downloaded 2026-11-24):
  cover  https://media.springernature.com/full/springer-static/cover-hires/journal/41586/652/8111
         (Nature 652, issue 8111, 23 April 2026; 827 x 1098, the native size)
  photo  https://ai.sony/hubfs/SonyAI_Ace_Tournament_DSC04362.jpg (Sony AI blog; 6871 x 4581)

Usage: python3 tools/make_nature_thumb.py COVER.png PHOTO.jpg images/pub-nature.jpg
"""
import sys

from PIL import Image, ImageDraw, ImageFilter

W, H = 1200, 900
COVER_H, MARGIN, BORDER = 420, 40, 4


def main(cover_path, photo_path, out):
    cover = Image.open(cover_path).convert("RGB")
    photo = Image.open(photo_path).convert("RGB")
    # 3:2 photo to 4:3 by trimming the left edge only (the player's back), keeping the robot whole.
    w = photo.height * 4 // 3
    frame = photo.crop((photo.width - w, 0, photo.width, photo.height)).resize((W, H), Image.LANCZOS)

    c = cover.resize((round(cover.width * COVER_H / cover.height), COVER_H), Image.LANCZOS)
    card = Image.new("RGB", (c.width + 2 * BORDER, c.height + 2 * BORDER), "white")
    card.paste(c, (BORDER, BORDER))
    x, y = W - card.width - MARGIN, MARGIN - 6

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle((x + 8, y + 8, x + 8 + card.width, y + 8 + card.height), fill=(0, 0, 0, 150))
    img = frame.convert("RGBA")
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16)))
    img = img.convert("RGB")
    img.paste(card, (x, y))
    img.save(out, quality=88)


if __name__ == "__main__":
    main(*sys.argv[1:4])
