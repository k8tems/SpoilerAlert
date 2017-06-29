@echo off
python main.py FFXVネタバレ test.png out.gif font.ttf
Set fs=python get_file_size.py out.gif
echo %fs%
