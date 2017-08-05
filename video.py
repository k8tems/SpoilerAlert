from subprocess import check_output


def run_ffmpeg(cmd):
    check_output('bin/ffmpeg -y %s' % cmd)


def get_first_frame(src, dest):
    run_ffmpeg('-i "%s" -vf "select=eq(n\\,0)" -q:v 3 "%s"' % (src, dest))


def is_video(file):
    return file.endswith('mp4')


def convert_from_gif(src, dest1, dest2):
    run_ffmpeg('-f gif -i "%s" "%s"' % (src, dest1))
    # Decoding will fail for this command if input and output file is the same
    run_ffmpeg('-i "%s" -f lavfi -i aevalsrc=0 -shortest -y "%s"' % (dest1, dest2))


def merge_videos(src1, src2, dest):
    run_ffmpeg('-i "%s" -i "%s" -filter_complex "[0:0][0:1][1:0][1:1] concat=n=2:v=1:a=1" "%s"' % (src1, src2, dest))
