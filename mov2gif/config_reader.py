"""
設定ファイルからmovファイルのパスリストを読み込むためのモジュール
"""

import os
import importlib.util
from typing import List

from mov2gif.app_logger import AppLogger


class ConfigReader:
    """
    config.pyファイルから設定を読み込むクラス
    """

    def __init__(self, logger: AppLogger):
        """
        ConfigReaderのコンストラクタ
        """
        self.default_config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config", "config.py"
        )
        self.logger = logger

    def read_config(self, config_path: str = "") -> List[str]:
        """
        設定ファイルから動画ファイルのパスリストを読み込む

        Args:
            config_path (str, optional): 設定ファイルのパス。デフォルトはNone (デフォルトの場所を使用)

        Returns:
            List[str]: 動画ファイルパスのリスト。エラー時や設定がない場合は空リストを返す
        """
        # パスが指定されていない場合はデフォルトパスを使用
        if config_path is None or config_path == "":
            config_path = self.default_config_path

        # 設定ファイルが存在するか確認
        if not os.path.exists(config_path):
            self.logger.warning(f"設定ファイルが見つかりません: {config_path}")
            return []

        try:
            # 動的にPythonモジュールを読み込む
            spec = importlib.util.spec_from_file_location("config", config_path)
            if spec is None or spec.loader is None:
                self.logger.error(
                    f"設定ファイルの読み込みに失敗しました: {config_path}"
                )
                return []

            config_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config_module)

            # MOV_FILE_PATHSキーが存在するか確認
            if not hasattr(config_module, "MOV_FILE_PATHS"):
                self.logger.warning("設定ファイルにMOV_FILE_PATHSが定義されていません")
                return []

            # パスのリストを取得
            file_paths = getattr(config_module, "MOV_FILE_PATHS")

            # リストであることを確認
            if not isinstance(file_paths, list):
                self.logger.error("MOV_FILE_PATHSはリスト形式である必要があります")
                return []

            return file_paths

        except Exception as e:
            self.logger.error(
                f"設定ファイルの読み込み中にエラーが発生しました: {str(e)}"
            )
            return []
