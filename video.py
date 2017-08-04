from subprocess import check_output


def get_first_frame(in_file, out_file):
    cmd = 'bin\\ffmpeg -i %s -vf "select=eq(n\\,0)" -q:v 3 %s' % (in_file, out_file)
    check_output(cmd)


def is_video(file):
    return 'mp4' in av.open(file).format.name


def gif_to_mp4(src, dest):
    ff = ffmpy.FFmpeg(
        inputs={src: None},
        outputs={dest: None},
    )
    ff.run()


def merge_videos(vid1, vid2):
    ff = ffmpy.FFmpeg(
        inputs={'"concat:%s|%s"' % (vid1, vid2): None},
        outputs={'output.mp4': '-c copy -bsf:a aac_adtstoasc'}
    )
    ff.run()


if __name__ == '__main__':
    get_first_frame('test.mp4', 'frame.png')
