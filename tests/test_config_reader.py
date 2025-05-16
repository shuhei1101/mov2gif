"""
config_reader モジュールのテスト
"""

import unittest
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

from mov2gif.config_reader import ConfigReader
from mov2gif.app_logger import AppLogger


class TestConfigReader(unittest.TestCase):
    """ConfigReaderクラスのテスト"""

    def setUp(self):
        """テスト実行前の準備"""
        self.mock_logger = MagicMock(spec=AppLogger)
        self.config_reader = ConfigReader(self.mock_logger)
        # 一時ファイルを作成するためのテンポラリディレクトリ
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """テスト実行後のクリーンアップ"""
        self.temp_dir.cleanup()

    def test_read_config_normal(self):
        """正常系: 有効な設定ファイルを読み込めることを確認"""
        # テスト用の一時設定ファイル作成
        test_config_path = Path(self.temp_dir.name) / "config.py"
        with open(test_config_path, "w") as f:
            f.write("MOV_FILE_PATHS = [\n")
            f.write('    "/path/to/movie1.mov",\n')
            f.write('    "/path/to/movie2.mov"\n')
            f.write("]\n")

        # テスト対象メソッド呼び出し
        file_paths = self.config_reader.read_config(str(test_config_path))

        # 検証
        self.assertEqual(len(file_paths), 2)
        self.assertEqual(file_paths[0], "/path/to/movie1.mov")
        self.assertEqual(file_paths[1], "/path/to/movie2.mov")

    def test_read_config_empty_list(self):
        """正常系: 空のリストが設定されている場合"""
        # テスト用の一時設定ファイル作成（空のリスト）
        test_config_path = Path(self.temp_dir.name) / "config.py"
        with open(test_config_path, "w") as f:
            f.write("MOV_FILE_PATHS = []\n")

        # テスト対象メソッド呼び出し
        file_paths = self.config_reader.read_config(str(test_config_path))

        # 検証
        self.assertEqual(len(file_paths), 0)
        self.assertEqual(file_paths, [])

    def test_read_config_file_not_found(self):
        """異常系: 設定ファイルが存在しない場合"""
        # 存在しないファイルパス
        non_existent_path = Path(self.temp_dir.name) / "non_existent_config.py"

        # テスト対象メソッド呼び出し
        file_paths = self.config_reader.read_config(str(non_existent_path))

        # 検証 - ファイルが存在しなくても空のリストを返すこと
        self.assertEqual(len(file_paths), 0)
        self.assertEqual(file_paths, [])

        # ロガーが呼び出されたことを確認
        self.mock_logger.warning.assert_called_once()

    def test_read_config_invalid_format(self):
        """異常系: 設定ファイルのフォーマットが不正な場合"""
        # テスト用の一時設定ファイル作成（不正なフォーマット）
        test_config_path = Path(self.temp_dir.name) / "invalid_config.py"
        with open(test_config_path, "w") as f:
            f.write("# 不正なフォーマット\n")
            f.write('INVALID_FORMAT = "This is not valid"\n')

        # テスト対象メソッド呼び出し
        file_paths = self.config_reader.read_config(str(test_config_path))

        # 検証 - フォーマットが不正でも空のリストを返すこと
        self.assertEqual(len(file_paths), 0)
        self.assertEqual(file_paths, [])

        # ロガーが呼び出されたことを確認
        self.mock_logger.warning.assert_called_once()


if __name__ == "__main__":
    unittest.main()
