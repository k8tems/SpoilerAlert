import sys
from PIL import Image, ImageFilter, ImageFont, ImageDraw


def get_text_pos(img_size, font):
    img_width, img_height = img_size
    img_center_x = img_width / 2
    img_center_y = img_height / 2
    return (img_center_x, img_center_y)


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
