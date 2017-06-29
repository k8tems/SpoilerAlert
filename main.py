import sys
from PIL import Image, ImageFilter, ImageFont, ImageDraw


if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    caption = 'FFXV'
    img = Image.open(in_file)
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=40))
    font = ImageFont.truetype("arial")
    draw = ImageDraw.Draw(blurred_img)
    draw.text((10, 10), caption, font=font)
    blurred_img.save(out_file, save_all=True, duration=[3000, 30000], append_images=[img])
