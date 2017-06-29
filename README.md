## ネタバレフィルター適用スクリプト


### 必要なもの
- 入力画像
- 適当なフォントの入った`font.ttf`


### 依存性のインストール
```
pip install -r requirements.txt
```


### 使用例
```
filter.py \
    FFXVネタバレ \
    input.png \
    --out_file output.gif \
    --font_file font.ttf \
    --resize_ratio 0.25 \
    --settings_file settings.yml
```

### 出力
![](examples/output.gif)

### TODO
- [ ] ツイッターのメディアURLを渡したらフィルターを適用してメディアとしてアップロードし直す
- [ ] 動画のフィルタリング
