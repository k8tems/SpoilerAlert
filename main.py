import sys
from PIL import Image, ImageFilter, ImageFont, ImageDraw


def get_text_pos(img_size, font):
    return (10, 10)


if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    caption = 'FFXV'
    img = Image.open(in_file)
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=40))
    font = ImageFont.truetype("arial", size=100)
    draw = ImageDraw.Draw(blurred_img)
    draw.text(get_text_pos(img.size, font), caption, font=font)
    blurred_img.save(out_file, save_all=True, duration=[3000, 30000], append_images=[img])
    blurred_img.show()
