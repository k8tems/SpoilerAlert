import os
import tempfile
import argparse
import logging.config
import yaml
from PIL import Image, ImageFilter, ImageFont, ImageDraw
import video

logger = logging.getLogger(__name__)


def resize_img(img, resize_ratio):
    """
    画像を指定の倍率に調節する
    画像を動画化するとファイルの大きさが気になるので節約用
    """
    img_width, img_height = img.size
    return img.resize((int(img_width * resize_ratio), int(img_height * resize_ratio)))


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
    """与えられた画像をぼかす"""
    return orig_img.filter(ImageFilter.GaussianBlur(radius=40))


def get_text_pos(img_size, text_size):
    """
    文字列のレンダリングする位置を返す
    x座標は文字列が画像の中央、
    y座標は画像の上半分中央に来るように調節する
    """
    img_width, img_height = img_size
    img_center_x = img_width / 2
    # 文字列は画像の上半分にレンダリングする
    img_center_y = img_height * 1 / 4
    text_width, text_height = text_size
    text_x = img_center_x - text_width / 2
    text_y = img_center_y - text_height / 2
    return text_x, text_y


def find_fitting_font(font_file, recommended_size, caption):
    """
    総当りで`recommended_size`内に入るフォントサイズを探した後、
    該当フォントを返す
    """
    recommended_width, recommended_height = recommended_size
    for i in range(1, 500):
        font = ImageFont.truetype(font_file, size=i)
        if font.getsize(caption)[0] > recommended_width or \
                        font.getsize(caption)[1] > recommended_height:
            return font
    assert ()


def render_caption(img, caption, font_file):
    """画像の上半分に文字列をレンダリングする"""
    font = find_fitting_font(font_file, (img.size[0] / 2, img.size[1] / 2), caption)
    draw = ImageDraw.Draw(img)
    draw.text(get_text_pos(img.size, font.getsize(caption)), caption, font=font)
    return img


def render_progress(img, progress, settings):
    """
    画像の下半分に左右から減っていくプログレスバーをレンダリングする
    `progress`が0.0の場合最も長く、
    `progress`が1.0の場合最も短い
    """
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
    return yaml.load(open(fname).read())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('caption', type=str)
    parser.add_argument('in_file', type=str)
    parser.add_argument('--out_file', type=str, default='out.gif')
    parser.add_argument('--font_file', type=str, default='font.ttf')
    parser.add_argument('--resize_ratio', type=float, default=1.0)
    parser.add_argument('--settings_file', default='settings.yml')
    return parser.parse_args()


def filter_image(orig_img, caption, resize_ratio, settings_file, font_file):
    orig_img = resize_img(orig_img, resize_ratio)

    filtered_img = blur_img(orig_img)
    filtered_img = render_caption(filtered_img, caption, font_file)

    settings = load_settings(settings_file)
    adjust_color_settings(settings['progress'])

    blur_duration = settings['blur']['duration']
    blurred_frames = settings['blur']['frames']

    gif = Gif()
    for i in range(blurred_frames):
        progress = i / blurred_frames
        gif.append((render_progress(filtered_img, progress, settings['progress']), blur_duration / blurred_frames))
    # 視覚的にプログレスが終わるようにフレームを追加する
    gif.append((render_progress(filtered_img, 1.0, settings['progress']), 100))
    # 元の画像は適当に長めの数字に設定する
    # 数字はファイルの大きさに影響しない
    gif.append((orig_img, settings['original']['duration']))
    return gif


class TemporaryDirectory(object):
    def __init__(self):
        self.dir = tempfile.mkdtemp()

    def __enter__(self):
        return self.dir

    def __exit__(self, *args, **kwargs):
        os.rmdir(self.dir)


class TemporaryFile(object):
    def __init__(self, temp_dir, fname):
        self.file = os.path.join(temp_dir, fname)

    def __enter__(self):
        return self.file

    def __exit__(self, *args, **kwargs):
        os.remove(self.file)


def main():
    args = parse_args()
    if video.is_video(args.in_file):
        # `NamedTemporaryFile`はWindowsだとサブプロセスから開けないので自分で実装する必要がある
        # https://stackoverflow.com/questions/15169101/how-to-create-a-temporary-file-that-can-be-read-by-a-subprocess
        with TemporaryDirectory() as temp_dir, \
                TemporaryFile(temp_dir, 'frame.png') as frame_path, \
                TemporaryFile(temp_dir, 'temp.gif') as gif_path, \
                TemporaryFile(temp_dir, 'temp1.mp4') as mp4_path_1, \
                TemporaryFile(temp_dir, 'temp2.mp4') as mp4_path_2:
            logger.info('temp_dir ' + temp_dir)
            logger.info('frame_path ' + frame_path)
            logger.info('mp4_path_1 ' + mp4_path_1)
            logger.info('mp4_path_2 ' + mp4_path_2)
            video.get_first_frame(args.in_file, frame_path)
            orig_img = Image.open(frame_path)
            gif = filter_image(orig_img, args.caption, args.resize_ratio, args.settings_file, args.font_file)
            gif.save(gif_path)
            video.gif_to_mp4(gif_path, mp4_path_1, mp4_path_2)
            video.merge_videos(mp4_path_2, args.in_file, args.out_file)
    else:
        orig_img = Image.open(args.in_file)
        gif = filter_image(orig_img, args.caption, args.resize_ratio, args.settings_file, args.font_file)
        gif.save(args.out_file)


if __name__ == '__main__':
    logging.config.dictConfig(yaml.load(open('log.yml')))
    main()
