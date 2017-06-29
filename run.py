import os
import filter


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
    out_file = 'out.gif'
    filter.run('FFXVネタバレ', 'test.png', out_file, 'font.ttf', aspect_ratio=1/4)
    print('ファイルサイズ:', serialize_file_size(os.path.getsize(out_file)))
