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


def encode_to_browser_format(src, dest):
    run_ffmpeg('-i %s -s hd720 -vcodec libx264 -vcodec libx264 -pix_fmt yuv420p '
               '-preset slow -profile:v baseline -movflags faststart %s' % (src, dest))


def encode_to_ts(src, dest):
    """h264/aac形式の動画をts形式に変換する"""
    run_ffmpeg('-i %s -c copy -bsf:v h264_mp4toannexb -f mpegts %s' % (src, dest))


def merge_ts(src1, src2, dest):
    run_ffmpeg('-i "concat:%s|%s" '
               '-c copy -bsf:a aac_adtstoasc %s' % (src1, src2, dest))


def merge2(src1, src2, ts1, ts2, dest1, dest2):
    """
    `-filter_complex`でやると元動画がモッサリして、
    `concat demux`でやると元の動画がスローになってしまう
    ts形式として結合するとシームレスに動くけどブラウザで再生出来ないので、
    最後にブラウザが理解出来る形式に再エンコードする
    """
    encode_to_ts(src1, ts1)
    encode_to_ts(src2, ts2)
    merge_ts(ts1, ts2, dest1)
    encode_to_browser_format(dest1, dest2)


if __name__ == '__main__':
    output_path = 'output/quality_ts'
    merge2(output_path + '/audible.mp4',
           output_path + '/in.mp4',
           output_path + '/intermediate1.ts',
           output_path + '/intermediate2.ts',
           output_path + '/out.mp4',
           output_path + '/out2.mp4')
