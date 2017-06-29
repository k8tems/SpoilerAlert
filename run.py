import os
import sys
import filter


if __name__ == '__main__':
    out_file = 'out.gif'
    filter.run('FFXVネタバレ', 'test.png', out_file, 'font.ttf')
    print('ファイルサイズ:', os.path.getsize(out_file))
