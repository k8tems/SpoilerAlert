from subprocess import check_output


def run_ffmpeg(cmd):
    check_output('bin/ffmpeg -y %s' % cmd)


def save_first_frame(src, dest):
    run_ffmpeg('-i "%s" -vf "select=eq(n\\,0)" -q:v 3 "%s"' % (src, dest))


def is_video(file):
    return file.endswith('mp4')


def add_dummy_audio(src, dest):
    """
    動画を結合する前に音声を追加する必要がある
    入力と出力ファイルが同じだと失敗する
    """
    run_ffmpeg('-i "%s" -f lavfi -i aevalsrc=0 -shortest -y "%s"' % (src, dest))


def convert_from_gif(gif_path, inaudible_video_path, audible_video_path):
    # ツイッターがピクセルフォーマットYUV4:2:0にのみ対応してる
    run_ffmpeg('-f gif -i "%s" -pix_fmt "yuv420p" "%s"' % (gif_path, inaudible_video_path))
    add_dummy_audio(inaudible_video_path, audible_video_path)


def merge(src1, src2, dest):
    run_ffmpeg('-i "%s" -i "%s" -filter_complex "[0:0][0:1][1:0][1:1] concat=n=2:v=1:a=1" "%s"' % (src1, src2, dest))
