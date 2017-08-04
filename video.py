from subprocess import check_output


def run_ffmpeg(cmd):
    check_output('bin\\ffmpeg %s' % cmd)


def get_first_frame(src, dest):
    run_ffmpeg('-i "%s" -vf "select=eq(n\\,0)" -q:v 3 "%s"' % (src, dest))


def is_video(file):
    return file.endswith('mp4')


def gif_to_mp4(src, dest):
    run_ffmpeg('-i "%s" -f lavfi -i aevalsrc=0 -shortest -y "%s"' % (src, dest))


def merge_videos(src1, src2, dest):
    run_ffmpeg('-i "%s" -i "%s" -filter_complex "[0:0][0:1][1:0][1:1] concat=n=2:v=1:a=1" "%s"' % (src1, src2, dest))


if __name__ == '__main__':
    gif_to_mp4('mp4_out.gif', 'out.mp4')
