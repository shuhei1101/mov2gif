# mov2gif 設定ファイル
# 変換対象の動画ファイルパスを記載
# 相対パスまたは絶対パスで指定可能
MOV_FILE_PATHS = [
    # ここに変換したい動画ファイルのパスを記載してください[MP4, MOV]
    # 例: "/Users/username/Movies/example.mov",
]

# 変換オプション
CONVERSION_OPTIONS = {
    "fps": 15,  # GIFのフレームレート
    "optimize": True,  # GIF最適化
    "quality": 80,  # 品質 (1-100)
}
