import argparse
import yaml
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
    # 文字列は画像の上半分にレンダリングする
    img_center_y = img_height * 1/4
    text_width, text_height = text_size
    text_x = img_center_x - text_width / 2
    text_y = img_center_y - text_height / 2
    return text_x, text_y


def find_fitting_font(font_file, recommended_size, caption):
    """総当りで`recommended_size`内に入るフォントサイズを探した後、該当フォントを返す"""
    recommended_width, recommended_height = recommended_size
    for i in range(1, 500):
        font = ImageFont.truetype(font_file, size=i)
        if font.getsize(caption)[0] > recommended_width or \
           font.getsize(caption)[1] > recommended_height:
            return font
    assert()


def render_caption(img, caption, font_file):
    """画像の上半分に文字列をレンダリングする"""
    font = find_fitting_font(font_file, (img.size[0] / 2, img.size[1] / 2), caption)
    draw = ImageDraw.Draw(img)
    draw.text(get_text_pos(img.size, font.getsize(caption)), caption, font=font)
    return img


def render_progress(img, progress, settings):
    """画像の下半分に左右から減っていくプログレスバーをレンダリングする"""
    img = img.copy()
    progress_y = img.height * settings['y_ratio']
    progress_x_margin = img.width * settings['x_initial_margin_ratio']
    progress_initial_length = img.width - progress_x_margin * 2
    progress_length = progress_initial_length * (1 - progress)
    progress_x = img.width / 2 - progress_length / 2
    crds = (progress_x, progress_y, progress_x + progress_length, progress_y)
    ImageDraw.Draw(img).line(crds, fill=settings['color'], width=3)
    return img


def adjust_color_settings(settings):
    # yamlはtuple型に対応していないのでここで変換する
    r, g, b = settings['color']
    settings['color'] = r, g, b


def load_settings(fname):
    return  yaml.load(open(fname).read())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('caption', type=str)
    parser.add_argument('in_file', type=str)
    parser.add_argument('--out_file', type=str, default='out.gif')
    parser.add_argument('--font_file', type=str, default='font.ttf')
    parser.add_argument('--aspect_ratio', type=float, default=1.0)
    parser.add_argument('--settings_file', default='settings.yml')
    return parser.parse_args()


def main():
    args = parse_args()
    orig_img = Image.open(args.in_file)
    orig_img = resize_img(orig_img, args.aspect_ratio)

    filtered_img = blur_img(orig_img)
    filtered_img = render_caption(filtered_img, args.caption, args.font_file)

    settings = load_settings(args.settings_file)
    adjust_color_settings(settings['progress'])

    blur_duration = settings['blur']['duration']
    blurred_frames = settings['blur']['frames']

    gif = Gif()
    for i in range(blurred_frames):
        progress = i / blurred_frames
        gif.append((render_progress(filtered_img, progress, settings['progress']), blur_duration / blurred_frames))
    # 視覚的にプログレスが終われるようにフレームを追加する
    gif.append((render_progress(filtered_img, 1.0, settings['progress']), 100))
    # 元の画像は適当に長めの数字に設定する
    # 数字はファイルの大きさに影響しない
    gif.append((orig_img, settings['original']['duration']))
    gif.save(args.out_file)


if __name__ == '__main__':
    main()
