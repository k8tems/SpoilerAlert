from PIL import Image, ImageFilter, ImageFont, ImageDraw


def resize_img(img, aspect_ratio):
    img_width, img_height = img.size
    return img.resize((int(img_width * aspect_ratio), int(img_height * aspect_ratio)))


class Gif(list):
    @property
    def append_images(self):
        return [img for img, duration in self[1:]]

    @property
    def duration(self):
        return [duration for img, duration in self]

    @property
    def first_img(self):
        return self[0][0]

    def save(self, fname):
        self.first_img.save(fname, save_all=True, duration=self.duration, append_images=self.append_images)


def blur_img(orig_img):
    return orig_img.filter(ImageFilter.GaussianBlur(radius=40))


def get_text_pos(img_size, text_size):
    img_width, img_height = img_size
    img_center_x = img_width / 2
    img_center_y = img_height / 2
    text_width, text_height = text_size
    return img_center_x - text_width / 2, img_center_y - text_height / 2


def find_fitting_font(font_file, recommended_size, caption):
    recommended_width, recommended_height = recommended_size
    for i in range(1, 500):
        font = ImageFont.truetype(font_file, size=i)
        if font.getsize(caption)[0] > recommended_width or \
           font.getsize(caption)[1] > recommended_height:
            return font
    assert()


def draw_caption(img, caption, font_file):
    font = find_fitting_font(font_file, (img.size[0] / 2, img.size[1] / 2), caption)
    draw = ImageDraw.Draw(img)
    draw.text(get_text_pos(img.size, font.getsize(caption)), caption, font=font)
    return img


def run(caption, in_file, out_file, font_file, aspect_ratio=1.0):
    orig_img = Image.open(in_file)
    orig_img = resize_img(orig_img, aspect_ratio)

    filtered_img = blur_img(orig_img)
    filtered_img = draw_caption(filtered_img, caption, font_file)

    blur_duration = 2000
    blurred_frames = 10

    gif = Gif()
    gif += [(filtered_img, blur_duration / blurred_frames)] * blurred_frames
    gif.append((orig_img, 30000))
    gif.save(out_file)
