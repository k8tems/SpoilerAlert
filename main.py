from PIL import Image, ImageFilter


if __name__ == '__main__':
    img = Image.open ('test.png')
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=40))
    img.save('out.gif', save_all=True, append_images=[blurred_img])
