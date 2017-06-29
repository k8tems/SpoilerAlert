import sys
from PIL import Image, ImageFilter, ImageFont, ImageDraw


def get_text_pos(img_size, text_size):
    img_width, img_height = img_size
    img_center_x = img_width / 2
    img_center_y = img_height / 2
    text_width, text_height = text_size
    return img_center_x - text_width / 2, img_center_y - text_height / 2


if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    caption = sys.argv[3]
    img = Image.open(in_file)
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=40))
    font = ImageFont.truetype("font.ttf", size=100)
    draw = ImageDraw.Draw(blurred_img)
    draw.text(get_text_pos(img.size, font.getsize(caption)), caption, font=font)
    blurred_img.save(out_file, save_all=True, duration=[3000, 30000], append_images=[img])
