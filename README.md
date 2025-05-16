# mov2gif

MOV形式の動画ファイルをGIF形式のアニメーションに変換するシンプルなツールです。

## 機能

- config.pyに指定した複数のMOVファイルを一括でGIFに変換
- ファイル選択ダイアログを使用した単一ファイル変換
- 変換オプションのカスタマイズ

## インストール方法

1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/mov2gif.git
cd mov2gif
```

2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

3. 開発用インストール

```bash
pip install -e .
```

## 使用方法

### 方法1: 設定ファイルに変換対象のファイルパスを指定する場合

1. `mov2gif/config/config.py` ファイルを編集し、変換したいMOVファイルのパスを記載します。

```python
MOV_FILE_PATHS = [
    "/path/to/your/movie1.mov",
    "/path/to/your/movie2.mov",
    # 追加のファイルパスはここに記載
]
```

2. 以下のコマンドでプログラムを実行します。

```bash
python -m mov2gif.main
```

### 方法2: ファイル選択ダイアログを使用する場合

1. `config.py` にファイルパスを指定せずに、以下のコマンドでプログラムを実行します。

```bash
python -m mov2gif.main
```

2. 表示されるダイアログから変換したいMOVファイルを選択します。

## テスト実行方法

```bash
python -m unittest discover tests
```

## ライセンス

[MIT License](LICENSE)