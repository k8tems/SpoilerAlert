## ネタバレフィルター適用スクリプト
![](examples/output.gif)

### 必要なもの
- 適当なフォントの入った`font.ttf`

### 依存性のインストール
```
pip install -r requirements.txt
```

### 使用例
画像のフィルター  
```
filter.py \
    FFXVネタバレ \
    input.png \
    --out_file output.gif \
    --font_file font.ttf \
    --resize_ratio 0.25 \
    --settings_file settings.yml
```
動画のフィルター  
入力はmp4のみ対応  
出力もmp4形式必須  
```
filter.py \
    FFXVネタバレ \
    input.mp4 \
    --out_file output.mp4 \
    --font_file font.ttf \
    --resize_ratio 1 \
    --settings_file settings.yml
```

### TODO
- [x] 動画のフィルタリング
- [ ] ツイッターのメディアURLを渡したらフィルターを適用してメディアとしてアップロードし直す
