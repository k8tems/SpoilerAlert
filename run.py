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
    in_file = 'video__in.mp4'
    out_file = 'video__out.mp4'
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
