"""
テスト用スクリプト
視覚的にうまく言ってるか確認したい
"""

import os
from subprocess import check_output, CalledProcessError


def serialize_file_size(file_size):
    sizes = [
        (1000000000, 'GB'),
        (1000000, 'MB'),
        (10000, 'KB'),
    ]
    for s, t in sizes:
        if file_size > s:
            return '%f %s' % (file_size / s, t)


def run_command(cmd):
    try:
        print(check_output(cmd, shell=True).decode())
    except CalledProcessError as e:
        print(e.output)
        raise


def run_image():
    output_path = os.path.join('output', 'image')
    in_file = os.path.join(output_path, 'in.png')
    out_file = os.path.join(output_path, 'out.gif')
    cmd = 'python filter.py ' \
        'DQ11ネタバレ ' \
        '%s ' \
        '%s ' \
        '--font_file font.ttf ' \
        '--resize_ratio %s ' \
        '--image_duration 60000 ' \
        '--settings_file custom.yml' % (in_file, out_file, 1)
    run_command(cmd)
    print('ファイルサイズ:', serialize_file_size(os.path.getsize(out_file)))


def run_video():
    output_path = os.path.join('output', 'video')
    in_file = os.path.join(output_path, 'in.mp4')
    out_file = os.path.join(output_path, 'out.mp4')
    cmd = 'python filter.py ' \
        'DQ11ネタバレ ' \
        '%s ' \
        '%s ' \
        '--font_file font.ttf ' \
        '--settings_file custom.yml' % (in_file, out_file)
    run_command(cmd)
    print('ファイルサイズ:', serialize_file_size(os.path.getsize(out_file)))


if __name__ == '__main__':
    run_image()
    run_video()
