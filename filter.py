import argparse
import logging.config
import yaml
from PIL import Image, ImageFilter, ImageFont, ImageDraw
import video
from temp import TemporaryDirectory, TemporaryFile


logger = logging.getLogger(__name__)


def resize_img(img, resize_ratio):
    """画像を指定の倍率に調節する"""
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


class ProgressRenderer(object):
    def __init__(self, base_img, settings):
        self.base_img = base_img
        self.settings = settings

    @staticmethod
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

    def render(self, progress):
        return self.render_progress(self.base_img, progress, self.settings)


def adjust_color_settings(settings):
    # yamlはtuple型に対応していないのでここで変換する
    r, g, b = settings['color']
    settings['color'] = r, g, b


def load_settings(fname):
    return yaml.load(open(fname).read())


def filter_image(orig_img, caption, settings_file, font_file):
    filtered_img = blur_img(orig_img)
    filtered_img = render_caption(filtered_img, caption, font_file)

    settings = load_settings(settings_file)
    adjust_color_settings(settings['progress'])

    blur_duration = settings['blur']['duration']
    num_blurred_frames = settings['blur']['frames']
    frame_duration = blur_duration / num_blurred_frames

    gif = Gif()
    progress_renderer = ProgressRenderer(filtered_img, settings['progress'])
    for i in range(num_blurred_frames):
        gif.append((progress_renderer.render(i / num_blurred_frames), frame_duration))
    # 視覚的にプログレスが終わるようにフレームを追加する
    gif.append((progress_renderer.render(1.0), 100))
    return gif


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('caption', type=str)
    parser.add_argument('in_file', type=str)
    parser.add_argument('out_file', type=str)
    parser.add_argument('--font_file', type=str, default='font.ttf')
    parser.add_argument('--settings_file', default='settings.yml')
    parser.add_argument('--resize_ratio', type=float, default=1.0,
                        help='gif化する前に画像をリサイズする時の比率(入力が動画の場合は無視される')
    parser.add_argument('--image_duration', type=int, default=60000,
                        help='元の画像が静止画として再生されるms単位の時間(入力が動画の場合は無視される)')
    return parser.parse_args()


def process_video(args):
    # `NamedTemporaryFile`はWindowsだとサブプロセスから開けないので自分で実装する必要がある
    # https://stackoverflow.com/questions/15169101/how-to-create-a-temporary-file-that-can-be-read-by-a-subprocess
    # サブルーチン内で一時ファイルを生成/削除するより
    # ここで全部生成して明確にレイヤー分けした方が小回りが利く気がする
    with TemporaryDirectory() as temp_dir, \
            TemporaryFile(temp_dir, 'png') as frame_path, \
            TemporaryFile(temp_dir, 'gif') as filtered_path, \
            TemporaryFile(temp_dir, 'mp4') as filtered_video_path:
        logger.info('temp_dir ' + temp_dir)
        logger.info('filtered_path ' + filtered_path)
        video.save_first_frame(args.in_file, frame_path)
        orig_img = Image.open(frame_path)
        gif = filter_image(orig_img, args.caption, args.settings_file, args.font_file)
        gif.save(filtered_path)
        video.convert_from_gif(filtered_path, filtered_video_path)
        video.merge(filtered_video_path, args.in_file, args.out_file)


def process_image(args):
    orig_img = Image.open(args.in_file)
    # 画像を動画化するとファイルの大きさが気になるので節約するためにリサイズ
    orig_img = resize_img(orig_img, args.resize_ratio)
    gif = filter_image(orig_img, args.caption, args.settings_file, args.font_file)
    # 元の画像は適当に長めの数字に設定する
    # 数字はファイルの大きさに影響しない
    gif.append((orig_img, args.image_duration))
    gif.save(args.out_file)


def main():
    args = parse_args()
    process_video(args) if video.is_video(args.in_file) else process_image(args)


def config_logging():
    logging.config.dictConfig(yaml.load(open('log.yml')))


if __name__ == '__main__':
    config_logging()
    main()
