from subprocess import check_output
import logging
from temp import TemporaryDirectory, TemporaryFile, StandaloneTemporaryFile


logger = logging.getLogger(__name__)


def run_ffmpeg(cmd):
    logger.info('executing ' + cmd)
    check_output('bin/ffmpeg -y %s' % cmd)


def save_first_frame(src, dest):
    """動画の最初のフレームを画像として保存する"""
    run_ffmpeg('-i "%s" -vf "select=eq(n\\,0)" -q:v 3 "%s"' % (src, dest))


def is_video(file):
    return file.endswith('mp4')


def add_dummy_audio(src, dest):
    """
    動画を結合する前に音声を追加する必要がある
    入力と出力ファイルが同じだと失敗する
    """
    run_ffmpeg('-i "%s" -f lavfi -i aevalsrc=0 -shortest -y "%s"' % (src, dest))


def convert_from_gif(gif_path, audible_video_path):
    """
    gifをmp4に変換する
    標準のピクセルフォーマットYUV4:4:4にツイッターが対応してないのでYUV4:2:0でエンコードする
    """
    with StandaloneTemporaryFile('mp4') as inaudible_video_path:
        run_ffmpeg('-f gif -i "%s" -pix_fmt "yuv420p" "%s"' % (gif_path, inaudible_video_path))
        add_dummy_audio(inaudible_video_path, audible_video_path)


def encode_to_browser_format(src, dest):
    """動画をブラウザが理解出来る形式に再エンコードする"""
    run_ffmpeg('-i %s -s hd720 -vcodec libx264 -vcodec libx264 -pix_fmt yuv420p '
               '-preset slow -profile:v baseline -movflags faststart %s' % (src, dest))


def encode_to_ts(src, dest):
    """h264/aac形式の動画をts形式に変換する"""
    run_ffmpeg('-i %s -c copy -bsf:v h264_mp4toannexb -f mpegts %s' % (src, dest))


def merge_ts(src1, src2, dest):
    """ts形式の動画を結合する"""
    run_ffmpeg('-i "concat:%s|%s" '
               '-c copy -bsf:a aac_adtstoasc %s' % (src1, src2, dest))


def merge(src1, src2, dest):
    """
    `-filter_complex`でやると元動画がモッサリして、
    `concat demux`でやると元の動画がスローになってしまう
    ts形式として結合するとシームレスに動くけどブラウザで再生出来ないので、
    最後にブラウザが理解出来る形式に再エンコードする
    """
    with TemporaryDirectory() as temp_dir, \
            TemporaryFile(temp_dir, 'ts') as ts1, \
            TemporaryFile(temp_dir, 'ts') as ts2, \
            TemporaryFile(temp_dir, 'mp4') as merged_ts:
        encode_to_ts(src1, ts1)
        encode_to_ts(src2, ts2)
        merge_ts(ts1, ts2, merged_ts)
        encode_to_browser_format(merged_ts, dest)
