import sys
from PIL import Image, ImageFilter


if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    img = Image.open(in_file)
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=40))
    img.save(out_file, save_all=True, duration=[5000,30000], append_images=[blurred_img])
