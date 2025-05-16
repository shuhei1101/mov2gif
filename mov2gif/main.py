"""
アプリケーションのメインクラスとエントリーポイント
"""

import logging
import os
import sys
from typing import List

from mov2gif.config_reader import ConfigReader
from mov2gif.file_selector import FileSelector
from mov2gif.movie_converter import MovieConverter

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class App:
    """
    mov2gifアプリケーションのメインクラス
    """

    def __init__(self):
        """
        Appのコンストラクタ
        """
        self.config_reader = ConfigReader()
        self.file_selector = FileSelector()
        self.movie_converter = MovieConverter()

    def run(self) -> None:
        """
        アプリケーションのメイン処理を実行する

        1. 設定ファイルから動画パスを読み込み
        2. パスがない場合はファイル選択ダイアログを表示
        3. 動画をGIFに変換
        4. 結果を表示
        """
        # 設定ファイルから動画パスのリストを取得
        file_paths = self.config_reader.read_config()

        if file_paths:
            # パスが設定されている場合は一括変換
            logger.info(
                f"設定ファイルから{len(file_paths)}個のファイルパスを読み込みました"
            )
            results = self.movie_converter.batch_convert(file_paths)

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
            file_path = self.file_selector.show_dialog()

            if file_path:
                # ファイルが選択された場合は変換
                success = self.movie_converter.convert_to_gif(file_path)

                # 結果表示
                if success:
                    output_path = os.path.splitext(file_path)[0] + ".gif"
                    logger.info(f"✅ 変換成功: {file_path} -> {output_path}")
                else:
                    logger.error(f"❌ 変換失敗: {file_path}")
            else:
                logger.info("ファイル選択がキャンセルされました")

    def main(self) -> None:
        """
        アプリケーションのエントリーポイント
        """
        print("mov2gif - MOV動画をGIFに変換")
        self.run()
        print("変換処理を完了しました")


# スクリプトとして直接実行された場合はmain()を呼び出す
if __name__ == "__main__":
    app = App()
    app.main()
