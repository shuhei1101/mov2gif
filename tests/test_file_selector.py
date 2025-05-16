"""
file_selector モジュールのテスト
"""

import unittest
import sys
import os
import tkinter as tk
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from mov2gif.file_selector import FileSelector


class TestFileSelector(unittest.TestCase):
    """FileSelectorクラスのテスト"""

    def setUp(self):
        """テスト実行前の準備"""
        self.file_selector = FileSelector()

    @patch("tkinter.filedialog.askopenfilename")
    def test_show_dialog_file_selected(self, mock_askopenfilename):
        """正常系: ユーザーがファイルを選択した場合"""
        # モックの戻り値設定
        expected_path = "/path/to/selected/movie.mov"
        mock_askopenfilename.return_value = expected_path

        # テスト対象メソッド呼び出し
        result = self.file_selector.show_dialog()

        # 検証
        self.assertEqual(result, expected_path)
        mock_askopenfilename.assert_called_once()

        # filetypes引数が正しく設定されていることを確認
        args, kwargs = mock_askopenfilename.call_args
        self.assertIn("filetypes", kwargs)
        self.assertTrue(any("mov" in ft[1].lower() for ft in kwargs["filetypes"]))

    @patch("tkinter.filedialog.askopenfilename")
    def test_show_dialog_cancelled(self, mock_askopenfilename):
        """異常系: ユーザーがキャンセルした場合"""
        # モックの戻り値設定（キャンセル時は空文字を返す）
        mock_askopenfilename.return_value = ""

        # テスト対象メソッド呼び出し
        result = self.file_selector.show_dialog()

        # 検証 - 空文字が返されること
        self.assertEqual(result, "")
        mock_askopenfilename.assert_called_once()

    @patch("tkinter.Tk")
    @patch("tkinter.filedialog.askopenfilename")
    def test_tkinter_init_and_withdraw(self, mock_askopenfilename, mock_tk):
        """tkinterの初期化とウィンドウ非表示処理が行われることを確認"""
        # モックの設定
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        mock_askopenfilename.return_value = "/path/to/movie.mov"

        # テスト対象メソッド呼び出し
        self.file_selector.show_dialog()

        # 検証 - Tkの初期化とwithdrawが呼ばれること
        mock_tk.assert_called_once()
        mock_root.withdraw.assert_called_once()


if __name__ == "__main__":
    unittest.main()
