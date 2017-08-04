"""
テスト用スクリプト
視覚的にうまく言ってるか確認したい
"""

import os
from subprocess import check_output


def serialize_file_size(file_size):
    sizes = [
        (1000000000, 'GB'),
        (1000000, 'MB'),
        (10000, 'KB'),
    ]
    for s, t in sizes:
        if file_size > s:
            return '%f %s' % (file_size / s, t)


if __name__ == '__main__':
    output_path = os.path.join('output', 'video')
    in_file = os.path.join(output_path, 'in.mp4')
    out_file = os.path.join(output_path, 'out.mp4')
    cmd = 'python filter.py ' \
          'FFXVネタバレ ' \
          '%s ' \
          '--out_file %s ' \
          '--font_file font.ttf ' \
          '--resize_ratio %s ' \
          '--settings_file custom.yml' % (in_file, out_file, 1)
    output = check_output(cmd, shell=True).decode()
    print(output)
    print('ファイルサイズ:', serialize_file_size(os.path.getsize(out_file)))
