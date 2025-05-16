# mov2gif 設定ファイル例
# このファイルはプロジェクトのルートディレクトリに config.py として配置してください

# 変換対象の動画ファイルパスを記載
# 相対パスまたは絶対パスで指定可能
MOV_FILE_PATHS = [
    "/path/to/your/movie1.mov",
    "/path/to/your/movie2.mov",
    # 追加のファイルパスはここに記載
]

# 変換オプション (オプション)
CONVERSION_OPTIONS = {
    "fps": 15,  # GIFのフレームレート
    "optimize": True,  # GIF最適化
    "quality": 80,  # 品質 (1-100)
}
