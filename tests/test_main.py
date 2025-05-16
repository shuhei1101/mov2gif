"""
main モジュールのテスト
"""

import unittest
from unittest.mock import patch, MagicMock

from mov2gif.main import main
from mov2gif.app_logger import AppLogger
from mov2gif.config_reader import ConfigReader
from mov2gif.file_selector import FileSelector
from mov2gif.movie_converter import MovieConverter


class TestMain(unittest.TestCase):
    """mainモジュールのテスト"""

    @patch("mov2gif.main.AppLogger")
    @patch("mov2gif.main.ConfigReader")
    @patch("mov2gif.main.FileSelector")
    @patch("mov2gif.main.MovieConverter")
    def test_main_with_config_paths(
        self,
        mock_movie_converter_cls,
        mock_file_selector_cls,
        mock_config_reader_cls,
        mock_app_logger_cls,
    ):
        """正常系: 設定ファイルからパスが読み込める場合"""
        # モックの設定
        mock_logger = MagicMock(spec=AppLogger)
        mock_app_logger_cls.return_value = mock_logger

        mock_config_reader = MagicMock(spec=ConfigReader)
        mock_config_reader_cls.return_value = mock_config_reader
        mock_config_reader.read_config.return_value = [
            "/path/to/movie1.mov",
            "/path/to/movie2.mov",
        ]

        mock_movie_converter = MagicMock(spec=MovieConverter)
        mock_movie_converter_cls.return_value = mock_movie_converter
        mock_movie_converter.batch_convert.return_value = {
            "/path/to/movie1.mov": True,
            "/path/to/movie2.mov": True,
        }

        # テスト対象メソッド呼び出し
        main()

        # 検証
        mock_config_reader.read_config.assert_called_once()
        mock_movie_converter.batch_convert.assert_called_once_with(
            ["/path/to/movie1.mov", "/path/to/movie2.mov"]
        )
        mock_logger.info.assert_any_call("mov2gif - MOV動画をGIFに変換")
        mock_logger.info.assert_any_call(
            "設定ファイルから2個のファイルパスを読み込みました"
        )
        mock_logger.info.assert_any_call("✅ 変換成功: /path/to/movie1.mov")
        mock_logger.info.assert_any_call("✅ 変換成功: /path/to/movie2.mov")

    @patch("mov2gif.main.AppLogger")
    @patch("mov2gif.main.ConfigReader")
    @patch("mov2gif.main.FileSelector")
    @patch("mov2gif.main.MovieConverter")
    def test_main_without_config_paths(
        self,
        mock_movie_converter_cls,
        mock_file_selector_cls,
        mock_config_reader_cls,
        mock_app_logger_cls,
    ):
        """正常系: 設定ファイルにパスがない場合、ダイアログが表示される"""
        # モックの設定
        mock_logger = MagicMock(spec=AppLogger)
        mock_app_logger_cls.return_value = mock_logger

        mock_config_reader = MagicMock(spec=ConfigReader)
        mock_config_reader_cls.return_value = mock_config_reader
        mock_config_reader.read_config.return_value = []  # 空のリストを返す

        mock_file_selector = MagicMock(spec=FileSelector)
        mock_file_selector_cls.return_value = mock_file_selector
        mock_file_selector.show_dialog.return_value = "/path/to/selected/movie.mov"

        mock_movie_converter = MagicMock(spec=MovieConverter)
        mock_movie_converter_cls.return_value = mock_movie_converter
        mock_movie_converter.mov_to_gif.return_value = True

        # テスト対象メソッド呼び出し
        main()

        # 検証
        mock_config_reader.read_config.assert_called_once()
        mock_file_selector.show_dialog.assert_called_once()
        mock_movie_converter.mov_to_gif.assert_called_once_with(
            "/path/to/selected/movie.mov"
        )
        mock_logger.info.assert_any_call(
            "設定ファイルに動画パスが設定されていないため、ファイル選択ダイアログを表示します"
        )
        mock_logger.info.assert_any_call(
            "✅ 変換成功: /path/to/selected/movie.mov -> /path/to/selected/movie.gif"
        )

    @patch("mov2gif.main.AppLogger")
    @patch("mov2gif.main.ConfigReader")
    @patch("mov2gif.main.FileSelector")
    @patch("mov2gif.main.MovieConverter")
    def test_main_dialog_cancelled(
        self,
        mock_movie_converter_cls,
        mock_file_selector_cls,
        mock_config_reader_cls,
        mock_app_logger_cls,
    ):
        """異常系: ダイアログでキャンセルされた場合"""
        # モックの設定
        mock_logger = MagicMock(spec=AppLogger)
        mock_app_logger_cls.return_value = mock_logger

        mock_config_reader = MagicMock(spec=ConfigReader)
        mock_config_reader_cls.return_value = mock_config_reader
        mock_config_reader.read_config.return_value = []

        mock_file_selector = MagicMock(spec=FileSelector)
        mock_file_selector_cls.return_value = mock_file_selector
        mock_file_selector.show_dialog.return_value = ""  # ユーザーがキャンセル

        mock_movie_converter = MagicMock(spec=MovieConverter)
        mock_movie_converter_cls.return_value = mock_movie_converter

        # テスト対象メソッド呼び出し
        main()

        # 検証 - 変換メソッドは呼ばれないこと
        mock_config_reader.read_config.assert_called_once()
        mock_file_selector.show_dialog.assert_called_once()
        mock_movie_converter.mov_to_gif.assert_not_called()
        mock_logger.info.assert_any_call("ファイル選択がキャンセルされました")
        mock_logger.info.assert_any_call("変換処理を完了しました")


if __name__ == "__main__":
    unittest.main()
