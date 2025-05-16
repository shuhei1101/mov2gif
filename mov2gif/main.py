"""
アプリケーションのメインクラスとエントリーポイント
"""

import os

from mov2gif.app_logger import AppLogger
from mov2gif.config_reader import ConfigReader
from mov2gif.file_selector import FileSelector
from mov2gif.movie_converter import MovieConverter


def main():
    """アプリケーションのメイン処理を実行する

    1. 設定ファイルから動画パスを読み込み
    2. パスがない場合はファイル選択ダイアログを表示
    3. 動画をGIFに変換
    4. 結果を表示
    """
    logger = AppLogger()
    logger.info("mov2gif - MOV動画をGIFに変換")

    config_reader = ConfigReader(logger)
    file_selector = FileSelector(logger)
    movie_converter = MovieConverter(logger)

    # 設定ファイルから動画パスのリストを取得
    file_paths = config_reader.read_config()

    if file_paths:
        # パスが設定されている場合は一括変換
        logger.info(
            f"設定ファイルから{len(file_paths)}個のファイルパスを読み込みました"
        )
        results = movie_converter.batch_convert(file_paths)

        # 結果表示
        for path, success in results.items():
            if success:
                logger.info(f"✅ 変換成功: {path}")
            else:
                logger.error(f"❌ 変換失敗: {path}")
    else:
        # パスが設定されていない場合はファイル選択ダイアログを表示
        logger.info(
            "設定ファイルに動画パスが設定されていないため、ファイル選択ダイアログを表示します"
        )
        file_path = file_selector.show_dialog()

        if file_path:
            # ファイルが選択された場合は変換
            success = movie_converter.convert_to_gif(file_path)

            # 結果表示
            if success:
                output_path = os.path.splitext(file_path)[0] + ".gif"
                logger.info(f"✅ 変換成功: {file_path} -> {output_path}")
            else:
                logger.error(f"❌ 変換失敗: {file_path}")
        else:
            logger.info("ファイル選択がキャンセルされました")
        logger.info("変換処理を完了しました")


if __name__ == "__main__":
    main()
