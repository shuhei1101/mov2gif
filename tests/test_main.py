"""
main モジュールのテスト
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from mov2gif.main import App


class TestApp(unittest.TestCase):
    """Appクラスのテスト"""

    def setUp(self):
        """テスト実行前の準備"""
        self.app = App()

    @patch("mov2gif.config_reader.ConfigReader.read_config")
    @patch("mov2gif.movie_converter.MovieConverter.batch_convert")
    def test_run_with_config_paths(self, mock_batch_convert, mock_read_config):
        """正常系: 設定ファイルからパスが読み込める場合"""
        # モックの設定
        mock_read_config.return_value = ["/path/to/movie1.mov", "/path/to/movie2.mov"]
        mock_batch_convert.return_value = {
            "/path/to/movie1.mov": True,
            "/path/to/movie2.mov": True,
        }

        # テスト対象メソッド呼び出し
        self.app.run()

        # 検証
        mock_read_config.assert_called_once()
        mock_batch_convert.assert_called_once_with(
            ["/path/to/movie1.mov", "/path/to/movie2.mov"]
        )

    @patch("mov2gif.config_reader.ConfigReader.read_config")
    @patch("mov2gif.file_selector.FileSelector.show_dialog")
    @patch("mov2gif.movie_converter.MovieConverter.convert_to_gif")
    def test_run_without_config_paths(
        self, mock_convert, mock_show_dialog, mock_read_config
    ):
        """正常系: 設定ファイルにパスがない場合、ダイアログが表示される"""
        # モックの設定
        mock_read_config.return_value = []  # 空のリストを返す
        mock_show_dialog.return_value = "/path/to/selected/movie.mov"
        mock_convert.return_value = True

        # テスト対象メソッド呼び出し
        self.app.run()

        # 検証
        mock_read_config.assert_called_once()
        mock_show_dialog.assert_called_once()
        mock_convert.assert_called_once_with("/path/to/selected/movie.mov")

    @patch("mov2gif.config_reader.ConfigReader.read_config")
    @patch("mov2gif.file_selector.FileSelector.show_dialog")
    @patch("mov2gif.movie_converter.MovieConverter.convert_to_gif")
    def test_run_dialog_cancelled(
        self, mock_convert, mock_show_dialog, mock_read_config
    ):
        """異常系: ダイアログでキャンセルされた場合"""
        # モックの設定
        mock_read_config.return_value = []
        mock_show_dialog.return_value = ""  # ユーザーがキャンセル

        # テスト対象メソッド呼び出し
        self.app.run()

        # 検証 - 変換メソッドは呼ばれないこと
        mock_read_config.assert_called_once()
        mock_show_dialog.assert_called_once()
        mock_convert.assert_not_called()

    @patch("builtins.print")
    @patch("mov2gif.main.App.run")
    def test_main(self, mock_run, mock_print):
        """正常系: mainメソッドの動作確認"""
        # テスト対象メソッド呼び出し
        self.app.main()

        # 検証
        mock_run.assert_called_once()
        # 開始/終了メッセージの出力確認
        self.assertEqual(mock_print.call_count, 2)


if __name__ == "__main__":
    unittest.main()
