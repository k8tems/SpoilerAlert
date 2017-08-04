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
    out_file = 'out.mp4'
    cmd = 'python filter.py ' \
          'FFXVネタバレ ' \
          'test.mp4 ' \
          '--out_file %s ' \
          '--font_file font.ttf ' \
          '--resize_ratio %s ' \
          '--settings_file custom.yml' % (out_file, 1)
    output = check_output(cmd, shell=True).decode()
    print(output)
    print('ファイルサイズ:', serialize_file_size(os.path.getsize(out_file)))
