from subprocess import check_output


def run_ffmpeg(cmd):
    check_output('bin\\ffmpeg %s' % cmd)


def get_first_frame(src, dest):
    run_ffmpeg('-i "%s" -vf "select=eq(n\\,0)" -q:v 3 "%s"' % (src, dest))


def is_video(file):
    return file.endswith('mp4')


def gif_to_mp4(src, dest):
    run_ffmpeg('-i "%s" -f lavfi -i aevalsrc=0 -shortest -y "%s"' % (src, dest))


def merge_videos(vid1, vid2):
    ff = ffmpy.FFmpeg(
        inputs={'"concat:%s|%s"' % (vid1, vid2): None},
        outputs={'output.mp4': '-c copy -bsf:a aac_adtstoasc'}
    )
    ff.run()


if __name__ == '__main__':
    gif_to_mp4('mp4_out.gif', 'out.mp4')
